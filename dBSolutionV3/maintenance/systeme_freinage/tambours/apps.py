from django.apps import AppConfig


class TamboursConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "maintenance.systeme_freinage.tambours"
    label = "tambours"
    verbose_name = "Tambours de frein"
