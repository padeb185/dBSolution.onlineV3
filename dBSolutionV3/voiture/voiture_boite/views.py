from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_boite.forms import VoitureBoiteForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_boite.models import TypeBoite


@login_required
def ajouter_boite(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureBoiteForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Boite ajoutée avec succès !")
                return redirect("voiture_exemplaire_liste_exemplaires", modele_id=modele.id)
            else:
                # Form invalide → on retourne le formulaire avec erreurs
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureBoiteForm(initial={
                "voiture_marque": marque.pk,
                "voiture_modele": modele.id
            })

        return render(request, "voiture_boite/ajouter_boite_simple.html", {
            "form": form,
            "modele": modele
        })


@login_required
def liste_boite(request):
    """
    Affiche tous les exemplaires de véhicules avec recherche sur marque et immatriculation
    """
    tenant = request.user.societe
    with tenant_context(tenant):
        boites = VoitureBoite.objects.all()
        context = {"boites": boites}
    return render(request, "voiture_boite/list.html", context)




@login_required
def ajouter_boite_simple(request):
    if request.method == "POST":
        VoitureBoite.objects.create(
            fabricant=request.POST.get("fabricant"),
            nom_du_type=request.POST.get("nom_du_type"),
            type_de_boite=request.POST.get("type_de_boite"),
            nombre_rapport=request.POST.get("nombre_rapport") or 5,
            qualite_huile=request.POST.get("qualite_huile"),
            quantite_huile_l=request.POST.get("quantite_huile_l"),
        )
        messages.success(request, "Boite de vitesse ajoutée avec succès")

        return redirect("voiture_boite:ajouter_boite_simple")

    # Passer TypeBoite au template pour la liste déroulante
    context = {
        "TypeBoite": TypeBoite,
    }

    return render(request, "voiture_boite/ajouter_boite_simple.html", context)






@login_required
def boite_detail_view(request, boite_id):
    boite = get_object_or_404(VoitureBoite, id=boite_id)
    return render(request, "voiture_boite/boite_detail.html", {"boite": boite})

