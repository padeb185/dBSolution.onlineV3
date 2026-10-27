"""Comptes annuels belges (bilan + compte de résultats) et opérations diverses."""
from decimal import Decimal

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache

from .bilan import SAISIE, comptes_annuels, libelle_rubrique, presentation, reference_pour
from .models import COMPTES_CONTREPARTIE, BilanReference, LigneOperationDiverse, OperationDiverse
from .views import _autorise, _log, _refus

ZERO = Decimal("0.00")


def _annee(request):
    try:
        return int(request.GET.get("annee") or timezone.localdate().year)
    except ValueError:
        return timezone.localdate().year


def _schema(request, societe, annee):
    """Schéma demandé (?schema=), sinon celui du dernier bilan de référence, sinon abrégé."""
    demande = (request.GET.get("schema") or "").upper()
    if demande in BilanReference.Schema.values:
        return demande
    ref = reference_pour(societe, annee)
    return ref.schema if ref else BilanReference.Schema.ABREGE


def _contexte_bilan(request, annee):
    societe = request.user.societe
    schema = _schema(request, societe, annee)
    n, n1 = comptes_annuels(societe, annee), comptes_annuels(societe, annee - 1)
    actif, passif, resultats = presentation(n, n1, schema)
    return {
        "schema": schema, "schemas": BilanReference.Schema.choices,
        "schema_libelle": BilanReference.Schema(schema).label,
        "reference": n.get("reference"), "source": n.get("source"),
        "annee": annee, "annee_precedente": annee - 1, "societe": societe,
        "actif": actif, "passif": passif, "resultats": resultats,
        "n": n, "n1": n1, "ecart": n["totaux"]["ecart"],
        "equilibre": abs(n["totaux"]["ecart"]) < Decimal("0.01"),
        "annees": range(timezone.localdate().year - 6, timezone.localdate().year + 1),
        "date_export": timezone.now(),
    }


@never_cache
@login_required
def bilan(request):
    if not _autorise(request.user):
        return _refus(request)
    return render(request, "compta/bilan/bilan.html", _contexte_bilan(request, _annee(request)))


@login_required
def bilan_pdf(request):
    if not _autorise(request.user):
        return _refus(request)
    from weasyprint import HTML
    annee = _annee(request)
    html = render_to_string("compta/bilan/bilan_pdf.html", _contexte_bilan(request, annee), request=request)
    pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{_("Comptes_annuels")}_{annee}_{_("indicatif")}.pdf"'
    return response


# ==================================================================
# OPÉRATIONS DIVERSES
# ==================================================================
class OperationDiverseForm(forms.ModelForm):
    class Meta:
        model = OperationDiverse
        fields = ["journal", "date", "piece", "libelle"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}


class LigneODForm(forms.ModelForm):
    class Meta:
        model = LigneOperationDiverse
        fields = ["compte", "libelle", "debit", "credit"]
        widgets = {
            "compte": forms.TextInput(attrs={"list": "comptes-pcmn", "class": "border rounded px-2 py-1 w-28 font-mono"}),
            "libelle": forms.TextInput(attrs={"class": "border rounded px-2 py-1 w-full"}),
            "debit": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "border rounded px-2 py-1 w-32 text-right debit"}),
            "credit": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "border rounded px-2 py-1 w-32 text-right credit"}),
        }

    def clean_compte(self):
        c = (self.cleaned_data.get("compte") or "").strip()
        if not c.isdigit() or len(c) < 2:
            raise forms.ValidationError(gettext_lazy("Compte PCMN invalide (chiffres uniquement)."))
        return c.ljust(6, "0") if len(c) < 6 else c

    def clean(self):
        cleaned = super().clean()
        d, c = cleaned.get("debit") or ZERO, cleaned.get("credit") or ZERO
        if d and c:
            raise forms.ValidationError(gettext_lazy("Une ligne est soit au débit, soit au crédit."))
        return cleaned


class BaseLignesOD(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        debit = credit = ZERO
        nb = 0
        for f in self.forms:
            if not getattr(f, "cleaned_data", None) or f.cleaned_data.get("DELETE"):
                continue
            debit += f.cleaned_data.get("debit") or ZERO
            credit += f.cleaned_data.get("credit") or ZERO
            nb += 1
        if nb < 2:
            raise forms.ValidationError(gettext_lazy("Une opération comporte au moins deux lignes."))
        if debit != credit:
            raise forms.ValidationError(gettext_lazy("L'opération n'est pas équilibrée : débit %(d)s € ≠ crédit %(c)s €.") % {"d": debit, "c": credit})


LignesODFormSet = forms.inlineformset_factory(OperationDiverse, LigneOperationDiverse, form=LigneODForm,
                                              formset=BaseLignesOD, extra=4, can_delete=True)


@never_cache
@login_required
def od_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    ods = OperationDiverse.objects.filter(societe=request.user.societe).prefetch_related("lignes")
    annee = request.GET.get("annee")
    if annee and annee.isdigit():
        ods = ods.filter(date__year=int(annee))
    return render(request, "compta/bilan/od_liste.html", {"ods": ods, "annee": annee or ""})


def _od_form(request, od=None):
    societe = request.user.societe
    instance = od or OperationDiverse(societe=societe)
    form = OperationDiverseForm(request.POST or None, instance=instance)
    formset = LignesODFormSet(request.POST or None, instance=instance, prefix="lignes")
    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                obj = form.save(commit=False)
                obj.societe = societe
                if not obj.cree_par_id:
                    obj.cree_par = request.user
                obj.save()
                formset.instance = obj
                formset.save()
            _log(request, f"Opération diverse – {obj.libelle}")
            messages.success(request, _("L'opération diverse a été enregistrée."))
            return redirect("compta:od_liste")
        messages.error(request, _("Le formulaire contient des erreurs."))
    return render(request, "compta/bilan/od_form.html", {
        "form": form, "formset": formset, "od": od, "comptes_pcmn": COMPTES_CONTREPARTIE,
    })


@never_cache
@login_required
def od_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    return _od_form(request)


@never_cache
@login_required
def od_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    return _od_form(request, get_object_or_404(OperationDiverse, societe=request.user.societe, pk=pk))


@login_required
def od_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    od = get_object_or_404(OperationDiverse, societe=request.user.societe, pk=pk)
    if request.method == "POST":
        od.delete()
        messages.success(request, _("L'opération diverse a été supprimée."))
        return redirect("compta:od_liste")
    return render(request, "compta/immo/supprimer.html", {
        "titre": _("Supprimer l'opération diverse"), "objet": od, "retour": "compta:od_liste",
    })



# ==================================================================
# DERNIER BILAN (comptable) : saisie par rubriques
# ==================================================================
def _lignes_saisie(schema):
    return {cote: [(cle,) + libelle_rubrique(cle) for cle in cles] for cote, cles in SAISIE[schema].items()}


class BilanReferenceForm(forms.ModelForm):
    """Données générales + un champ montant par rubrique des deux schémas (le schéma choisi décide)."""

    class Meta:
        model = BilanReference
        fields = ["annee", "schema", "etabli_par", "date_depot", "remarques"]
        widgets = {
            "date_depot": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, societe=None, **kwargs):
        self.societe = societe
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "border rounded px-3 py-2 w-full")
        cles = {c for sch in SAISIE.values() for cotes in sch.values() for c in cotes}
        for cle in sorted(cles):
            self.fields[f"m_{cle}"] = forms.DecimalField(
                required=False, max_digits=15, decimal_places=2,
                initial=self.instance.montants.get(cle) if self.instance.pk else None,
                widget=forms.NumberInput(attrs={"step": "0.01", "class": "montant border rounded px-2 py-1 w-40 text-right",
                                                "data-cle": cle}),
            )

    def lignes(self):
        """{schéma: {côté: [(cle, code, libellé, champ)]}} pour le template."""
        return {
            schema: {cote: [(cle, code, lib, self[f"m_{cle}"]) for cle, code, lib in lignes]
                     for cote, lignes in _lignes_saisie(schema).items()}
            for schema in SAISIE
        }

    def clean_annee(self):
        annee = self.cleaned_data["annee"]
        if annee < 1990 or annee > timezone.localdate().year:
            raise forms.ValidationError(gettext_lazy("Exercice invalide."))
        qs = BilanReference.objects.filter(societe=self.societe, annee=annee)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(gettext_lazy("Un bilan de référence existe déjà pour cet exercice."))
        return annee

    def clean(self):
        cleaned = super().clean()
        schema = cleaned.get("schema") or BilanReference.Schema.ABREGE
        montants = {}
        for cote, cles in SAISIE[schema].items():
            for cle in cles:
                v = cleaned.get(f"m_{cle}")
                if v:
                    montants[cle] = str(v)
        total = lambda cote: sum((Decimal(montants.get(c, "0")) for c in SAISIE[schema][cote]), ZERO)
        ecart = total("actif") - total("passif")
        if not montants:
            raise forms.ValidationError(gettext_lazy("Indiquez au moins un montant."))
        if abs(ecart) >= Decimal("0.01"):
            raise forms.ValidationError(
                gettext_lazy("Le bilan n'est pas équilibré : total actif – total passif = %(e)s €.") % {"e": ecart})
        self.montants = montants
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.montants = self.montants
        if commit:
            obj.save()
        return obj


@never_cache
@login_required
def references_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    refs = BilanReference.objects.filter(societe=request.user.societe)
    return render(request, "compta/bilan/references_liste.html", {"refs": refs})


def _reference_form(request, ref=None):
    societe = request.user.societe
    instance = ref or BilanReference(societe=societe)
    form = BilanReferenceForm(request.POST or None, instance=instance, societe=societe)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.societe = societe
            if not obj.cree_par_id:
                obj.cree_par = request.user
            obj.save()
            _log(request, f"Bilan de référence {obj.annee}")
            messages.success(request, _("Le bilan %(annee)s a été enregistré. Il sert de base aux bilans suivants.") % {"annee": obj.annee})
            return redirect(f"{reverse('compta:bilan')}?annee={obj.annee}")
        messages.error(request, _("Le formulaire contient des erreurs."))
    return render(request, "compta/bilan/reference_form.html", {"form": form, "ref": ref})


@never_cache
@login_required
def reference_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    return _reference_form(request)


@never_cache
@login_required
def reference_modifier(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    return _reference_form(request, get_object_or_404(BilanReference, societe=request.user.societe, pk=pk))


@login_required
def reference_supprimer(request, pk):
    if not _autorise(request.user):
        return _refus(request)
    ref = get_object_or_404(BilanReference, societe=request.user.societe, pk=pk)
    if request.method == "POST":
        ref.delete()
        messages.success(request, _("Le bilan de référence a été supprimé."))
        return redirect("compta:references_liste")
    return render(request, "compta/immo/supprimer.html", {
        "titre": _("Supprimer le bilan de référence"), "objet": ref, "retour": "compta:references_liste",
    })
