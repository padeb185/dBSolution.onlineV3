from django.apps import AppConfig


class CasseBoiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.boite_de_vitesse.casse_boite"
    label = "casse_boite"
    verbose_name = "Casse boîte manuelle"
