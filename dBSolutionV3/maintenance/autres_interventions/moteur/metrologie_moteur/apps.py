from django.apps import AppConfig


class MetrologieMoteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.moteur.metrologie_moteur"
    label = "metrologie_moteur"
    verbose_name = "Métrologie moteur"
