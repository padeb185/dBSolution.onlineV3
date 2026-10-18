from django.apps import AppConfig


class InjecteurAdblueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.echappement.injecteur_adblue"
    label = "injecteur_adblue"
    verbose_name = "Injecteur AdBlue"
