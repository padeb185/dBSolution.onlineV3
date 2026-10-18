from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from voiture.voiture_exemplaire.models import VoitureExemplaire

from .composants import suspensions_vehicule


# ======================================================
# DASHBOARD SUSPENSION (suspension d'origine + suspension sport)
# ======================================================
@never_cache
@login_required
def dashboard_suspension_view(request, exemplaire_id):
    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    suspensions = suspensions_vehicule(exemplaire)
    return render(request, "suspension/dashboard_suspension.html", {
        "exemplaire": exemplaire,
        "suspensions": suspensions,
        "total_suspension": sum(s["total"] for s in suspensions),
    })
