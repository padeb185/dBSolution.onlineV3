from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .forms import MoteurVoitureForm
from .models import MoteurVoiture



@login_required
def ajouter_moteur(request, exemplaire_id=None):

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




@login_required()
def moteur_detail_view(request, moteur_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    return render(request, 'tenant/moteur_detail.html', {
        'moteur': moteur,
    })






class MoteurListView(ListView):
    model = MoteurVoiture
    template_name = "voiture/voiture_moteur/list.html"  # <-- chemin correct
    context_object_name = "moteurs"
    paginate_by = 20  # optionnel
