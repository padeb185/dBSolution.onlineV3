from django.shortcuts import render
from voiture.voiture_moteur.models import MoteurVoiture
from voiture.voiture_marque.models import VoitureMarque


def moteur_view(request):
    total_moteurs = MoteurVoiture.objects.count()
    moteurs = MoteurVoiture.objects.all()

    total_marques = VoitureMarque.objects.count()
    marques = VoitureMarque.objects.all()
    return render(request, 'tenant/moteurs_list.html', {
        'total_moteurs': total_moteurs,
        'moteurs': moteurs,
        'total_marques': total_marques,
        'marques': marques,
    })
