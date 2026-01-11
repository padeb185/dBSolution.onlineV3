from django.shortcuts import render
from voiture.voiture_moteur.models import MoteurVoiture

def moteur_view(request):
    total_moteurs = MoteurVoiture.objects.count()
    moteurs = MoteurVoiture.objects.all()
    return render(request, 'tenant/moteurs_list.html', {
        'total_moteurs': total_moteurs,
        'moteurs': moteurs,
    })
