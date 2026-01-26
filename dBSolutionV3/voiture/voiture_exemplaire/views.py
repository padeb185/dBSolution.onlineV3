from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from .models import VoitureExemplaire
from .forms import VoitureExemplaireForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture
from django.utils.translation import gettext as _
from societe.models import Societe
from voiture.voiture_boite.models import VoitureBoite
from voiture.voiture_embrayage.models import VoitureEmbrayage
from voiture.voiture_freins.models import VoitureFreins

from ..voiture_freins_ar.models import VoitureFreinsAR


@login_required
def liste_exemplaires(request, modele_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        modele = get_object_or_404(VoitureModele, id=modele_id)
        exemplaires = VoitureExemplaire.objects.filter(voiture_modele=modele).order_by("id")

        # Décomposer l'immatriculation belge (1-ABC-234)
        for ex in exemplaires:
            immat = ex.immatriculation.replace('-', '').upper()  # enlever les tirets
            if len(immat) == 7:
                ex.chiffre = immat[0]
                ex.lettres = immat[1:4]
                ex.chiffres = immat[4:7]
            else:
                ex.chiffre = ''
                ex.lettres = ''
                ex.chiffres = ''

    return render(request, "voiture_exemplaire/liste_exemplaires.html", {
        "modele": modele,
        "exemplaires": exemplaires,
    })





@never_cache
@login_required
def voiture_exemplaire_detail(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        modele = exemplaire.voiture_modele
        marque = modele.voiture_marque

    return render(request, "voiture_exemplaire/detail_exemplaire.html", {
        "exemplaire": exemplaire,
        "modele": modele,
        "marque": marque,
    })







@login_required
def lier_boite_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    with tenant_context(request.user.societe):
        boites = VoitureBoite.objects.all().order_by('fabricant')

        if request.method == "POST":
            boite_id = request.POST.get("boite_id")
            if boite_id:
                boite = get_object_or_404(VoitureBoite, id=boite_id)
                boite.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("La boîte de vitesse a été liée à l'exemplaire avec succès."))


                return redirect("voiture_exemplaire:lier_boite_exemplaire", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner une boîte à lier."))

        return render(request, "voiture_exemplaire/lier_boite.html", {
            "exemplaire": exemplaire,
            "boites": boites,
            "title": _("Lier une boîte de vitesse à un véhicule"),
        })


@login_required
def lier_moteur_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    with tenant_context(request.user.societe):
        moteurs = MoteurVoiture.objects.all().order_by('motoriste')

        if request.method == "POST":
            moteur_id = request.POST.get("moteur_id")
            if moteur_id:
                moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
                moteur.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("Le moteur a été lié à l'exemplaire avec succès."))


                return redirect("voiture_exemplaire:lier_moteur_exemplaire", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner un moteur à lier."))

        return render(request, "voiture_exemplaire/lier_moteur.html", {
            "exemplaire": exemplaire,
            "moteurs": moteurs,
            "title": _("Lier un moteur à un véhicule"),
        })



@login_required
def lier_embrayage_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    with tenant_context(request.user.societe):
        embrayages = VoitureEmbrayage.objects.all().order_by('fabricant')

        if request.method == "POST":
            embrayage_id = request.POST.get("embrayage_id")
            if embrayage_id:
                embrayage = get_object_or_404(VoitureEmbrayage, id=embrayage_id)
                embrayage.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("L'embrayage a été lié à l'exemplaire avec succès."))


                return redirect("voiture_exemplaire:lier_embrayage_exemplaire", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner un embrayage à lier."))

        return render(request, "voiture_exemplaire/lier_embrayage.html", {
            "exemplaire": exemplaire,
            "embrayages": embrayages,
            "title": _("Lier un embrayage à un véhicule"),
        })





@login_required
def lier_freins(request, exemplaire_id):
    # Récupération de l'exemplaire
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    with tenant_context(request.user.societe):
        # Liste de tous les systèmes de freins
        freins = VoitureFreins.objects.all().order_by('taille_disque_av')

        if request.method == "POST":
            frein_id = request.POST.get("frein_id")
            if frein_id:
                frein = get_object_or_404(VoitureFreins, id=frein_id)
                # Lier le frein à l'exemplaire
                frein.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("Le système de freinage a été lié à l'exemplaire avec succès."))

                # Redirection vers la page de détail de l'exemplaire (ou une page liste)
                return redirect("voiture_exemplaire:lier_frein", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner un système de freinage à lier."))

        return render(request, "voiture_exemplaire/lier_frein.html", {
            "exemplaire": exemplaire,
            "freins": freins,
            "title": _("Lier un système de freinage à un véhicule"),
        })



@login_required
def lier_frein_ar(request, exemplaire_id):
    # Récupération de l'exemplaire
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    with tenant_context(request.user.societe):
        # Liste de tous les systèmes de freins
        freins_ar = VoitureFreinsAR.objects.all().order_by('taille_disque_ar')

        if request.method == "POST":
            frein_ar_id = request.POST.get("frein_ar_id")
            if frein_ar_id:
                frein_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)
                # Lier le frein à l'exemplaire
                frein_ar.voitures_exemplaires.add(exemplaire)
                messages.success(request, _("Le système de freinage a été lié à l'exemplaire avec succès."))

                # Redirection vers la page de détail de l'exemplaire (ou une page liste)
                return redirect("voiture_exemplaire:lier_frein_ar", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner un système de freinage à lier."))

        return render(request, "voiture_exemplaire/lier_frein_ar.html", {
            "exemplaire": exemplaire,
            "freins_ar": freins_ar,
            "title": _("Lier un système de freinage arrière à un véhicule"),
        })







@login_required
def moteur_autocomplete(request):

    code = request.GET.get("code_moteur")
    motoriste = request.GET.get("motoriste")

    if not code or not motoriste:
        return JsonResponse({"error": _("Paramètres manquants")}, status=400)


    moteur = MoteurVoiture.objects.filter(code_moteur=code, motoriste=motoriste).first()
    if not moteur:
        return JsonResponse({"error": _("Moteur non trouvé")}, status=404)

    # Retourne les champs à remplir
    data = {
        "type_moteur": moteur.type_moteur,
        "carburant": moteur.carburant,
        "cylindree_l": moteur.cylindree_l,
        "distribution": moteur.distribution,
        "nombre_cylindres": moteur.nombre_cylindres,
        "puissance_ch": moteur.puissance_ch,
        "puissance_tr_min": moteur.puissance_tr_min,
        "couple_nm": moteur.couple_nm,
        "couple_tr_min": moteur.couple_tr_min,
        "qualite_huile": moteur.qualite_huile,
        "quantite_huile_l": moteur.quantite_huile_l,
        "intervalle_km_entretien": moteur.intervalle_km_entretien,
    }

    return JsonResponse(data)





def modifier_exemplaire(request, exemplaire_id):
    # Récupérer le tenant courant depuis request (ou via ton contexte multi-tenant)
    tenant = request.user.societe  # Remplacer par logique réelle si nécessaire
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        if request.method == "POST":
            form = VoitureExemplaireForm(request.POST, instance=exemplaire)
            if form.is_valid():
                form.save()
                messages.success(request, "Exemplaire mis à jour avec succès.")
                return redirect('voiture_exemplaire:voiture_exemplaire_detail', exemplaire_id=exemplaire.id)
        else:
            form = VoitureExemplaireForm(instance=exemplaire)

        return render(request, 'voiture_exemplaire/modifier_exemplaire.html', {
            'form': form,
            'exemplaire': exemplaire,
        })



@login_required
def liste_exemplaires_all(request):
    """
    Affiche tous les exemplaires de véhicules avec recherche sur marque et immatriculation
    """
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaires = VoitureExemplaire.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'voiture_exemplaire/list.html',
        {
            'exemplaires': exemplaires
        }
    )



@login_required
def ajouter_exemplaire_all(request, modele_id):
    modele = get_object_or_404(VoitureModele, id=modele_id)

    if request.method == "POST":
        VoitureExemplaire.objects.create(
            voiture_marque=modele.voiture_marque,   # marque depuis le modèle
            voiture_modele=modele,                  # lien vers le modèle
            immatriculation=request.POST.get("immatriculation"),
            pays=request.POST.get("pays"),
            numero_vin=request.POST.get("numero_vin"),
            kilometres_chassis=request.POST.get("kilometres_chassis"),
            annee_production=request.POST.get("annee_production"),
            mois_production=request.POST.get("mois_production"),
        )
        return redirect("voiture_exemplaire:voiture_exemplaire", modele_id=modele.id)


    return render(
        request,
        "voiture_exemplaire/ajouter_exemplaire_all.html",
        {"modele": modele}
    )




