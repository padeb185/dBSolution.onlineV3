"""Suspension : une app par type de suspension (dashboard Suspension)."""
from importlib import import_module

from django.utils.translation import gettext_lazy as _

# (app / namespace, classe du modèle, libellé)
SUSPENSIONS = [
    ("suspension_origine", "SuspensionOrigine", _("Suspension d'origine")),
    ("suspension_sport", "SuspensionSport", _("Suspension sport")),
]


def modele_suspension(app):
    for code, classe, _label in SUSPENSIONS:
        if code == app:
            return getattr(import_module(f"maintenance.autres_interventions.suspension.{code}.models"), classe)
    raise LookupError(app)


def suspensions_vehicule(exemplaire):
    """[{code, label, total, url_list, icone}] pour un véhicule."""
    return [
        {
            "code": code,
            "label": label,
            "total": modele_suspension(code).objects.filter(voiture_exemplaire=exemplaire).count() if exemplaire else 0,
            "url_list": f"{code}:{code}_list",
            "icone": f"icons/susp_{code}.png",
        }
        for code, _classe, label in SUSPENSIONS
    ]


def total_suspension(exemplaire):
    return sum(b["total"] for b in suspensions_vehicule(exemplaire))
