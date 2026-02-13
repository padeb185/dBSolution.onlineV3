from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import  redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django_tenants.utils import tenant_context
from .models import VoitureExemplaire, TypeUtilisation
from .forms import VoitureExemplaireForm
from ..voiture_modele.models import VoitureModele
from ..voiture_moteur.models import MoteurVoiture
from django.utils.translation import gettext as _
from societe.models import Societe
from ..voiture_boite.models import VoitureBoite
from ..voiture_embrayage.models import VoitureEmbrayage
from ..voiture_freins.models import VoitureFreins
from ..voiture_freins_ar.models import VoitureFreinsAR
from ..voiture_pneus.models import VoiturePneus


@never_cache
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
                messages.success(request, _(f"La boîte de vitesse a été liée au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation}' avec succès."))


                return redirect("voiture_exemplaire:lier_boite_exemplaire", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner une boîte à lier."))

        return render(request, "voiture_exemplaire/lier_boite.html", {
            "exemplaire": exemplaire,
            "boites": boites,
            "title": _("Lier une boîte de vitesse à un véhicule"),
        })



@login_required
def lier_pneus(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    with tenant_context(request.user.societe):
        pneus = VoiturePneus.objects.all().order_by('manufacturier')

        if request.method == "POST":
            pneu_id = request.POST.get("pneu_id")
            if pneu_id:
                pneu = get_object_or_404(VoiturePneus, id=pneu_id)  # ← corrigé ici
                pneu.voitures_exemplaires.add(exemplaire)
                messages.success(request, _(f"Les pneus ont été liés au véhivule '{exemplaire.voiture_marque}  {exemplaire.immatriculation}'  avec succès."))
                return redirect("voiture_exemplaire:lier_pneus", exemplaire_id=exemplaire.id)
            else:
                messages.error(request, _("Veuillez sélectionner des pneus à lier."))

        return render(request, "voiture_exemplaire/lier_pneus.html", {
            "exemplaire": exemplaire,
            "pneus": pneus,
            "title": _("Lier des pneus à un véhicule"),
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
                messages.success(request, _(f"Le moteur a été lié au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation }' avec succès."))


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
                messages.success(request, _(f"L'embrayage a été lié au véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation }' avec succès."))


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
            marque_disques_av = request.POST.get("marque_disques_av")
            marque_plaquettes_av = request.POST.get("marque_plaquettes_av")

            if frein_id:
                frein = get_object_or_404(VoitureFreins, id=frein_id)

                if frein_id:
                    frein_ar = get_object_or_404(VoitureFreinsAR, id=frein_id)

                    if marque_disques_av:
                        frein_ar.marque_disques_av = marque_disques_av
                    if marque_plaquettes_av:
                        frein_ar.marque_plaquettes_av = marque_plaquettes_av
                    frein_ar.save()

                # Lier le frein à l'exemplaire
                frein.voitures_exemplaires.add(exemplaire)

                messages.success(request, _(f"Le système de freinage avant a été lié au véhicule '{exemplaire.voiture_marque} {exemplaire.immatriculation}' avec succès."))

                # Redirection vers la page de liaison
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
        marque_disques_ar = request.POST.get("marque_disques_ar")
        marque_plaquettes_ar = request.POST.get("marque_plaquettes_ar")

        if request.method == "POST":
            frein_ar_id = request.POST.get("frein_ar_id")
            if frein_ar_id:
                frein_ar = get_object_or_404(VoitureFreinsAR, id=frein_ar_id)

                if marque_disques_ar:
                    frein_ar.marque_disques_av = marque_disques_ar
                if marque_plaquettes_ar:
                    frein_ar.marque_plaquettes_av = marque_plaquettes_ar
                frein_ar.save()

                # Lier le frein à l'exemplaire
                frein_ar.voitures_exemplaires.add(exemplaire)
                messages.success(request, _(f"Le système de freinage arrière a été lié au véhicule '{exemplaire.voiture_marque}  { exemplaire.immatriculation }' avec succès."))

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



@login_required
def modifier_exemplaire(request, exemplaire_id):
    # Récupérer le tenant courant depuis request
    tenant = request.user.societe  # Ajuster selon ton contexte
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        if request.method == "POST":
            form = VoitureExemplaireForm(request.POST, instance=exemplaire)
            if form.is_valid():
                form.save()

                messages.success(request, _(f"Véhicule '{exemplaire.voiture_marque} { exemplaire.immatriculation }' mis à jour avec succès."))

        else:
            form = VoitureExemplaireForm(instance=exemplaire)

        return render(request, 'voiture_exemplaire/modifier_exemplaire.html', {
            'form': form,
            'exemplaire': exemplaire,
        })

@never_cache
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
        form = VoitureExemplaireForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)

            # Calcul automatique de l'année de production à partir du VIN
            vin = form.cleaned_data.get("numero_vin", "")
            annee_calculee = None
            if vin and len(vin) >= 10:
                code = vin[9].upper()
                VIN_YEAR_BASE = {
                    "A": 1980, "B": 1981, "C": 1982, "D": 1983, "E": 1984, "F": 1985, "G": 1986, "H": 1987,
                    "J": 1988, "K": 1989, "L": 1990, "M": 1991, "N": 1992, "P": 1993, "R": 1994, "S": 1995,
                    "T": 1996, "V": 1997, "W": 1998, "X": 1999, "Y": 2000,
                    "1": 2001, "2": 2002, "3": 2003, "4": 2004, "5": 2005, "6": 2006, "7": 2007, "8": 2008, "9": 2009
                }
                if code in VIN_YEAR_BASE:
                    annee_calculee = VIN_YEAR_BASE[code]  # pas de +30
                instance.annee_production = annee_calculee # ta logique existante


            # Déterminer automatiquement si le véhicule est avant 2010
            instance.est_avant_2010 = annee_calculee is not None and annee_calculee < 2010

            instance.modele = modele
            instance.save()
            messages.success(request, "Véhicule ajouté avec succès !")
        else:
            messages.error(request, "Merci de corriger les erreurs ci-dessous.")
    else:
        form = VoitureExemplaireForm()

    return render(request, "voiture_exemplaire/ajouter_exemplaire_all.html", {
        "modele": modele,
        "form": form,
    })