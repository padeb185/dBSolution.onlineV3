from django.contrib.auth.decorators import login_required
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




@login_required
def toggle_favori_marque(request, marque_id):
    if request.method == "POST":
        user = request.user
        try:
            marque = VoitureMarque.objects.get(id_marque=marque_id)
        except VoitureMarque.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Marque non trouvée'}, status=404)

        if marque in user.favoris_marques.all():
            user.favoris_marques.remove(marque)
            return JsonResponse({'status': 'removed'})
        else:
            user.favoris_marques.add(marque)
            return JsonResponse({'status': 'added'})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=400)
