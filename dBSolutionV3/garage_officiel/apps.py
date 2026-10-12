from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GarageOfficielConfig(AppConfig):
    name = "garage_officiel"
    verbose_name = _("Garages officiels")
