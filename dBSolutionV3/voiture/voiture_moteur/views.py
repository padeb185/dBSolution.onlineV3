from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .forms import MoteurVoitureForm

@login_required
def ajouter_moteur(request, exemplaire_id=None):
    """
    Création d'un moteur. Optionnellement lié à un exemplaire si exemplaire_id fourni.
    """
    exemplaire = None
    if exemplaire_id:
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        form = MoteurVoitureForm(request.POST)
        if form.is_valid():
            moteur = form.save()
            if exemplaire:
                moteur.voitures_exemplaires.add(exemplaire)
            return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)
    else:
        form = MoteurVoitureForm()

    return render(request, "voiture/voiture_moteur/ajouter_moteur.html", {
        "form": form,
        "exemplaire": exemplaire,
        "title": _("Ajouter un moteur"),
        "submit_text": _("Créer le moteur")
    })

