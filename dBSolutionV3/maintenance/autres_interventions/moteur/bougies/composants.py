"""Bougies : une app par type de bougie (dashboard Bougies dans Moteur)."""
from importlib import import_module

from django.utils.translation import gettext_lazy as _

# (app / namespace, classe du modèle, libellé)
BOUGIES = [
    ("bougies_allumage", "BougiesAllumage", _("Bougies d'allumage")),
    ("bougies_prechauffage", "BougiesPrechauffage", _("Bougies de préchauffage")),
]


def modele_bougie(app):
    for code, classe, _label in BOUGIES:
        if code == app:
            return getattr(import_module(f"maintenance.autres_interventions.moteur.bougies.{code}.models"), classe)
    raise LookupError(app)


def bougies_vehicule(exemplaire):
    """[{code, label, total, url_list, icone}] pour un véhicule."""
    return [
        {
            "code": code,
            "label": label,
            "total": modele_bougie(code).objects.filter(voiture_exemplaire=exemplaire).count() if exemplaire else 0,
            "url_list": f"{code}:{code}_list",
            "icone": f"icons/bg_{code}.png",
        }
        for code, _classe, label in BOUGIES
    ]


def total_bougies(exemplaire):
    return sum(b["total"] for b in bougies_vehicule(exemplaire))
