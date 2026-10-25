from django.apps import AppConfig


class VentilationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.ventilation"
    label = "ventilation"
    verbose_name = "Ventilation"
