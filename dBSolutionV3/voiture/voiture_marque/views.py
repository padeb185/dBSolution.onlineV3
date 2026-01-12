from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import VoitureMarque, MarqueFavorite
from voiture.voiture_modele.models import VoitureModele



@login_required
def marque_list(request):
    """
    Affiche la liste des marques de voiture.
    """
    # Récupérer toutes les marques
    marques = VoitureMarque.objects.all()

    # Renvoyer au template avec le contexte
    return render(
        request,
        "voiture/marques.html",  # Assure-toi que le chemin est correct
        {
            "marques": marques,
        }
    )











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





def modeles_par_marque(request, marque_id):
    """
    Affiche la liste des modèles d'une marque spécifique.
    """
    # Récupérer la marque ou renvoyer 404 si inexistant
    marque = get_object_or_404(VoitureMarque, id=marque_id)

    # Récupérer tous les modèles liés à cette marque
    modeles = VoitureModele.objects.filter(marque=marque).order_by('nom')

    context = {
        'marque': marque,
        'modeles': modeles,
    }

    return render(request, 'voiture/voiture_marque/modeles_par_marque.html', context)
