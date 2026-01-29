from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele
from maintenance.models import Maintenance
from maintenance.models import TypeMaintenance
from django.utils.translation import gettext as _

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