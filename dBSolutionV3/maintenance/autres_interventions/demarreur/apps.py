from django.apps import AppConfig


class DemarreurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.demarreur"
    label = "demarreur"
    verbose_name = "Démarreur"
