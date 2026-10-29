from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PlanCablageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.plan_cablage"
    label = "plan_cablage"
    verbose_name = _("Plan de câblage")
