"""Préparation course : une app par intervention (dashboard Préparation course)."""
from importlib import import_module

from django.utils.translation import gettext_lazy as _

# (dossier, app / namespace, classe du modèle, libellé)
PREPARATIONS = [
    ("arceau", "pc_arceau", "ArceauSecurite", _("Arceau de sécurité")),
    ("extincteur", "pc_extincteur", "Extincteur", _("Extincteur")),
    ("sieges_baquets", "pc_sieges", "SiegesBaquets", _("Sièges baquets et harnais")),
    ("cablage", "pc_cablage", "CablageCompetition", _("Câblage électrique")),
    ("boitier_competition", "pc_boitier", "BoitierCompetition", _("Boîtier compétition / additionnel")),
    ("preparation_moteur", "pc_moteur", "PreparationMoteur", _("Préparation moteur")),
    ("echappement_course", "pc_echappement", "EchappementCompetition", _("Échappement compétition")),
    ("demontage", "pc_demontage", "DemontageAllegement", _("Démontage et allègement")),
    ("air_jack", "pc_air_jack", "AirJack", _("Air jack (vérins pneumatiques)")),
]


def modele_preparation(code):
    for dossier, app, classe, _label in PREPARATIONS:
        if app == code:
            return getattr(import_module(f"maintenance.autres_interventions.preparation_course.{dossier}.models"), classe)
    raise LookupError(code)


def preparations_vehicule(exemplaire):
    """[{code, label, total, url_list, icone}] pour un véhicule."""
    return [
        {
            "code": app,
            "label": label,
            "total": modele_preparation(app).objects.filter(voiture_exemplaire=exemplaire).count() if exemplaire else 0,
            "url_list": f"{app}:{app}_list",
            "icone": f"icons/{app}.png",
        }
        for _dossier, app, _classe, label in PREPARATIONS
    ]


def total_preparation_course(exemplaire):
    return sum(p["total"] for p in preparations_vehicule(exemplaire))
