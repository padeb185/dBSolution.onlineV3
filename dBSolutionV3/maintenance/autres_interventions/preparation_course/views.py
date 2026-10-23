from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from voiture.voiture_exemplaire.models import VoitureExemplaire

from .composants import preparations_vehicule


# ======================================================
# DASHBOARD PRÉPARATION COURSE
# ======================================================
@never_cache
@login_required
def dashboard_preparation_course_view(request, exemplaire_id):
    tenant = request.user.societe
    exemplaire = get_object_or_404(
        VoitureExemplaire.objects.filter(
            Q(client__societe=tenant) | Q(client__isnull=True, societe=tenant)
        ),
        id=exemplaire_id,
    )
    preparations = preparations_vehicule(exemplaire)
    return render(request, "preparation_course/dashboard_preparation_course.html", {
        "exemplaire": exemplaire,
        "preparations": preparations,
        "total_preparation_course": sum(p["total"] for p in preparations),
    })
