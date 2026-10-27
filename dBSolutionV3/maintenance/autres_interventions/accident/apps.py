from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccidentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.accident"
    verbose_name = _("Rapport d'accident")
