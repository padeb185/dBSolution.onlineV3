from django.apps import AppConfig


class SuspensionOrigineConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.suspension.suspension_origine"
    label = "suspension_origine"
    verbose_name = "Suspension d'origine"
