from django.shortcuts import render, get_object_or_404
from voiture.voiture_marque.models import VoitureMarque

def liste_marques(request):
    """
    Affiche la liste des marques de voiture pour le tenant courant.
    """
    marques = VoitureMarque.objects.all().order_by('nom_marque')
    return render(request, 'dbsolution/voiture_marque.html', {'marques': marques})


def liste_voitures_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id=marque_id)
    voitures = Voiture.objects.filter(marque=marque)
    return render(request, 'dbsolution/voiture_liste.html', {
        'marque': marque,
        'voitures': voitures
    })
