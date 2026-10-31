from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VoitureRemorqueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "voiture.voiture_remorque"
    label = "voiture_remorque"
    verbose_name = _("Remorques")
