from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        maintenance = form.save()
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
        maintenance = form.save()
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
        maintenance.delete()
        messages.success(request, _("Maintenance externe supprimée."))
        return redirect("maintenance_externe:maintenance_externe_liste")
    return render(request, "maintenance_externe/maintenance_externe_confirm_delete.html", {"maintenance": maintenance})
