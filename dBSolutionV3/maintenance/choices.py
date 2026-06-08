from django.db import models
from django.utils.translation import gettext_lazy as _

class RouesSerrageEtat(models.TextChoices):
    A_FAIRE = "AFAIRE", _("À faire")
    FAIT = "Fait", _("Fait")
