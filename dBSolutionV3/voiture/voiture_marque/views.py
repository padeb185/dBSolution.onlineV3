from django.shortcuts import render
from .models import VoitureMarque


def marque_list(request):
    marques = VoitureMarque.objects.all()
    return render(request, "voiture_marque/marque_list.html", {
        "marques": marques
    })
