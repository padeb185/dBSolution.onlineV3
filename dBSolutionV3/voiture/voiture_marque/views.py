from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import VoitureMarque, MarqueFavorite




@login_required
def marque_list(request):
    marques = VoitureMarque.objects.all()
    favoris = []
    if request.user.is_authenticated:
        favoris = list(request.user.favoris_marques.all())

    for marque in marques:
        marque.est_favori = marque in favoris

    return render(request, "voiture_marque.html", {"marques": marques, "favoris": favoris})







@login_required
def toggle_favori_marque(request, id_marque):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    societe = request.user  # ou ton modèle societe
    marque = get_object_or_404(VoitureMarque, id_marque=id_marque)

    favori, created = MarqueFavorite.objects.get_or_create(societe=societe, marque=marque)

    if not created:
        # existait déjà → supprimer
        favori.delete()
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "added"})