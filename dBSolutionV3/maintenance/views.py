from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from maintenance.models import Maintenance
from maintenance.models import TypeMaintenance
from django.utils.translation import gettext as _
from maintenance.utils import creer_maintenance_complete
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_exemplaire.models import TypeUtilisation
from django.utils import timezone



@login_required
def liste_maintenance_all(request):
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaires = VoitureExemplaire.objects.select_related(
            'voiture_marque', 'voiture_modele'  # Ce sont les bons noms de champs
        ).all().order_by('id')

    return render(
        request,
        'maintenance/list.html',
        {
            'exemplaires': exemplaires
        }
    )


@login_required
def detail_exemplaire_maintenance(request, exemplaire_id):
    tenant = request.user.societe
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    return render(request, "maintenance/exemplaire_detail.html", {
        "exemplaire": exemplaire,
    })

# Types possibles de maintenance
TYPES_MAINTENANCE = [
    {"code": "checkup", "nom": _("Checkup")},
    {"code": "entretien", "nom": _("Entretien")},
    {"code": "freins", "nom": _("Freins")},
    {"code": "pneus", "nom": _("Pneus")},
    {"code": "nettoyage_ext", "nom": _("Nettoyage extérieur")},
    {"code": "nettoyage_int", "nom": _("Nettoyage intérieur")},
    {"code": "niveaux", "nom": _("Niveaux")},
    {"code": "autres", "nom": _("Autres interventions")},
]

@login_required
def choisir_type_maintenance(request, exemplaire_id):

    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    if request.method == "POST":
        type_choisi = request.POST.get("type_maintenance")
        date_intervention = request.POST.get("date_intervention")
        description = request.POST.get("description", "")

        if type_choisi and date_intervention:
            Maintenance.objects.create(
                voiture_exemplaire=exemplaire,
                type_maintenance=type_choisi,
                immatriculation=exemplaire.immatriculation,
                date_intervention=date_intervention,
                description=description
            )
            # Redirige vers la liste de maintenance du modèle
            return redirect('maintenance:list', modele_id=exemplaire.voiture_modele.id)

    context = {
        "exemplaire": exemplaire,
        "types_maintenance": TYPES_MAINTENANCE
    }
    return render(request, "maintenance/choisir_type.html", context)







@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe  # ton tenant actuel

    # ⚡ Tout se passe dans le contexte du tenant
    with tenant_context(tenant):
        # Récupération de l'exemplaire uniquement dans le schema du tenant
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        mecanicien = request.user  # l'utilisateur qui crée la maintenance

        if request.method == "POST":
            # Création de la maintenance complète dans le tenant
            maintenance = creer_maintenance_complete(exemplaire, mecanicien, tenant)
            return redirect("maintenance_detail", maintenance_id=maintenance.id)

        return render(request, "maintenance/creer_maintenance.html", {
            "exemplaire": exemplaire,
            "now": timezone.now(),
        })







def creer_maintenance_complete(exemplaire, mecanicien):
    maintenance = Maintenance.objects.create(
        voiture_exemplaire=exemplaire,  # champ correct
        mecanicien=mecanicien,          # ton utilisateur responsable
        immatriculation=exemplaire.immatriculation,
        date_intervention=timezone.now().date(),
        kilometres_total=exemplaire.kilometres_total,
        kilometres_derniere_intervention=exemplaire.kilometres_derniere_intervention,
        type_maintenance="checkup",
        tag=Maintenance.Tag.JAUNE
    )
    return maintenance
