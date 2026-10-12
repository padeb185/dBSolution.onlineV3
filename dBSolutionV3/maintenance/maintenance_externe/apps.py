from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MaintenanceExterneConfig(AppConfig):
    name = "maintenance.maintenance_externe"
    label = "maintenance_externe"
    verbose_name = _("Maintenances externes")
