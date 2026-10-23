from django.apps import AppConfig


class DemontageAllegementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.preparation_course.demontage"
    label = "pc_demontage"
    verbose_name = "Démontage et allègement"
