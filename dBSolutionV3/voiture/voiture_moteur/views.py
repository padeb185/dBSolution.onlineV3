from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .forms import MoteurVoitureForm

class AjouterMoteurView(View):
    def get(self, request, exemplaire_id):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        form = MoteurVoitureForm()
        return render(request, "ajouter_moteur.html", {"form": form, "exemplaire": exemplaire})

    def post(self, request, exemplaire_id):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
        form = MoteurVoitureForm(request.POST)
        if form.is_valid():
            moteur = form.save(commit=False)
            moteur.voiture_exemplaire = exemplaire
            moteur.save()
            return redirect('voiture_exemplaire:voiture_exemplaire_detail', exemplaire.id)
        return render(request, "ajouter_moteur.html", {"form": form, "exemplaire": exemplaire})
