from django.shortcuts import render, get_object_or_404
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


def liste_marques(request):
    """
    Affiche la liste des marques de voiture pour le tenant courant.
    """
    marques = VoitureMarque.objects.all().order_by('nom_marque')
    return render(request, "voiture/marques.html", {'marques': marques})


def liste_voitures_modele(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id=marque_id)
    voitures = VoitureModele.objects.filter(marque=marque)
    return render(request, "voiture/modele.html", {
        'marque': marque,
        'voitures': voitures
    })

