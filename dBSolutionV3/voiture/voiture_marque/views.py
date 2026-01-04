from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import VoitureMarque, MarqueFavorite

def marque_list(request):
    marques = VoitureMarque.objects.all()
    favoris = []  # liste vide pour l’instant ou récupère les favoris de l’utilisateur
    for marque in marques:
        marque.est_favori = marque.id_marque in [f.id_marque for f in favoris]
    return render(request, "voiture_marque.html", {"marques": marques, "favoris": favoris})


def liste_marques(request, id_marque):
    marque = get_object_or_404(VoitureMarque, id_marque=id_marque)
    voitures = VoitureMarque.objects.filter(marque=marque)
    return render(request, "voiture_marque/liste_marques.html", {
        "marque": marque,
        "voitures": voitures
    })




def toggle_favori_marque(request, marque_id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Utilisateur non connecté"}, status=403)

    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    favori, created = MarqueFavorite.objects.get_or_create(
        utilisateur=request.user,
        marque=marque
    )
    if not created:
        favori.delete()
        status = "removed"
    else:
        status = "added"

    return JsonResponse({"status": status})
