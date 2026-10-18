from django.apps import AppConfig


class EspConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.esp"
    label = "esp"
    verbose_name = "ESP (contrôle de stabilité)"
