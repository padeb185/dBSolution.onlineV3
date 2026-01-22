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
from voiture.voiture_boite.models import VoitureBoite


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
def lier_moteur_exemplaire_from_detail(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        if request.method == "POST":
            motoriste = request.POST.get("motoriste")
            cylindree = request.POST.get("cylindree_l")
            code = request.POST.get("code_moteur")
            moteur = MoteurVoiture.objects.filter(code_moteur=code, motoriste=motoriste, cylindree_l=cylindree).first()
            if moteur:
                moteur.voitures_exemplaires.add(exemplaire)
                return redirect("voiture_exemplaire:detail_exemplaire", exemplaire_id=exemplaire.id)
            else:
                return render(request, "voiture_exemplaire/detail_exemplaire.html", {
                    "exemplaire": exemplaire,
                    "error": _("Moteur non trouvé")
                })





@login_required
def lier_boite_exemplaire_from_detail(request, exemplaire_id):
    """
    Permet de lier une boîte de vitesse existante à un exemplaire.
    """
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        if request.method == "POST":
            fabricant = request.POST.get("fabricant", "").strip()
            nom_du_type = request.POST.get("nom_du_type", "").strip()

            if not fabricant or not nom_du_type:
                messages.error(request, "Veuillez sélectionner un fabricant et une boîte valide.")
                return redirect("voiture_exemplaire:detail_exemplaire", exemplaire_id=exemplaire.id)

            # Cherche la boîte correspondante
            boite = VoitureBoite.objects.filter(fabricant__iexact=fabricant, nom_du_type__iexact=nom_du_type).first()
            if boite:
                # Lier l'exemplaire à la boîte
                boite.voitures_exemplaires.add(exemplaire)
                messages.success(request, f"La boîte '{boite.nom_du_type}' a été liée avec succès.")
            else:
                messages.error(request, "Aucune boîte correspondante trouvée pour ce fabricant et ce type.")

        return redirect("voiture_exemplaire:detail_exemplaire", exemplaire_id=exemplaire.id)



@login_required
def get_cylindrees(request):
    motoriste = request.GET.get("motoriste")
    tenant = request.user.societe
    with tenant_context(tenant):
        cylindrees = MoteurVoiture.objects.filter(motoriste=motoriste).values_list("cylindree_l", flat=True).distinct()
        return JsonResponse(list(cylindrees), safe=False)

@login_required
def get_type_de_boite(request):
    fabricant = request.GET.get("fabricant", "").strip()
    tenant = request.user.societe

    with tenant_context(tenant):
        types = (
            VoitureBoite.objects
            .filter(fabricant__iexact=fabricant)
            .values_list("type_de_boite", flat=True)
            .distinct()
        )

    return JsonResponse(list(types), safe=False)


@login_required
def get_code_moteur(request):
    motoriste = request.GET.get("motoriste")
    cylindree = request.GET.get("cylindree")
    tenant = request.user.societe
    with tenant_context(tenant):
        moteur = MoteurVoiture.objects.filter(motoriste=motoriste, cylindree_l=cylindree).first()
        return JsonResponse({"code_moteur": moteur.code_moteur if moteur else ""})








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
def lier_boite_exemplaire(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    boites = VoitureBoite.objects.all()  # Tu peux filtrer selon fabricant si tu veux

    if request.method == "POST":
        boite_id = request.POST.get("boite_id")
        if boite_id:
            boite = get_object_or_404(VoitureBoite, id=boite_id)
            boite.voitures_exemplaires.add(exemplaire)
            messages.success(request, _("La boîte de vitesse a été liée à l'exemplaire avec succès."))

            # 🔹 Correct redirect vers la même page pour voir le message
            return redirect("voiture_exemplaire:lier_boite_exemplaire", exemplaire_id=exemplaire.id)
        else:
            messages.error(request, _("Veuillez sélectionner une boîte à lier."))

    return render(request, "voiture_exemplaire/lier_boite.html", {
        "exemplaire": exemplaire,
        "boites": boites,
        "title": _("Lier une boîte de vitesse à un véhicule"),
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




def exemplaire_detail(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    moteurs = MoteurVoiture.objects.filter(voitures_exemplaires=exemplaire)
    boites = VoitureBoite.objects.filter(voitures_exemplaires=exemplaire)

    context = {
        "exemplaire": exemplaire,
        "moteurs": moteurs,
    }
    return render(request, "exemplaire_detail.html", context)
