from django.apps import AppConfig


class MaindoeuvreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maindoeuvre'

    def ready(self):
        # Véhicule + kilométrage de la fiche main-d'œuvre repris de l'intervention liée
        from .liaison import connecter_signaux
        connecter_signaux()
