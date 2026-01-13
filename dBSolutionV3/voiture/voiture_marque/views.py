from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


@login_required
def marques_list(request):
    # Le tenant courant est déjà activé par le middleware
    marques = VoitureMarque.objects.all().order_by("nom_marque")
    favoris = []  # ou ton queryset de favoris
    return render(request, "voiture_marque/marques_list.html", {
        "marques": marques,
        "favoris": favoris,
    })


@login_required
def modeles_par_marque(request, marque_id):
    marque = get_object_or_404(VoitureMarque, id_marque=marque_id)
    modeles = VoitureModele.objects.filter(
        voiture_marque=marque
    ).order_by("nom_modele")
    return render(request, "voiture_modele/modeles_par_marque.html", {
        "marque": marque,
        "modeles": modeles,
    })
