from django.apps import AppConfig


class MoteurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance.autres_interventions.moteur'

    def ready(self):
        from .moteur_lie import connecter_signaux
        connecter_signaux()
