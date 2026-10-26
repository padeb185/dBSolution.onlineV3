from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from maintenance.choices import TVAConfig
from .forms import MaintenanceExterneForm
from .models import MaintenanceExterne

ROLES_AUTORISES = ["chef_mecanicien", "direction"]


def _autorise(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_AUTORISES


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _queryset(request):
    return (
        MaintenanceExterne.objects.filter(societe=request.user.societe)
        .select_related(
            "voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
            "garage__adresse", "garage__voiture_marque",
        )
    )


def _contexte_form(form, maintenance):
    return {
        "form": form,
        "maintenance": maintenance,
        "garages_infos": form.garages_infos,
        "vehicules_infos": form.vehicules_infos,
        "taux_pays": {k: str(v) for k, v in TVAConfig.TVA_PIECES.items()},
        "effets_types": form.effets_types,
    }


@never_cache
@login_required
def maintenance_externe_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    maintenances = _queryset(request)
    totaux = maintenances.aggregate(
        htva=Sum("total_htva"), tva=Sum("total_tva"), tvac=Sum("total_tvac"),
        pieces=Sum("pieces_htva"), mo=Sum("main_oeuvre_htva"),
    )
    totaux = {k: v or Decimal("0.00") for k, v in totaux.items()}
    return render(request, "maintenance_externe/maintenance_externe_list.html", {
        "maintenances": maintenances,
        "totaux": totaux,
    })


@never_cache
@login_required
def maintenance_externe_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    initial = {}
    if request.GET.get("voiture_exemplaire"):
        initial["voiture_exemplaire"] = request.GET["voiture_exemplaire"]
    form = MaintenanceExterneForm(request.POST or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            maintenance = form.save(commit=False)
            if maintenance.societe_id is None:
                maintenance.societe = request.user.societe
            maintenance.appliquer_compteurs()
            maintenance.save()
        messages.success(request, _("Maintenance externe enregistrée : %(total)s € TVAC.") % {
            "total": maintenance.total_tvac})
        return redirect("maintenance_externe:maintenance_externe_liste")
    return render(request, "maintenance_externe/maintenance_externe_form.html", _contexte_form(form, None))


@never_cache
@login_required
def maintenance_externe_modifier(request, maintenance_id):
    if not _autorise(request.user):
        return _refus(request)
    maintenance = get_object_or_404(_queryset(request), id=maintenance_id)
    form = MaintenanceExterneForm(request.POST or None, instance=maintenance, user=request.user)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            recalcul = form.compteurs_modifies()
            if recalcul:
                # Annule l'effet de l'ancienne version (valeurs relues en base)
                ancienne = MaintenanceExterne.objects.select_for_update().get(pk=maintenance.pk)
                ancienne.annuler_compteurs()
            maintenance = form.save(commit=False)
            if recalcul:
                maintenance.appliquer_compteurs()
            maintenance.save()
        messages.success(request, _("Maintenance externe mise à jour."))
        return redirect("maintenance_externe:maintenance_externe_liste")
    return render(request, "maintenance_externe/maintenance_externe_form.html", _contexte_form(form, maintenance))


@never_cache
@login_required
def maintenance_externe_supprimer(request, maintenance_id):
    if not _autorise(request.user):
        return _refus(request)
    maintenance = get_object_or_404(_queryset(request), id=maintenance_id)
    if request.method == "POST":
        with transaction.atomic():
            maintenance.annuler_compteurs()
            maintenance.delete()
        messages.success(request, _("Maintenance externe supprimée."))
        return redirect("maintenance_externe:maintenance_externe_liste")
    return render(request, "maintenance_externe/maintenance_externe_confirm_delete.html", {"maintenance": maintenance})


# =====================================================================
# CARROSSERIE EXTERNE (devis / facture d'un carrossier)
# =====================================================================
from django.http import FileResponse, Http404  # noqa: E402

from .forms import CarrosserieExterneForm  # noqa: E402
from .models import CarrosserieExterne  # noqa: E402


def _carrosseries(request):
    return (
        CarrosserieExterne.objects.filter(societe=request.user.societe)
        .select_related("voiture_exemplaire__voiture_marque", "voiture_exemplaire__voiture_modele",
                        "carrossier", "sinistre__police")
    )


def _contexte_carrosserie(form, carrosserie):
    return {
        "form": form,
        "carrosserie": carrosserie,
        "taux_pays": {k: str(v) for k, v in TVAConfig.TVA_PIECES.items()},
        "sinistres_par_vehicule": form.sinistres_par_vehicule,
    }


@never_cache
@login_required
def carrosserie_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    carrosseries = _carrosseries(request)
    statut = request.GET.get("statut") or ""
    if statut:
        carrosseries = carrosseries.filter(statut=statut)
    facturees = [c for c in carrosseries if c.est_facturee]
    z = Decimal("0.00")
    totaux = {
        "devis": sum((Decimal(c.devis_htva or 0) for c in carrosseries if not c.est_facturee), z),
        "htva": sum((c.total_htva for c in facturees), z),
        "tvac": sum((c.total_tvac for c in facturees), z),
        "assurance": sum((Decimal(c.montant_assurance or 0) for c in facturees if c.prise_en_charge_assurance), z),
        "reste": sum((c.reste_a_charge_tvac for c in facturees), z),
    }
    return render(request, "maintenance_externe/carrosserie_list.html", {
        "carrosseries": carrosseries, "totaux": totaux, "statut": statut,
        "statuts": CarrosserieExterne.Statut.choices,
    })


@never_cache
@login_required
def carrosserie_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    initial = {}
    if request.GET.get("voiture_exemplaire"):
        initial["voiture_exemplaire"] = request.GET["voiture_exemplaire"]
    form = CarrosserieExterneForm(request.POST or None, request.FILES or None, user=request.user, initial=initial)
    if request.method == "POST" and form.is_valid():
        carrosserie = form.save(commit=False)
        carrosserie.societe = request.user.societe
        carrosserie.save()
        messages.success(request, _("Carrosserie externe enregistrée."))
        return redirect("maintenance_externe:carrosserie_detail", carrosserie_id=carrosserie.pk)
    return render(request, "maintenance_externe/carrosserie_form.html", _contexte_carrosserie(form, None))


@never_cache
@login_required
def carrosserie_modifier(request, carrosserie_id):
    if not _autorise(request.user):
        return _refus(request)
    carrosserie = get_object_or_404(_carrosseries(request), id=carrosserie_id)
    form = CarrosserieExterneForm(request.POST or None, request.FILES or None, instance=carrosserie, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Carrosserie externe mise à jour."))
        return redirect("maintenance_externe:carrosserie_detail", carrosserie_id=carrosserie.pk)
    return render(request, "maintenance_externe/carrosserie_form.html", _contexte_carrosserie(form, carrosserie))


@never_cache
@login_required
def carrosserie_detail(request, carrosserie_id):
    if not _autorise(request.user):
        return _refus(request)
    carrosserie = get_object_or_404(_carrosseries(request), id=carrosserie_id)
    return render(request, "maintenance_externe/carrosserie_detail.html", {"carrosserie": carrosserie})


@never_cache
@login_required
def carrosserie_supprimer(request, carrosserie_id):
    if not _autorise(request.user):
        return _refus(request)
    carrosserie = get_object_or_404(_carrosseries(request), id=carrosserie_id)
    if request.method == "POST":
        for champ in ("devis_pdf", "facture_pdf"):
            f = getattr(carrosserie, champ)
            if f:
                f.delete(save=False)
        carrosserie.delete()
        messages.success(request, _("Carrosserie externe supprimée."))
        return redirect("maintenance_externe:carrosserie_liste")
    return render(request, "maintenance_externe/carrosserie_confirm_delete.html", {"carrosserie": carrosserie})


@never_cache
@login_required
def carrosserie_document(request, carrosserie_id, document):
    """PDF du devis ou de la facture : servi uniquement aux utilisateurs autorisés de la société."""
    if not _autorise(request.user) or document not in ("devis", "facture"):
        raise Http404
    carrosserie = get_object_or_404(_carrosseries(request), id=carrosserie_id)
    fichier = getattr(carrosserie, f"{document}_pdf")
    if not fichier:
        raise Http404
    try:
        flux = fichier.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404
    numero = getattr(carrosserie, f"{document}_numero") or carrosserie.pk
    nom = f"{document}_{numero}.pdf".replace(" ", "_").replace('"', "")
    reponse = FileResponse(flux, content_type="application/pdf", as_attachment=False, filename=nom)
    reponse["X-Content-Type-Options"] = "nosniff"
    reponse["Content-Security-Policy"] = "default-src 'none'; sandbox"
    reponse["Cache-Control"] = "private, no-store"
    return reponse
