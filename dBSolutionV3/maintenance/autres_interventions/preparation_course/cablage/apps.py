from django.apps import AppConfig


class CablageCompetitionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.preparation_course.cablage"
    label = "pc_cablage"
    verbose_name = "Câblage électrique"
