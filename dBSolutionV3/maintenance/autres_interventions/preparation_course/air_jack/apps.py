from django.apps import AppConfig


class AirJackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.autres_interventions.preparation_course.air_jack"
    label = "pc_air_jack"
    verbose_name = "Air jack (vérins pneumatiques)"
