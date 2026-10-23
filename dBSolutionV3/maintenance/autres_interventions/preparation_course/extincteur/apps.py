from django.apps import AppConfig


class ExtincteurConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.preparation_course.extincteur"
    label = "pc_extincteur"
    verbose_name = "Extincteur"
