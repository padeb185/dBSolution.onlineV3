from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from .forms import VoitureFreinsARForm
from ..voiture_modele.models import VoitureModele
from ..voiture_freins_ar.models import VoitureFreinsAR
from societe.models import Societe
from django.utils.translation import gettext_lazy as _



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


@login_required
def ajouter_freins_ar_simple(request):
    tenant = request.user.societe
    with tenant_context(tenant):
        if request.method == "POST":

            # Fonction utilitaire pour convertir en float ou None
            def to_float(value):
                if not value:  # vide → None
                    return None
                return float(value.replace(',', '.'))  # transforme 20,4 → 20.4

            VoitureFreinsAR.objects.create(
                societe=tenant,
                marque_disques_ar=request.POST.get("marque_disques_ar"),
                numero_oem_disques_ar=request.POST.get("numero_oem_disques_ar"),
                marque_plaquettes_ar=request.POST.get("marque_plaquettes_ar"),
                numero_oem_plaquettes_ar=request.POST.get("numero_oem_plaquettes_ar"),
                taille_disque_ar=to_float(request.POST.get("taille_disque_ar")),
                epaisseur_disque_ar=to_float(request.POST.get("epaisseur_disque_ar")),
                epaisseur_min_disque_ar=to_float(request.POST.get("epaisseur_min_disque_ar")),

            )
            messages.success(request, "Freins arrière ajouté avec succès !")


        return render(request, "voiture_freins_ar/ajouter_freins_ar_simple.html")




@never_cache
@login_required
def freins_ar_detail_view(request, frein_ar_id):
    frein = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)
    return render(request, 'voiture_freins_ar/freins_ar_detail.html', {
        'frein': frein,
    })




@never_cache
@login_required
def liste_freins_ar(request, societe_id=None):
    societe = request.user.societe
    if societe_id:
        societe = Societe.objects.get(id=societe_id)

    with tenant_context(societe):
        freins_ar = VoitureFreinsAR.objects.filter(societe=societe)
        return render(request, "voiture_freins_ar/freins_ar_list.html", {"freins_ar": freins_ar})



@login_required
def modifier_freins_ar_view(request, frein_ar_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        freins_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)

        if request.method == "POST":
            form_frein = VoitureFreinsARForm(request.POST, instance=freins_ar)
            if form_frein.is_valid():
                form_frein.save()
                messages.success(request, _("Freins arrière mis à jour avec succès."))

            else:
                messages.error(request, _("Le formulaire contient des erreurs."))
        else:
            form_frein = VoitureFreinsARForm(instance=freins_ar)

    return render(
        request,
        "voiture_freins_ar/modifier_freins_ar.html",
        {
            "form": form_frein,
            "frein": freins_ar,
        }
    )