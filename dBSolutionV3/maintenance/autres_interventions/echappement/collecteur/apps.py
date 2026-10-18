from django.apps import AppConfig


class CollecteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.echappement.collecteur"
    label = "collecteur"
    verbose_name = "Collecteur d'échappement"
