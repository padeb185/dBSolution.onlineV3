from django.apps import AppConfig


class SilentBlocsEchappementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.echappement.silent_blocs_echappement"
    label = "silent_blocs_echappement"
    verbose_name = "Silent blocs d'échappement"
