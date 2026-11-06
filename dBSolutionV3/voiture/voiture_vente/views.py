from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from utils.securite import peut_supprimer, refuser_suppression
from voiture.voiture_exemplaire.models import VoitureExemplaire

from . import calculs
from .forms import AnnulationForm, VenteVehiculeForm
from .models import VenteVehicule


def _autorise(user):
    from voiture.voiture_exemplaire.views import _finance_autorise
    return _finance_autorise(user)


def _refuser(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _ventes(request):
    return (VenteVehicule.objects.filter(societe=request.user.societe)
            .select_related("exemplaire", "exemplaire__voiture_marque", "exemplaire__voiture_modele",
                            "immobilisation", "compte_encaissement", "client_particulier", "societe_cliente"))


def _log(request, action):
    try:
        from utilisateurs.models import UserLog
        UserLog.objects.create(utilisateur=request.user, action=action[:255])
    except Exception:
        pass


# ------------------------------------------------------------------
# Liste
# ------------------------------------------------------------------
@never_cache
@login_required
def liste(request):
    if not _autorise(request.user):
        return _refuser(request)
    qs = _ventes(request)
    annee = request.GET.get("annee")
    if annee and annee.isdigit():
        qs = qs.filter(date_vente__year=int(annee))
    statut = request.GET.get("statut")
    if statut in VenteVehicule.Statut.values:
        qs = qs.filter(statut=statut)
    totaux = qs.filter(statut=VenteVehicule.Statut.EMISE).aggregate(
        nb=Count("id"), htva=Sum("prix_htva"), tva=Sum("montant_tva"), tvac=Sum("prix_tvac"))
    annees = sorted({d.year for d in _ventes(request).values_list("date_vente", flat=True) if d}, reverse=True)
    return render(request, "voiture_vente/liste.html", {
        "ventes": qs, "totaux": totaux, "annees": annees, "annee": annee or "", "statut": statut or "",
        "statuts": VenteVehicule.Statut.choices,
    })


# ------------------------------------------------------------------
# Création
# ------------------------------------------------------------------
def _vehicules_vendables(request):
    vendus = VenteVehicule.objects.filter(societe=request.user.societe).exclude(
        statut=VenteVehicule.Statut.ANNULEE).values("exemplaire_id")
    return (VoitureExemplaire.objects.filter(societe=request.user.societe, client__isnull=True)
            .exclude(pk__in=vendus).select_related("voiture_marque", "voiture_modele")
            .order_by("voiture_marque__nom_marque", "immatriculation"))


def _valeurs_initiales(exemplaire):
    fv = getattr(exemplaire, "financement", None) if hasattr(exemplaire, "financement") else None
    initial = {
        "date_vente": timezone.localdate(),
        "kilometrage_vente": exemplaire.kilometres_chassis or None,
        "montant_saisi": exemplaire.valeur_revente or None,
        "prix_achat_marge": exemplaire.prix_achat,
        "regime_tva": VenteVehicule.RegimeTVA.NORMAL,
    }
    if fv is not None:
        initial["immobilisation"] = fv.immobilisation_id
        if fv.mode != fv.Mode.RENTING and not fv.tva_deductible_effective:
            initial["regime_tva"] = VenteVehicule.RegimeTVA.EXONERE
    return initial


@never_cache
@login_required
def nouvelle(request):
    if not _autorise(request.user):
        return _refuser(request)
    exemplaire_id = request.GET.get("exemplaire") or request.POST.get("exemplaire")
    if not exemplaire_id:
        return render(request, "voiture_vente/choisir_vehicule.html", {"vehicules": _vehicules_vendables(request)})
    try:
        exemplaire = _vehicules_vendables(request).get(pk=exemplaire_id)
    except (VoitureExemplaire.DoesNotExist, ValueError, ValidationError):
        try:
            existante = _ventes(request).exclude(statut=VenteVehicule.Statut.ANNULEE).filter(
                exemplaire_id=exemplaire_id).first()
        except (ValueError, ValidationError):
            existante = None
        if existante:
            messages.info(request, _("Ce véhicule a déjà une vente en cours."))
            return redirect("voiture_vente:detail", pk=existante.pk)
        raise Http404

    societe = request.user.societe
    instance = VenteVehicule(societe=societe, exemplaire=exemplaire, cree_par=request.user)
    if request.method == "POST":
        form = VenteVehiculeForm(request.POST, instance=instance, societe=societe, exemplaire=exemplaire)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.completer_acheteur()
            vente.save()
            messages.success(request, _("Vente enregistrée en brouillon. Vérifiez le bilan puis émettez la facture."))
            return redirect("voiture_vente:detail", pk=vente.pk)
    else:
        form = VenteVehiculeForm(instance=instance, societe=societe, exemplaire=exemplaire,
                                 initial=_valeurs_initiales(exemplaire))
    return render(request, "voiture_vente/form.html", {"form": form, "exemplaire": exemplaire, "vente": None})


@never_cache
@login_required
def modifier(request, pk):
    if not _autorise(request.user):
        return _refuser(request)
    vente = get_object_or_404(_ventes(request), pk=pk)
    if vente.est_annulee:
        messages.error(request, _("Une vente annulée ne peut plus être modifiée."))
        return redirect("voiture_vente:detail", pk=pk)
    if request.method == "POST":
        form = VenteVehiculeForm(request.POST, instance=vente, societe=request.user.societe, exemplaire=vente.exemplaire)
        if form.is_valid():
            vente = form.save(commit=False)
            if vente.est_brouillon:
                vente.completer_acheteur()
            vente.save()
            messages.success(request, _("Vente modifiée."))
            return redirect("voiture_vente:detail", pk=vente.pk)
    else:
        form = VenteVehiculeForm(instance=vente, societe=request.user.societe, exemplaire=vente.exemplaire)
    return render(request, "voiture_vente/form.html", {"form": form, "exemplaire": vente.exemplaire, "vente": vente})


# ------------------------------------------------------------------
# Détail : bilan, alertes, écritures
# ------------------------------------------------------------------
@never_cache
@login_required
def detail(request, pk):
    if not _autorise(request.user):
        return _refuser(request)
    vente = get_object_or_404(_ventes(request), pk=pk)
    alertes = vente.alertes()
    ecritures = vente.ecritures() if not vente.est_brouillon else []
    ecritures_cession = []
    if vente.immobilisation_id and vente.est_emise:
        ecritures_cession = [l for l in vente.immobilisation.ecritures(vente.date_vente, vente.date_vente)
                             if l["journal"] == "OD"]
    apercu = []
    if vente.est_brouillon:
        # Aperçu des écritures de vente qui seront passées à l'émission
        apercu = vente._lignes_vente(vente.date_vente, _("Vente véhicule"))
    return render(request, "voiture_vente/detail.html", {
        "vente": vente,
        "ex": vente.exemplaire,
        "prix": vente.calcul_prix(),
        "alertes": alertes,
        "bloquant": any(n == "erreur" for n, _m in alertes),
        "bilan": calculs.bilan(vente),
        "ecritures": ecritures,
        "ecritures_cession": ecritures_cession,
        "apercu": apercu,
        "revision": calculs.revision_tva(vente, vente.pays),
        "peut_supprimer": peut_supprimer(request.user),
        "form_annulation": AnnulationForm(initial={"date_annulation": timezone.localdate()}),
    })


@login_required
@require_POST
def emettre(request, pk):
    if not _autorise(request.user):
        return _refuser(request)
    vente = get_object_or_404(_ventes(request), pk=pk, statut=VenteVehicule.Statut.BROUILLON)
    if not calculs.peut_emettre(vente, vente.pays):
        messages.error(request, _("La facture ne peut pas être émise : corrigez les points bloquants."))
        return redirect("voiture_vente:detail", pk=pk)
    vente.emettre()
    _log(request, f"{_('Émission de la facture de vente du véhicule')} {vente.numero} – {vente.exemplaire.immatriculation or ''}")
    messages.success(request, _("Facture %(n)s émise. La cession est enregistrée dans les immobilisations.") % {"n": vente.numero})
    return redirect("voiture_vente:detail", pk=pk)


@login_required
@require_POST
def annuler(request, pk):
    if not _autorise(request.user):
        return _refuser(request)
    vente = get_object_or_404(_ventes(request), pk=pk, statut=VenteVehicule.Statut.EMISE)
    form = AnnulationForm(request.POST)
    if not form.is_valid() or form.cleaned_data["date_annulation"] < vente.date_vente:
        messages.error(request, _("Indiquez un motif et une date de note de crédit postérieure à la vente."))
        return redirect("voiture_vente:detail", pk=pk)
    vente.annuler(form.cleaned_data["motif"], form.cleaned_data["date_annulation"])
    _log(request, f"{_('Annulation de la vente du véhicule')} {vente.numero} ({vente.numero_note_credit})")
    messages.success(request, _("Vente annulée : note de crédit %(n)s.") % {"n": vente.numero_note_credit})
    return redirect("voiture_vente:detail", pk=pk)


@login_required
@require_POST
def supprimer(request, pk):
    if not peut_supprimer(request.user):
        return refuser_suppression(request)
    vente = get_object_or_404(_ventes(request), pk=pk)
    if not vente.est_brouillon:
        messages.error(request, _("Une facture émise ne peut pas être supprimée : annulez-la par une note de crédit."))
        return redirect("voiture_vente:detail", pk=pk)
    _log(request, f"{_('Suppression du brouillon de vente du véhicule')} {vente.exemplaire.immatriculation or vente.exemplaire}")
    vente.delete()
    messages.success(request, _("Brouillon supprimé."))
    return redirect("voiture_vente:liste")


# ------------------------------------------------------------------
# PDF : facture, note de crédit, certificat de cession
# ------------------------------------------------------------------
DOCUMENTS = {
    "facture": "voiture_vente/pdf_facture.html",
    "note-credit": "voiture_vente/pdf_facture.html",
    "cession": "voiture_vente/pdf_cession.html",
}


@login_required
def pdf(request, pk, document):
    if not _autorise(request.user):
        return _refuser(request)
    if document not in DOCUMENTS:
        raise Http404
    vente = get_object_or_404(_ventes(request), pk=pk)
    if document == "note-credit" and not vente.est_annulee:
        raise Http404
    from django.template.loader import render_to_string
    from weasyprint import HTML

    html = render_to_string(DOCUMENTS[document], {
        "vente": vente, "ex": vente.exemplaire, "societe": request.user.societe,
        "note_credit": document == "note-credit", "date_export": timezone.now(),
    }, request=request)
    contenu = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    noms = {"facture": _("Facture"), "note-credit": _("Note_de_credit"), "cession": _("Certificat_de_cession")}
    numero = (vente.numero_note_credit if document == "note-credit" else vente.numero) or _("brouillon")
    nom = f"{noms[document]}_{numero}_{vente.exemplaire.immatriculation or ''}.pdf".replace(" ", "_")
    response = HttpResponse(contenu, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nom}"'
    return response
