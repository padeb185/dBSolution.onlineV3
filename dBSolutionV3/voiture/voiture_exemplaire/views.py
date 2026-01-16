from django import forms
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_tenants.utils import tenant_context
from .models import VoitureExemplaire
from .forms import VoitureExemplaireForm
from voiture.voiture_modele.models import VoitureModele
from voiture.voiture_moteur.models import MoteurVoiture
from django.utils.translation import gettext as _
from societe.models import Societe



@login_required
def liste_exemplaires(request, modele_id):
    tenant = request.user.societe  # ton tenant
    with tenant_context(tenant):
        modele = get_object_or_404(VoitureModele, id=modele_id)
        exemplaires = VoitureExemplaire.objects.filter(voiture_modele=modele).order_by("id")

    return render(request, "voiture_exemplaire/liste_exemplaires.html", {
        "modele": modele,
        "exemplaires": exemplaires,
    })






@login_required
def voiture_exemplaire_detail(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    return render(request, "voiture_exemplaire/detail_exemplaire.html", {
        "exemplaire": exemplaire
    })




@login_required
def ajouter_exemplaire(request, modele_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        # Récupère le modèle
        modele = get_object_or_404(VoitureModele, id=modele_id)
        marque = modele.voiture_marque  # objet VoitureMarque

        if request.method == "POST":
            form = VoitureExemplaireForm(request.POST)
            if form.is_valid():
                exemplaire = form.save(commit=False)
                exemplaire.voiture_modele = modele
                exemplaire.voiture_marque = marque
                exemplaire.save()
                messages.success(request, "Exemplaire ajouté avec succès !")
                return redirect("liste_exemplaires_modele", modele_id=modele.id)
            else:
                # Form invalide → on retourne le formulaire avec erreurs
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            # GET → formulaire pré-rempli avec la marque et le modèle
            form = VoitureExemplaireForm(initial={
                "voiture_marque": marque.id_marque,  # ⚠ id_marque et pas id
                "voiture_modele": modele.id
            })

        # Retourne toujours le template avec le formulaire
        return render(request, "voiture_exemplaire/ajouter_exemplaire.html", {
            "form": form,
            "modele": modele,
            "marque": marque
        })


@login_required
def lier_moteur_exemplaire_from_detail(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        if request.method == "POST":
            code = request.POST.get("code_moteur")
            motoriste = request.POST.get("motoriste")
            moteur = MoteurVoiture.objects.filter(code_moteur=code, motoriste=motoriste).first()
            if moteur:
                moteur.voitures_exemplaires.add(exemplaire)
                return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)
            else:
                return render(request, "voiture_exemplaire/voiture_exemplaire_detail.html", {
                    "exemplaire": exemplaire,
                    "error": _("Moteur non trouvé")
                })


@login_required
def lier_moteur_exemplaire(request, moteur_id, exemplaire_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        moteur.voitures_exemplaires.add(exemplaire)

        messages.success(request, _("Le moteur a été lié à l'exemplaire avec succès."))
        return redirect("detail_exemplaire", id=exemplaire.id)

    return render(request, "voiture_exemplaire/liers_moteur.html", {
        "moteur": moteur,
        "exemplaire": exemplaire,
        "title": _("Lier un moteur à un véhicule"),
        "confirm_text": _("Voulez-vous lier ce moteur à ce véhicule ?"),
        "submit_text": _("Lier le moteur"),
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