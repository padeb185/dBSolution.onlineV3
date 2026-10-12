from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VoitureDiagnosticConfig(AppConfig):
    name = "voiture.voiture_diagnostic"
    verbose_name = _("Diagnostics")
