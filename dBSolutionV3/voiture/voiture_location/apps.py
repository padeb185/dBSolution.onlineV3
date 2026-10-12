from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VoitureLocationConfig(AppConfig):
    name = "voiture.voiture_location"
    verbose_name = _("Locations de véhicules")
