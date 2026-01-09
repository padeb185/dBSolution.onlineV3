from django.shortcuts import render, get_object_or_404
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import VoitureExemplaire
from .forms import VoitureExemplaireForm
from ..voiture_modele.models import VoitureModele


@login_required
def voiture_exemplaire(request, modele_id):

    modele = get_object_or_404(VoitureModele, id=modele_id)
    exemplaires = VoitureExemplaire.objects.filter(voiture_modele=modele)

    context = {
        "modele": modele,
        "exemplaires": exemplaires,
    }
    return render(request, "voiture_exemplaire/voiture_exemplaire.html", context)






@login_required
def ajouter_exemplaire(request, modele_id):
    modele = get_object_or_404(VoitureModele, id=modele_id)
    marque = modele.voiture_marque

    if request.method == "POST":
        form = VoitureExemplaireForm(request.POST)
        if form.is_valid():
            exemplaire = form.save(commit=False)
            exemplaire.voiture_modele = modele
            exemplaire.voiture_marque = marque
            exemplaire.save()
            messages.success(request, "Exemplaire ajouté avec succès !")
            return redirect("liste_exemplaires_modele", modele_id=modele.id)
    else:
        form = VoitureExemplaireForm()

    return render(request, "voiture/ajouter_exemplaire.html", {
        "form": form,
        "modele": modele
    })
