from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from maintenance.esthetique.ceramique.models import Ceramique
from maintenance.esthetique.cire.models import Cire
from maintenance.esthetique.decontamination.models import Decontamination
from maintenance.esthetique.nettoyage_exterieur.models import NettoyageExterieur
from maintenance.esthetique.polish.models import Polish
from voiture.voiture_exemplaire.models import VoitureExemplaire


def totaux_esthetique(exemplaire):
    """Nombre d'interventions esthétiques par module pour un exemplaire."""
    totaux = {
        "total_nettoyage_exterieur": NettoyageExterieur.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_decontamination": Decontamination.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_polish": Polish.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_cire": Cire.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_ceramique": Ceramique.objects.filter(voiture_exemplaire=exemplaire).count(),
    }
    totaux["total_esthetique"] = sum(totaux.values())
    return totaux


@never_cache
@login_required
def dashboard_esthetique_view(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)

    context = {
        "exemplaire": exemplaire,
        "is_checkup_allowed": request.user.role in [
            "direction",
            "mecanicien",
            "chef_mecanicien",
            "magasinier",
            "apprenti",
        ],
    }
    context.update(totaux_esthetique(exemplaire))

    return render(request, "esthetique/dashboard_esthetique.html", context)
