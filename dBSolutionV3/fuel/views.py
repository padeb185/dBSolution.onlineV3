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
    context_object_name = "fuels"   # ⚠️ important : pluriel
    paginate_by = 20
    ordering = ["-date"]

    def get_queryset(self):
        return (
            Fuel.objects
            .select_related(
                "utilisateur",
                "voiture_exemplaire",
                "voiture_exemplaire__voiture_modele",
                "voiture_exemplaire__voiture_modele__voiture_marque",
            )
            .order_by("-date")
        )




@login_required
def fuel_add(request):
    if request.method == "POST":
        form = FuelForm(request.POST)
        if form.is_valid():
            fuel = form.save(commit=False)
            fuel.utilisateur = request.user  # ⚡ Utilisateur courant
            fuel.save()
            messages.success(request, _("Carburant ajouté avec succès."))

        else:
            messages.error(request, _("Veuillez corriger les erreurs ci-dessous."))
    else:
        form = FuelForm()

    # ⚡ Passer les choices de type_carburant au template
    type_carburant_choices = Fuel._meta.get_field("type_carburant").choices

    return render(
        request,
        "fuel/fuel_form.html",
        {
            "form": form,
            "fuel": form.instance,
            "type_carburant_choices": type_carburant_choices,
        },
    )


@never_cache
@login_required
def fuel_list(request):
    # On sélectionne les relations nécessaires pour éviter les requêtes supplémentaires
    fuels = Fuel.objects.select_related(
        "utilisateur",
        "voiture_exemplaire",
        "voiture_exemplaire__voiture_modele",
        "voiture_exemplaire__voiture_modele__voiture_marque",
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
                'voiture_marque': voiture.voiture_marque.nom_marque,
                'voiture_modele': voiture.voiture_modele.nom_modele,
                'taille_reservoir': voiture.voiture_modele.taille_reservoir,
                'type_carburant': voiture.voiture_modele.type_carburant,
            }
        except VoitureExemplaire.DoesNotExist:
            data = {'error': 'Véhicule non trouvé'}
    return JsonResponse(data)






def get_voiture_by_immat(request):
    immat = request.GET.get("immatriculation")

    try:
        voiture = VoitureExemplaire.objects.get(immatriculation=immat)

        return JsonResponse({
            "id": voiture.id,
            "marque": voiture.voiture_marque.nom_marque,
            "modele": voiture.voiture_modele.nom_modele,
            "volume": voiture.voiture_modele.taille_reservoir,
        })

    except VoitureExemplaire.DoesNotExist:
        return JsonResponse({"error": "Immatriculation introuvable"})
