from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _, gettext_noop
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import LocationForm
from .models import Location

ROLES_AUTORISES = ["vendeur", "direction", "chef_mecanicien"]

ACTION_FACTURE_LOCATION = gettext_noop("Création d'une facture de location")


def _autorise(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_AUTORISES


def _queryset(request):
    return (
        Location.objects
        .filter(societe=request.user.societe)
        .select_related(
            "voiture_exemplaire__voiture_marque",
            "voiture_exemplaire__voiture_modele",
            "client",
            "societe_cliente",
            "client_pilotage__client_particulier",
            "societe__adresse",
        )
        .prefetch_related("factures")
    )


def _peut_facturer(user):
    from facture.views import ROLES_FACTURATION
    return user.is_superuser or getattr(user, "role", None) in ROLES_FACTURATION


@never_cache
@login_required
def location_liste(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    return render(request, "voiture_location/location_list.html", {
        "locations": _queryset(request),
        "peut_facturer": _peut_facturer(request.user),
        "type_client": "CLIENT",
        "type_pro": "PRO",
    })


@login_required
def location_ajouter(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    exemplaire_id = request.GET.get("exemplaire")
    initial = {"voiture_exemplaire": exemplaire_id} if exemplaire_id else {}

    form = LocationForm(request.POST or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        location = form.save()
        messages.success(request, _("Location '%(loc)s' créée avec succès.") % {"loc": location})
        return redirect("voiture_location:location_liste")

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": None, "taux_tva": Location(societe=request.user.societe).taux_tva,
    })


@login_required
def location_modifier(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    location = get_object_or_404(_queryset(request), id=location_id)
    form = LocationForm(request.POST or None, instance=location, user=request.user)
    if request.method == "POST" and form.is_valid():
        location = form.save()
        messages.success(request, _("Location '%(loc)s' mise à jour.") % {"loc": location})
        return redirect("voiture_location:location_liste")

    return render(request, "voiture_location/location_form.html", {
        "form": form, "location": location, "taux_tva": location.taux_tva,
    })


@login_required
def location_supprimer(request, location_id):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    location = get_object_or_404(_queryset(request), id=location_id)
    if request.method == "POST":
        try:
            location.delete()
            messages.success(request, _("Location supprimée."))
        except ProtectedError:
            messages.error(request, _("Impossible de supprimer cette location."))
        return redirect("voiture_location:location_liste")

    return render(request, "voiture_location/location_confirm_delete.html", {"location": location})


# -----------------------------
# Facturation d'une location (prix TVAC)
# -----------------------------
@login_required
@require_POST
def location_facturer(request, location_id):
    if not _peut_facturer(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("voiture_location:location_liste")

    from facture.models import Facture
    from facture.services import creer_facture_depuis_location
    from utilisateurs.models import UserLog

    location = get_object_or_404(_queryset(request), id=location_id)

    existante = location.facture
    if existante is not None:
        messages.info(request, _("Cette location est déjà facturée."))
        return redirect("facture:detail", pk=existante.pk)

    type_facture = request.POST.get("type_facture")
    if type_facture not in Facture.TypeFacture.values:
        messages.error(request, _("Type de facture inconnu."))
        return redirect("voiture_location:location_liste")

    facture = creer_facture_depuis_location(location, type_facture, request.user)
    UserLog.objects.create(
        utilisateur=request.user,
        action=f"{ACTION_FACTURE_LOCATION} : {location}",
    )
    if type_facture == Facture.TypeFacture.PRO and not facture.societe_cliente_id:
        messages.warning(request, _("Sélectionnez le client professionnel avant d'émettre la facture."))
    messages.success(request, _("Brouillon de facture créé. Le prix de location est TVAC : vérifiez la ligne avant d'émettre."))
    return redirect("facture:modifier", pk=facture.pk)


# -----------------------------
# Ventes : détail des locations (HTVA / TVA / TVAC)
# -----------------------------
TYPES_PERIODE_VENTES = ("mois", "trimestre", "annee", "tout")


@never_cache
@login_required
def ventes_detail(request):
    if not _autorise(request.user):
        messages.error(request, _("Accès refusé"))
        return redirect("utilisateurs:dashboard")

    from facture.tva import CalculTVA

    aujourdhui = timezone.localdate()
    type_periode = request.GET.get("periode", "annee")
    if type_periode not in TYPES_PERIODE_VENTES:
        type_periode = "annee"

    def entier(nom, defaut):
        try:
            return int(request.GET.get(nom, defaut))
        except (TypeError, ValueError):
            return defaut

    annee = entier("annee", aujourdhui.year)
    numero_defaut = aujourdhui.month if type_periode == "mois" else (aujourdhui.month - 1) // 3 + 1
    numero = entier("numero", numero_defaut)

    locations = _queryset(request)
    debut = fin = None
    if type_periode != "tout":
        debut, fin = CalculTVA.bornes(type_periode, annee, numero)
        locations = locations.filter(date_debut__range=(debut, fin))
    locations = list(locations.order_by("date_debut", "created_at"))

    zero = Decimal("0.00")

    def cumul(liste):
        return {
            "nb": len(liste),
            "htva": sum((l.prix_htva for l in liste), zero),
            "tva": sum((l.montant_tva for l in liste), zero),
            "tvac": sum((l.prix_tvac for l in liste), zero),
            "km": sum((l.kilometrage or 0 for l in liste), 0),
        }

    facturees = [l for l in locations if l.facture is not None]
    non_facturees = [l for l in locations if l.facture is None]

    return render(request, "voiture_location/ventes_detail.html", {
        "locations": locations,
        "totaux": cumul(locations),
        "totaux_circuit": cumul([l for l in locations if l.type_location == "circuit"]),
        "totaux_route": cumul([l for l in locations if l.type_location == "route"]),
        "totaux_facturees": cumul(facturees),
        "totaux_non_facturees": cumul(non_facturees),
        "type_periode": type_periode,
        "annee": annee,
        "numero": numero,
        "debut": debut,
        "fin": fin,
        "annees": range(aujourdhui.year - 5, aujourdhui.year + 1),
        "mois": range(1, 13),
        "trimestres": range(1, 5),
        "peut_facturer": _peut_facturer(request.user),
    })
