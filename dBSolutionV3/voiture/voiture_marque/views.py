from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import VoitureMarque, MarqueFavorite


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

    user = request.user
    marque = get_object_or_404(VoitureMarque, id=id_marque)

    if marque in user.favoris_marques.all():
        user.favoris_marques.remove(marque)
        return JsonResponse({"status": "removed"})
    else:
        user.favoris_marques.add(marque)
        return JsonResponse({"status": "added"})