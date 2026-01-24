from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from django.shortcuts import render
from voiture.voiture_freins.forms import VoitureFreinsForm
from voiture.voiture_modele.models import VoitureModele
from oiture.voiture_freins.models import VoitureFreins
from voiture.voiture_exemplaire.models import VoitureExemplaire


@login_required
def ajouter_embrayage(request, modele_id):
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
                messages.success(request, "Freins ajoutée avec succès !")
                return redirect("voiture_exemplaire_liste_exemplaires", modele_id=modele.id)
            else:
                # Form invalide → on retourne le formulaire avec erreurs
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
def lier_freins(request, frein_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        frein = get_object_or_404(VoitureFreins, id=frein_id)
        exemplaires = VoitureExemplaire.objects.all().order_by("id")

        if request.method == "POST":
            cible_id = request.POST.get("cible_id")
            if cible_id:
                frein.voiture_exemplaire_id = cible_id
                frein.voiture_modele = None  # on supprime tout lien précédent avec un modèle
                frein.save()
                return redirect("voiture_freins:list")  # ou vers la page détail

    return render(request, "voiture_embrayage/lier_freins.html", {
        "frein": frein,
        "exemplaires": exemplaires
    })


@login_required
def ajouter_freins_simple(request):
    if request.method == "POST":
        VoitureFreins.objects.create(
            marque_disque_av=request.POST.get("marque_disque_av"),
            marque_plaquettes_av=request.POST.get("marque_plaquettes_av"),
            taille_disque_av=request.POST.get("taille_disque_av"),
            epaisseur_disque_av=request.POST.get("epaisseur_disque_av"),
            épaisseur_min_disque_av=request.POST.get("epaisseur_min_disque_av"),
            marque_disque_ar=request.POST.get("marque_disque_ar"),
            marque_plaquettes_ar=request.POST.get("marque_plaquettes_ar"),
            taille_disque_ar=request.POST.get("taille_disque_ar"),
            epaisseur_disque_ar=request.POST.get("epaisseur_disque_ar"),
            épaisseur_min_disque_ar=request.POST.get("epaisseur_min_disque_ar"),
        )
        return redirect("voiture_freins:list")



    return render(request, "voiture_freins/ajouter_freins_simple.html")
    })
