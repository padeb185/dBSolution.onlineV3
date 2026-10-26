from django.apps import AppConfig


class BoiteDeVitesseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance.autres_interventions.boite_de_vitesse'

    def ready(self):
        # Boîte liée : renseignée automatiquement sur les interventions boîte / embrayage
        from .boite_liee import connecter_signaux
        connecter_signaux()
