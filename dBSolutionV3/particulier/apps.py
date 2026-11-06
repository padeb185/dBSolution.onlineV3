from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ParticulierConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "particulier"
    verbose_name = _("Particuliers (application mobile)")
