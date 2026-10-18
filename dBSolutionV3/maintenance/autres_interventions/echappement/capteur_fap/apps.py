from django.apps import AppConfig


class CapteurFapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.echappement.capteur_fap"
    label = "capteur_fap"
    verbose_name = "Capteur de pression différentielle FAP"
