"""
Regroupement « Boîte de vitesse » : boîte manuelle, boîte automatique, boîte de transfert.
Utilisé par le tableau de bord des boîtes et par la carte de choisir_autre.
"""
from django.utils.translation import gettext_lazy as _


def boites_vehicule(exemplaire):
    from maintenance.autres_interventions.boite_de_vitesse.models import ControleBoite
    from maintenance.autres_interventions.boite_de_vitesse.casse_boite.models import CasseBoite
    from maintenance.autres_interventions.boite_de_vitesse.remplacement_boite.models import RemplacementBoite
    from maintenance.autres_interventions.bte_vitesse_auto.models import ControleBteVitesseAuto
    from maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto.models import RemplacementBteAuto
    from maintenance.autres_interventions.boite_transfert.models import BoiteTransfert

    filtre = {"voiture_exemplaire": exemplaire}
    return [
        {
            "label": _("Boîte de vitesses manuelle"),
            "url": "boite_de_vitesse:dashboard_boite",
            "icone": "icons/boite-de-vitesse.png",
            "total": (
                ControleBoite.objects.filter(**filtre).count()
                + RemplacementBoite.objects.filter(**filtre).count()
                + CasseBoite.objects.filter(**filtre).count()
            ),
        },
        {
            "label": _("Boîte automatique"),
            "url": "bte_auto:dashboard_bte_auto",
            "icone": "icons/boite-auto.png",
            "total": (
                ControleBteVitesseAuto.objects.filter(**filtre).count()
                + RemplacementBteAuto.objects.filter(**filtre).count()
            ),
        },
        {
            "label": _("Boîte de transfert / transmission intégrale"),
            "url": "boite_transfert:transfert_list",
            "icone": "icons/boite-transfert.png",
            "total": BoiteTransfert.objects.filter(**filtre).count(),
        },
    ]


def total_boites(exemplaire):
    return sum(b["total"] for b in boites_vehicule(exemplaire))
