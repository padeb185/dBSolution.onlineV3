from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.utils.translation import gettext as _



@login_required
def liste_marques(request):
    societe = request.user.societe
    with tenant_context(societe):
        marques = VoitureMarque.objects.filter(societe=societe).order_by('nom_marque')
        return render(request, "voiture/marques_list.html", {'marques': marques})


@login_required
def liste_voitures_modele(request, marque_id):
    societe = request.user.societe

    with tenant_context(societe):
        marque = get_object_or_404(
            VoitureMarque,
            id=marque_id,
            societe=societe
        )

        voitures = VoitureModele.objects.filter(
            marque=marque,
            societe=societe
        )

        return render(request, "voiture/modele.html", {
            'marque': marque,
            'voitures': voitures
        })
