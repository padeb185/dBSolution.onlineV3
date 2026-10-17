from django.apps import AppConfig


class RemplacementBteAutoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance.autres_interventions.bte_vitesse_auto.remplacement_bte_auto'
    label = 'remplacement_bte_auto'
    verbose_name = 'Remplacement boîte automatique'
