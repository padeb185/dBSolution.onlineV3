from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from django.shortcuts import render
from ..voiture_freins.models import VoitureFreins
from ..voiture_exemplaire.models import VoitureExemplaire
from .forms import VoitureFreinsForm
from ..voiture_freins_ar.models import VoitureFreinsAR
from ..voiture_modele.models import VoitureModele



@login_required
def ajouter_freins_all(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureFreinsForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Freins avant ajoutés avec succès !")

            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureFreinsForm(initial={
                "voiture_marque": marque.pk,
                "voiture_modele": modele.id
            })

        return render(request, "voiture_freins/ajouter_freins_simple.html", {
            "form": form,
            "modele": modele
        })



@never_cache
@login_required
def liste_freins(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        freins = VoitureFreins.objects.all()
    return render(request, "voiture_freins/list.html", {"freins": freins})







@login_required()
def freins_detail_view(request, frein_id):
    frein = get_object_or_404(VoitureFreins, id=frein_id)
    return render(request, 'voiture_freins/freins_detail.html', {
        'frein': frein,
    })






@login_required
def ajouter_freins_simple(request):
    if request.method == "POST":

        def to_float(value):
            if not value:  # vide → None
                return None
            return float(value.replace(',', '.'))  # transforme 20,4 → 20.4

        VoitureFreins.objects.create(
            marque_disques_av=request.POST.get("marque_disques_av"),
            marque_plaquettes_av=request.POST.get("marque_plaquettes_av"),
            taille_disque_av=to_float(request.POST.get("taille_disque_av")),
            epaisseur_disque_av=to_float(request.POST.get("epaisseur_disque_av")),
            epaisseur_min_disque_av=to_float(request.POST.get("epaisseur_min_disque_av")),
        )
        messages.success(request, "Freins avant ajoutés avec succès !")


    return render(request, "voiture_freins/ajouter_freins_simple.html")
