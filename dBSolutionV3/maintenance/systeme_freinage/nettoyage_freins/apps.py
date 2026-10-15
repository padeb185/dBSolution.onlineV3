from django.apps import AppConfig


class NettoyageFreinsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.systeme_freinage.nettoyage_freins"
    label = "nettoyage_freins"
    verbose_name = "Nettoyage des freins"
