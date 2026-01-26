from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from .forms import VoitureFreinsARForm
from ..voiture_modele.models import VoitureModele
from ..voiture_exemplaire.models import VoitureExemplaire
from ..voiture_freins_ar.models import VoitureFreinsAR




@login_required
def ajouter_freins_ar(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureFreinsARForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Freins arrière ajouté avec succès !")
                return redirect("voiture_exemplaire_liste_exemplaires", modele_id=modele.id)
            else:
                # Form invalide → on retourne le formulaire avec erreurs
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureFreinsARForm(initial={
                "voiture_marque": marque.pk,
                "voiture_modele": modele.id
            })

        return render(request, "voiture_freins_ar/ajouter_freins_ar_simple.html", {
            "form": form,
            "modele": modele
        })

# Create your views here.
@login_required
def lier_freins_arriere(request, frein_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        frein = get_object_or_404(VoitureFreinsAR, id=frein_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                frein.voiture_exemplaire_id = cible_id
                frein.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                frein.save()
                return redirect("voiture_freins_ar:list_ar")  # ou vers la page détail

    return render(request, "voiture_freins_ar/lier_freins_ar.html", {
        "frein": frein,
        "exemplaires": exemplaires
    })



@login_required
def ajouter_freins_ar_simple(request):
    if request.method == "POST":

        # Fonction utilitaire pour convertir en float ou None
        def to_float(value):
            if not value:  # vide → None
                return None
            return float(value.replace(',', '.'))  # transforme 20,4 → 20.4

        VoitureFreinsAR.objects.create(
            marque_disques_ar=request.POST.get("marque_disques_ar"),
            marque_plaquettes_ar=request.POST.get("marque_plaquettes_ar"),
            taille_disque_ar=to_float(request.POST.get("taille_disque_ar")),
            epaisseur_disque_ar=to_float(request.POST.get("epaisseur_disque_ar")),
            epaisseur_min_disque_ar=to_float(request.POST.get("epaisseur_min_disque_ar")),
        )
        return redirect("voiture_freins_ar:list_ar")

    return render(request, "voiture_freins_ar/ajouter_freins_ar_simple.html")




@login_required()
def freins_ar_detail_view(request, frein_id):
    frein = get_object_or_404(VoitureFreinsAR, id=frein_id)
    return render(request, 'voiture_freins_ar/freins_ar_detail.html', {
        'frein': frein,
    })



@login_required
def liste_freins_ar(request):

    tenant = request.user.societe
    with tenant_context(tenant):
        freins_ar = VoitureFreinsAR.objects.all()
    return render(request, "voiture_freins_ar/list_ar.html", {"freins_ar": freins_ar})
