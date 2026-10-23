from django.apps import AppConfig


class PreparationMoteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.preparation_course.preparation_moteur"
    label = "pc_moteur"
    verbose_name = "Préparation moteur"
