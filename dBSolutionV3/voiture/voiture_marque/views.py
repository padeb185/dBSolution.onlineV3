from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_marque.models import MarqueFavorite
from django.utils.translation import gettext as _
from voiture.voiture_marque.forms import VoitureMarqueForm
from voiture.voiture_moteur.forms import MoteurVoitureForm




@login_required
def marques_list(request):
    marques = VoitureMarque.objects.all().order_by("nom_marque")
    modeles = VoitureModele.objects.filter(
    ).order_by("nom_modele")
    favorites_ids = set(
        MarqueFavorite.objects.filter(
            societe=request.user
        ).values_list("marque_id", flat=True)
    )

    return render(request, "voiture_marque/marques_list.html", {
        "marques": marques,
        "modeles": modeles,
        "favorites_ids": favorites_ids,
    })



@login_required
def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(
        voiture_marque=marque
    ).order_by("nom_modele")
    return render(request, "voiture_modele/modeles_par_marque.html", {
        "marque": marque,
        "modeles": modeles,
    })


@login_required
def toggle_marque_favorite(request, marque_id):
    if request.method != "POST":
        raise Http404

    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)

    favori, created = MarqueFavorite.objects.get_or_create(
        societe=request.user,
        marque=marque
    )

    if not created:
        favori.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({
        "is_favorite": is_favorite
    })



@login_required
def marques_favorites(request):
    marques = VoitureMarque.objects.filter(
        favoris__societe=request.user
    ).distinct()

    return render(request, "voiture_marque/marques_favorites.html", {
        "marques": marques
    })


def ajouter_marque(request):
    if request.method == "POST":
        nom_marque = request.POST.get("marque", "").strip()
        if nom_marque:
            # Vérifie si la marque existe déjà
            if VoitureMarque.objects.filter(nom_marque__iexact=nom_marque).exists():
                messages.error(request, "Cette marque existe déjà !")
            else:
                marque = VoitureMarque.objects.create(nom_marque=nom_marque)
                messages.success(request, f"Marque '{marque.nom_marque}' ajoutée avec succès !")
                return redirect("voiture_marque:ajouter_marque")
        else:
            messages.error(request, "Veuillez entrer un nom de marque.")

    return render(request, "voiture_marque/ajouter_marque.html")


@require_POST
def check_marque(request):
    nom_marque = request.POST.get("nom_marque", "").strip()
    exists = False
    if nom_marque:
        exists = VoitureMarque.objects.filter(nom_marque__iexact=nom_marque).exists()
    return JsonResponse({"exists": exists})