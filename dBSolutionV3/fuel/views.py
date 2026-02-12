from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from .forms import FuelForm
from .models import Fuel
from voiture.voiture_exemplaire.models import VoitureExemplaire


class FuelListView(ListView):
    model = Fuel
    template_name = "fuel/fuel_list.html"
    context_object_name = "fuel"
    paginate_by = 20
    ordering = ["date"]



@login_required
def fuel_add(request):
    if request.method == "POST":
        form = FuelForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _("Carburant ajouté avec succès."))

        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = FuelForm()

    return render(request, "fuel/fuel_form.html", {
        "form": form
    })


@never_cache
@login_required
def fuel_list(request):
    fuels = Fuel.objects.select_related(
        "voiture_exemplaire",
        "voiture_marque",
        "voiture_modele"
    ).order_by("-date")

    return render(request, "fuel/fuel_list.html", {
        "fuels": fuels
    })

def fuel_edit(request, pk):
    fuel = get_object_or_404(Fuel, pk=pk)
    if request.method == "POST":
        form = FuelForm(request.POST, instance=fuel)
        if form.is_valid():
            form.save()
            messages.success(request, _("Carburant modifié avec succès."))
            return redirect("fuel_list")
        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = FuelForm(instance=fuel)
    return render(request, "fuel/fuel_form.html", {"form": form, "title": _("Modifier un plein")})





def fuel_delete(request, pk):
    fuel = get_object_or_404(Fuel, pk=pk)
    if request.method == "POST":
        fuel.delete()
        messages.success(request, _("Carburant supprimé avec succès."))
        return redirect("fuel_list")
    return render(request, "fuel/fuel_confirm_delete.html", {"fuel": fuel})






def get_car_info(request):
    immatriculation = request.GET.get('immatriculation')
    data = {}
    if immatriculation:
        try:
            voiture = VoitureExemplaire.objects.get(immatriculation=immatriculation)
            data = {
                'voiture_exemplaire_id': str(voiture.id),
                'voiture_marque': voiture.voiture_marque.nom,
                'voiture_modele': voiture.voiture_modele.nom,
                'taille_reservoir': voiture.voiture_modele.taille_reservoir,
                'type_carburant': voiture.type_carburant,
            }
        except VoitureExemplaire.DoesNotExist:
            data = {'error': 'Véhicule non trouvé'}
    return JsonResponse(data)
