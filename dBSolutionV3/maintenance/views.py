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
from maintenance.check_up.views import TYPES_MAINTENANCE
from maintenance.check_up.views import creer_checkup_complet
from maintenance.check_up.models import Checkup


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


"""

@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe

    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # Vérifie que le client appartient au tenant courant
        if exemplaire.client.societe_id != tenant.id:
            return render(request, "403.html", status=403)

        if request.method == "POST":
            maintenance = creer_checkup_complet(
                exemplaire=exemplaire,
                mecanicien=request.user,
                tenant=tenant,
                request=request
            )

            # Met à jour le dernier utilisateur ayant fait la maintenance
            exemplaire.last_maintained_by = request.user
            exemplaire.save(update_fields=["last_maintained_by"])

            return redirect("maintenance_detail", maintenance_id=maintenance.id)

        return render(request, "maintenance/creer_maintenance.html", {
            "exemplaire": exemplaire,
            "now": timezone.now(),
        })

"""

"""

@login_required
def maintenance_tenant_view(request, exemplaire_id):
    # Récupère le tenant courant
    tenant = request.user.societe

    with tenant_context(tenant):
        # Récupération de l'exemplaire par UUID
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # Vérifie que le client appartient au tenant courant
        if exemplaire.client.societe_id != tenant.id:
            return render(request, "403.html", status=403)

        # Vérifie que l'utilisateur est un mécanicien
        if request.user.role != "mécanicien":
            return render(request, "403.html", status=403)


        return render(request, "maintenance/creer_maintenance.html", {
            "exemplaire": exemplaire,
            "now": timezone.now(),
        })

"""



@login_required
def maintenance_tenant_view(request, exemplaire_id):
    tenant = request.user.societe

    # Utilisation du contexte du tenant si tu as multi-tenant
    with tenant_context(tenant):
        exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

        # Vérifie que le client appartient au tenant courant
        if exemplaire.client.societe_id != tenant.id:
            return render(request, "403.html", status=403)

        if request.method == "POST":
            # Création du check-up complet
            maintenance = creer_checkup_complet(request, exemplaire)

            # Met à jour le dernier utilisateur ayant fait la maintenance
            exemplaire.last_maintained_by = request.user
            exemplaire.save(update_fields=["last_maintained_by"])

            # Redirection vers la page détail du check-up
            return redirect('maintenance:maintenance_detail', maintenance_id=maintenance.id)

        # GET → afficher la page de création
        return render(request, "maintenance/creer_maintenance.html", {
            "exemplaire": exemplaire,
            "now": timezone.now(),
        })




@login_required
def maintenance_detail_view(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    return render(request, "maintenance/detail.html", {
        "maintenance": maintenance
    })
