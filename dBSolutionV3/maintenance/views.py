from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django_tenants.utils import tenant_context
from voiture.voiture_exemplaire.models import VoitureExemplaire
from voiture.voiture_modele.models import VoitureModele


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

