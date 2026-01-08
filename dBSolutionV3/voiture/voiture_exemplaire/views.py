from django.shortcuts import render, get_object_or_404
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_exemplaire.models import VoitureExemplaire

def voiture_exemplaire(request, modele_id):
    """
    Affiche tous les exemplaires d'un modèle donné.
    Si aucun exemplaire n'existe, le template affichera un message.
    """
    modele = get_object_or_404(VoitureModele, id=modele_id)
    exemplaires = VoitureExemplaire.objects.filter(voiture_modele=modele)

    context = {
        "modele": modele,
        "exemplaires": exemplaires,
    }
    return render(request, "voiture_exemplaire/voiture_exemplaire.html", context)
