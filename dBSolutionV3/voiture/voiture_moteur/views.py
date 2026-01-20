from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import MoteurVoitureForm
from .models import MoteurVoiture, TypeCarburant, TypeMoteur


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

    return render(request, "voiture_moteur/ajouter_moteur.html", {
        "form": form,
        "exemplaire": exemplaire,
        "title": _("Ajouter un moteur"),
        "submit_text": _("Créer le moteur")
    })




@login_required()
def moteur_detail_view(request, moteur_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    return render(request, 'voiture_moteur/moteur_detail.html', {
        'moteur': moteur,
    })



@login_required
def liste_moteur(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        moteurs = MoteurVoiture.objects.all()
    return render(request, "voiture_moteur/list.html", {"moteurs": moteurs})




@login_required
def ajouter_moteur_seul(request):
    if request.method == "POST":
        MoteurVoiture.objects.create(
            motoriste=request.POST.get("motoriste"),
            code_moteur=request.POST.get("code_moteur"),
            type_moteur=request.POST.get("type_moteur"),
            carburant=request.POST.get("carburant"),
            cylindree_l=request.POST.get("cylindree_l"),
            nombre_cylindres=request.POST.get("nombre_cylindres"),
        )
        return redirect("voiture_moteur:list")

    # Passer TypeEmbrayage au template pour la liste déroulante
    context = {
        "TypeMoteur": TypeMoteur,
        "TypeCarburant": TypeCarburant,

    }

    return render(request, "voiture_moteur/ajouter_moteur_seul.html", context)
