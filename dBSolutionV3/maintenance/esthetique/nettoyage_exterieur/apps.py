from django.apps import AppConfig


class NettoyageExterieurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance.esthetique.nettoyage_exterieur'
    # Label conservé : migrations, tables et données inchangées après le déplacement
    label = 'nettoyage_exterieur'
