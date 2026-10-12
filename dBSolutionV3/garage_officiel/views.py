from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache

from .forms import GarageOfficielForm
from .models import GarageOfficiel

ROLES_AUTORISES = ["chef_mecanicien", "direction"]


def _autorise(user):
    return user.is_superuser or getattr(user, "role", None) in ROLES_AUTORISES


def _refus(request):
    messages.error(request, _("Accès refusé"))
    return redirect("utilisateurs:dashboard")


def _queryset(request):
    return (
        GarageOfficiel.objects.filter(societe=request.user.societe)
        .select_related("adresse", "voiture_marque")
    )


@never_cache
@login_required
def garage_liste(request):
    if not _autorise(request.user):
        return _refus(request)
    garages = _queryset(request).annotate(nb_maintenances=Count("maintenances_externes"))
    return render(request, "garage_officiel/garage_list.html", {"garages": garages})


@never_cache
@login_required
def garage_ajouter(request):
    if not _autorise(request.user):
        return _refus(request)
    form = GarageOfficielForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        garage = form.save()
        messages.success(request, _("Garage '%(nom)s' créé avec succès.") % {"nom": garage.nom})
        suivant = request.GET.get("next")
        if suivant and suivant.startswith("/"):
            return redirect(suivant)
        return redirect("garage_officiel:garage_liste")
    return render(request, "garage_officiel/garage_form.html", {"form": form, "garage": None})


@never_cache
@login_required
def garage_modifier(request, garage_id):
    if not _autorise(request.user):
        return _refus(request)
    garage = get_object_or_404(_queryset(request), id=garage_id)
    form = GarageOfficielForm(request.POST or None, instance=garage, user=request.user)
    if request.method == "POST" and form.is_valid():
        garage = form.save()
        messages.success(request, _("Garage '%(nom)s' mis à jour.") % {"nom": garage.nom})
        return redirect("garage_officiel:garage_liste")
    return render(request, "garage_officiel/garage_form.html", {"form": form, "garage": garage})


@never_cache
@login_required
def garage_supprimer(request, garage_id):
    if not _autorise(request.user):
        return _refus(request)
    garage = get_object_or_404(_queryset(request), id=garage_id)
    if request.method == "POST":
        try:
            garage.delete()
            messages.success(request, _("Garage supprimé."))
        except ProtectedError:
            messages.error(request, _("Impossible de supprimer ce garage : des maintenances externes y sont liées."))
        return redirect("garage_officiel:garage_liste")
    return render(request, "garage_officiel/garage_confirm_delete.html", {"garage": garage})
