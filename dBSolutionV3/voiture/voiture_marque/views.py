from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import VoitureMarque, MarqueFavorite
from voiture.voiture_modele.models import VoitureModele




@login_required
def marques_list(request):
    # Le tenant courant est déjà activé par le middleware
    marques = VoitureMarque.objects.all().order_by("nom_marque")
    return render(request, "voiture_marque/marques_list.html", {"marques": marques})



@login_required
def toggle_favori_marque(request, id_marque):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    societe = request.societe
    marque = get_object_or_404(VoitureMarque, id_marque=id_marque)

    favori, created = MarqueFavorite.objects.get_or_create(societe=societe, marque=marque)

    if not created:
        # existait déjà → supprimer
        favori.delete()
        return JsonResponse({"status": "removed"})
    else:
        return JsonResponse({"status": "added"})






@login_required
def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(marque=marque).order_by("nom_modele")
    return render(request, "voiture_marque/modeles_par_marque.html", {"marque": marque, "modeles": modeles})
