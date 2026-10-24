from django.apps import AppConfig


class CasseMoteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.moteur.casse_moteur"
    label = "casse_moteur"
    verbose_name = "Casse moteur"
