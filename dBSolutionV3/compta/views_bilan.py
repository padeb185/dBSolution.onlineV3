"""Comptes annuels belges (bilan + compte de résultats) et opérations diverses."""
from decimal import Decimal

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_lazy
from django.views.decorators.cache import never_cache

from .bilan import comptes_annuels, presentation
from .models import COMPTES_CONTREPARTIE, LigneOperationDiverse, OperationDiverse
from .views import _autorise, _log, _refus

ZERO = Decimal("0.00")


def _annee(request):
    try:
        return int(request.GET.get("annee") or timezone.localdate().year)
    except ValueError:
        return timezone.localdate().year


def _contexte_bilan(request, annee):
    societe = request.user.societe
    n, n1 = comptes_annuels(societe, annee), comptes_annuels(societe, annee - 1)
    actif, passif, resultats = presentation(n, n1)
    return {
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
    response["Content-Disposition"] = f'inline; filename="{_("Comptes_annuels")}_{annee}.pdf"'
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
