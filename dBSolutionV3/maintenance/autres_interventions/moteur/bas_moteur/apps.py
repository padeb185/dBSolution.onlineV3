from django.apps import AppConfig


class BasMoteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.moteur.bas_moteur"
    label = "bas_moteur"
    verbose_name = "Bas moteur"
