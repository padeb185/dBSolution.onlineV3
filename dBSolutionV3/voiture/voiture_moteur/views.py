from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from .forms import MoteurVoitureForm
from .models import MoteurVoiture, TypeCarburant, TypeMoteur, TypeDistribution
from django.contrib import messages
from django.views.decorators.cache import never_cache

@login_required
def ajouter_moteur(request, exemplaire_id=None):

    exemplaire = None
    if exemplaire_id:
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        form = MoteurVoitureForm(request.POST)
        if form.is_valid():
            moteur = form.save()
            if exemplaire:
                moteur.voitures_exemplaires.add(exemplaire)
            return redirect("voiture_exemplaire:voiture_exemplaire_detail", exemplaire_id=exemplaire.id)
    else:
        form = MoteurVoitureForm()

    return render(request, "voiture_moteur/ajouter_moteur.html", {
        "form": form,
        "exemplaire": exemplaire,
        "title": _("Ajouter un moteur"),
        "submit_text": _("Créer le moteur")
    })




@login_required()
def moteur_detail_view(request, moteur_id):
    moteur = get_object_or_404(MoteurVoiture, id=moteur_id)
    return render(request, 'voiture_moteur/moteur_detail.html', {
        'moteur': moteur,
    })


@never_cache
@login_required
def liste_moteur(request):
    tenant = request.user.societe  # récupérer le tenant
    with tenant_context(tenant):
        moteurs = MoteurVoiture.objects.all()  # tous les moteurs du tenant
        context = {"moteurs": moteurs}
        return render(request, "voiture_moteur/list.html", context)



@login_required
def ajouter_moteur_seul(request):
    if request.method == "POST":
        # Récupérer et nettoyer les valeurs POST
        motoriste = request.POST.get("motoriste", "").strip()
        code_moteur = request.POST.get("code_moteur", "").strip()
        type_moteur = request.POST.get("type_moteur", "").strip()
        carburant = request.POST.get("carburant", "").strip()
        distribution = request.POST.get("distribution", "").strip()
        qualite_huile = request.POST.get("qualite_huile", "").strip()

        # Récupérer les champs numériques et convertir
        def to_int(val):
            try: return int(val)
            except (ValueError, TypeError): return 0

        def to_float(val):
            try: return float(val)
            except (ValueError, TypeError): return 0.0

        cylindree_l = to_float(request.POST.get("cylindree_l"))
        nombre_cylindres = to_int(request.POST.get("nombre_cylindres"))
        puissance_ch = to_int(request.POST.get("puissance_ch"))
        puissance_tr_min = to_int(request.POST.get("puissance_tr_min"))
        couple_nm = to_int(request.POST.get("couple_nm"))
        couple_tr_min = to_int(request.POST.get("couple_tr_min"))
        quantite_huile_l = to_float(request.POST.get("quantite_huile_l"))
        intervalle_km_entretien = to_int(request.POST.get("intervalle_km_entretien"))

        # Créer le moteur avec les valeurs correctement converties
        MoteurVoiture.objects.create(
            motoriste=motoriste,
            code_moteur=code_moteur,
            type_moteur=type_moteur,
            carburant=carburant,
            cylindree_l=cylindree_l,
            distribution=distribution,
            puissance_ch=puissance_ch,
            puissance_tr_min=puissance_tr_min,
            couple_nm=couple_nm,
            couple_tr_min=couple_tr_min,
            nombre_cylindres=nombre_cylindres,
            qualite_huile=qualite_huile,
            quantite_huile_l=quantite_huile_l,
            intervalle_km_entretien=intervalle_km_entretien
        )

        messages.success(request, "Moteur ajouté avec succès !")



    context = {
        "TypeMoteur": TypeMoteur,
        "TypeCarburant": TypeCarburant,
        "TypeDistribution": TypeDistribution,

    }
    return render(request, "voiture_moteur/ajouter_moteur_seul.html", context)
