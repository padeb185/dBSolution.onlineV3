from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_boite.forms import VoitureBoiteForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_boite.models import VoitureBoite



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

        return render(request, "voiture_boite/ajouter_boite.html", {
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
        exemplaires = VoitureBoite.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'voiture_boite/list.html',
        {
            'exemplaires': exemplaires
        }
    )
