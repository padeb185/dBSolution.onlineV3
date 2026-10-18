from django.apps import AppConfig


class SuspensionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.suspension"
    label = "suspension"
    verbose_name = "Suspension"
