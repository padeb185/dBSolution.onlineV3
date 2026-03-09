# maintenance/constants.py
from django.utils.translation import gettext_lazy as _

TYPES_MAINTENANCE = [
    {"code": "checkup", "nom": _("Checkup")},
    {"code": "entretien", "nom": _("Entretien")},
    {"code": "freins", "nom": _("Freins")},
    {"code": "pneus", "nom": _("Pneus")},
    {"code": "nettoyage_ext", "nom": _("Nettoyage extérieur")},
    {"code": "nettoyage_int", "nom": _("Nettoyage intérieur")},
    {"code": "niveaux", "nom": _("Niveaux")},
    {"code": "autres", "nom": _("Autres interventions")},
]