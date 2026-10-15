from django.apps import AppConfig


class LubrificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.moteur.lubrification"
    label = "lubrification"
    verbose_name = "Lubrification moteur"
