"""Reversement des parts de location aux autres propriétaires du véhicule (direction, comptable, chef mécanicien)."""
from datetime import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .models import Location, ReversementLocation, StatutReversement
from .reversements import generer_reversements

ROLES_REVERSEMENT = ("direction", "comptable", "chef_mecanicien")
ACTION_REVERSEMENT = gettext_noop("Reversement location")


def peut_reverser(user):
    return bool(getattr(user, "is_superuser", False) or getattr(user, "role", None) in ROLES_REVERSEMENT)


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _log(user, texte):
    from utilisateurs.models import UserLog
    UserLog.objects.create(utilisateur=user, action=texte[:255])


def _reversements(request):
    return ReversementLocation.objects.filter(location__societe=request.user.societe).select_related(
        "location", "location__voiture_exemplaire", "location__voiture_exemplaire__voiture_modele", "part")


def _traiter_action(request, rev):
    """Payer / annuler le paiement d'un reversement. Retourne le message."""
    action = request.POST.get("action")
    if action == "annuler":
        rev.statut = StatutReversement.A_PAYER
        rev.date_paiement = None
        rev.save(update_fields=["statut", "date_paiement"])
        _log(request.user, f"{ACTION_REVERSEMENT} - {_('annulé')} : {rev.beneficiaire} {rev.montant_du} €")
        return _("Paiement du reversement annulé : %(nom)s.") % {"nom": rev.beneficiaire}
    try:
        jour = datetime.strptime(request.POST.get("date") or "", "%Y-%m-%d").date()
    except ValueError:
        jour = timezone.localdate()
    mode = request.POST.get("mode") or "VIREMENT"
    if mode not in dict(ReversementLocation._meta.get_field("mode_paiement").choices):
        mode = "VIREMENT"
    rev.statut = StatutReversement.PAYE
    rev.date_paiement = jour
    rev.mode_paiement = mode
    rev.reference = (request.POST.get("reference") or "")[:100]
    rev.save(update_fields=["statut", "date_paiement", "mode_paiement", "reference"])
    _log(request.user, f"{ACTION_REVERSEMENT} : {rev.beneficiaire} {rev.montant_du} €")
    return _("Reversement payé : %(nom)s – %(montant)s €.") % {"nom": rev.beneficiaire, "montant": rev.montant_du}


@login_required
@require_POST
def location_reversements(request, location_id):
    """Depuis le détail d'une location : recalculer, payer ou annuler un reversement."""
    if not peut_reverser(request.user):
        return _refus(request)
    location = get_object_or_404(Location.objects.filter(societe=request.user.societe), id=location_id)
    retour = redirect(f"{reverse('voiture_location:location_detail', kwargs={'location_id': location.id})}#ventilation")
    if request.POST.get("action") == "recalculer":
        facture = location.facture_emise
        if facture is None:
            messages.info(request, _("La location n'est pas encore facturée : les reversements seront calculés à l'émission de la facture."))
            return retour
        with transaction.atomic():
            n = generer_reversements(location, facture.issue_date)
        messages.success(request, _("Reversements recalculés (%(n)s modifié(s)).") % {"n": n})
        return retour
    rev = get_object_or_404(ReversementLocation, pk=request.POST.get("reversement_id"), location=location)
    messages.success(request, _traiter_action(request, rev))
    return retour


@never_cache
@login_required
def reversements_liste(request):
    """Tous les reversements aux propriétaires : à reverser / reversés, totaux par propriétaire."""
    if not peut_reverser(request.user):
        return _refus(request)
    if request.method == "POST":
        rev = get_object_or_404(_reversements(request), pk=request.POST.get("reversement_id"))
        messages.success(request, _traiter_action(request, rev))
        return redirect(f"{reverse('voiture_location:reversements_liste')}?{request.GET.urlencode()}")

    statut = request.GET.get("statut", "A_PAYER")
    qs = _reversements(request)
    if statut in StatutReversement.values:
        qs = qs.filter(statut=statut)
    beneficiaire = (request.GET.get("beneficiaire") or "").strip()
    if beneficiaire:
        qs = qs.filter(beneficiaire=beneficiaire)
    lignes = list(qs.order_by("-date", "beneficiaire"))

    zero = Decimal("0.00")
    par_proprietaire = {}
    for r in _reversements(request).filter(statut=StatutReversement.A_PAYER):
        p = par_proprietaire.setdefault(r.beneficiaire, {"nom": r.beneficiaire, "nb": 0, "total": zero})
        p["nb"] += 1
        p["total"] += r.montant_du
    return render(request, "voiture_location/reversements.html", {
        "lignes": lignes,
        "statut": statut,
        "beneficiaire": beneficiaire,
        "statuts": StatutReversement.choices,
        "par_proprietaire": sorted(par_proprietaire.values(), key=lambda p: p["nom"]),
        "total_a_reverser": sum((p["total"] for p in par_proprietaire.values()), zero),
        "total_liste": sum((r.montant_du for r in lignes), zero),
        "commissions_liste": sum((r.commission_htva for r in lignes), zero),
        "aujourdhui": timezone.localdate(),
        "modes": ReversementLocation._meta.get_field("mode_paiement").choices,
    })
