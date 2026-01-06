from django.shortcuts import get_object_or_404, render
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(voiture_marque=marque).order_by('nom_modele')
    context = {
        'marque': marque,
        'modeles': modeles,
    }
    return render(request, 'voiture/modeles_list.html', context)