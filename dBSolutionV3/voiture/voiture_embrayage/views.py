from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_embrayage.forms import VoitureEmbrayageForm
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_embrayage.models import TypeEmbrayage
from voiture.voiture_embrayage.models import TypeVolantMoteur
from voiture.voiture_embrayage.models import TypePlateauPression
from voiture.voiture_exemplaire.models import VoitureExemplaire


@login_required
def ajouter_embrayage(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureEmbrayageForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Embrayage ajoutée avec succès !")
            else:
                # Form invalide → on retourne le formulaire avec erreurs
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureEmbrayageForm(initial={
                "voiture_marque": marque.pk,
                "voiture_modele": modele.id
            })

        return render(request, "voiture_embrayage/ajouter_embrayage_simple.html", {
            "form": form,
            "modele": modele
        })


@login_required
def liste_embrayage(request):
    """
    Affiche tous les exemplaires de véhicules avec recherche sur marque et immatriculation
    """
    tenant = request.user.societe
    with tenant_context(tenant):
        embrayages = VoitureEmbrayage.objects.all()
    return render(request, "voiture_embrayage/list.html", {"embrayages": embrayages})




@login_required
def ajouter_embrayage_simple(request):
    if request.method == "POST":
        # Récupération des valeurs
        fabricant = request.POST.get("fabricant")
        type_embrayage = request.POST.get("type_embrayage")
        volant_moteur = request.POST.get("volant_moteur")
        plateau_pression = request.POST.get("plateau_pression")
        kilometrage_embrayage = request.POST.get("kilometrage_embrayage")
        numero_embrayage = request.POST.get("numero_embrayage")

        # Vérification basique : champs obligatoires
        if not fabricant or not type_embrayage:
            messages.error(request, "Veuillez renseigner au moins le fabricant et le type d'embrayage.")
        else:
            try:
                VoitureEmbrayage.objects.create(
                    fabricant=fabricant,
                    type_embrayage=type_embrayage,
                    volant_moteur=volant_moteur,
                    plateau_pression=plateau_pression,
                    kilometrage_embrayage=kilometrage_embrayage,
                    numero_embrayage=numero_embrayage,
                )
                messages.success(request, "Embrayage ajouté avec succès !")
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {str(e)}")

    # Passer les choix au template pour les listes déroulantes
    context = {
        "TypeEmbrayage": TypeEmbrayage,
        "TypeVolantMoteur": TypeVolantMoteur,
        "TypePlateauPression": TypePlateauPression,
    }

    return render(request, "voiture_embrayage/ajouter_embrayage_simple.html", context)




@login_required
def lier_embrayage(request, embrayage_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                embrayage.voiture_exemplaire_id = cible_id
                embrayage.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                embrayage.save()
                return redirect("voiture_embrayage:list")  # ou vers la page détail

    return render(request, "voiture_embrayage/lier_embrayage.html", {
        "embrayage": embrayage,
        "exemplaires": exemplaires
    })






@login_required()
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
    return render(request, 'voiture_embrayage/embrayage_detail.html', {
        'embrayage': embrayage,
    })
