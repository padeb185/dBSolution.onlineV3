from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import never_cache

from maintenance.freins.models import ControleFreins
from maintenance.systeme_freinage.frein_main.models import FreinMain
from maintenance.systeme_freinage.frein_main_hydraulique.models import FreinMainHydraulique
from maintenance.systeme_freinage.nettoyage_freins.models import NettoyageFreins
from maintenance.systeme_freinage.renovation_machoires.models import RenovationMachoires
from maintenance.systeme_freinage.tambours.models import Tambours
from voiture.voiture_exemplaire.models import VoitureExemplaire


def totaux_freinage(exemplaire):
    """Nombre d'interventions sur le système de freinage, par module, pour un exemplaire."""
    totaux = {
        "total_controle_freins": ControleFreins.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_nettoyage_freins": NettoyageFreins.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_tambours": Tambours.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_frein_main": FreinMain.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_frein_main_hydraulique": FreinMainHydraulique.objects.filter(voiture_exemplaire=exemplaire).count(),
        "total_renovation_machoires": RenovationMachoires.objects.filter(voiture_exemplaire=exemplaire).count(),
    }
    totaux["total_freinage"] = sum(totaux.values())
    return totaux


@never_cache
@login_required
def dashboard_freinage_view(request, exemplaire_id):
    exemplaire = get_object_or_404(VoitureExemplaire, id=exemplaire_id)
    context = {"exemplaire": exemplaire}
    context.update(totaux_freinage(exemplaire))
    return render(request, "systeme_freinage/dashboard_freinage.html", context)
