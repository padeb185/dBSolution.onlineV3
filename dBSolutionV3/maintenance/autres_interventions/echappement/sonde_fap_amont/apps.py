from django.apps import AppConfig


class SondeFapAmontConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.echappement.sonde_fap_amont"
    label = "sonde_fap_amont"
    verbose_name = "Sonde de température FAP amont"
