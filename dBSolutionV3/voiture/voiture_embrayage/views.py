from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_embrayage.forms import VoitureEmbrayageForm
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_modele.models import VoitureModele




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
                return redirect("voiture_exemplaire_liste_exemplaires", modele_id=modele.id)
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
        embrayage = VoitureEmbrayage.objects.all()
    return render(request, "voiture_embrayage/list.html", {"embrayage": embrayage})


@login_required
def ajouter_embrayage_simple(request):
    if request.method == "POST":
        VoitureEmbrayage.objects.create(
            fabricant=request.POST.get("fabricant"),
            type_embrayage=request.POST.get("type_embrayage"),
            kilometrage_embrayage=request.POST.get("kilometrage_embrayage"),
            numero_embrayage=request.POST.get("numero_embrayage"),

        )
        return redirect("voiture_embrayage:list")

    return render(request, "voiture_embrayage/ajouter_embrayage_simple.html")


@login_required()
def lier_embrayage(request, embrayage_id):
    embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)

    if request.method == "POST":
        type_liaison = request.POST.get("type_liaison")
        cible_id = request.POST.get("cible_id")

        if type_liaison == "modele":
            embrayage.voiture_modele_id = cible_id
            embrayage.voiture_exemplaire = None
        else:
            embrayage.voiture_exemplaire_id = cible_id
            embrayage.voiture_modele = None

        embrayage.save()
        return redirect("voiture_embrayage:list")

    return render(request, "voiture_embrayage/lier_embrayage.html", {"embrayage": embrayage})


@login_required()
def embrayage_detail_view(request, embrayage_id):
    embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
    return render(request, 'voiture_embrayage/embrayage_detail.html', {
        'embrayage': embrayage,
    })
