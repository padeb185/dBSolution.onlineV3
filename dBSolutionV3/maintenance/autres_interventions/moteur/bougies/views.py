from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from voiture.voiture_exemplaire.models import VoitureExemplaire

from .composants import bougies_vehicule


# ======================================================
# DASHBOARD BOUGIES (bougies d'allumage + bougies de préchauffage)
# ======================================================
@never_cache
@login_required
def dashboard_bougies_view(request, exemplaire_id):
    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    bougies = bougies_vehicule(exemplaire)
    return render(request, "bougies/dashboard_bougies.html", {
        "exemplaire": exemplaire,
        "bougies": bougies,
        "total_bougies": sum(b["total"] for b in bougies),
    })
