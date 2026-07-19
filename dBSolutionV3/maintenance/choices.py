from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


class RouesSerrageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("À faire")
    FAIT = "FAIT", _("Fait")


TAUX_HORAIRE_CHOICES = [
    (Decimal("25.00"), _("25,00 €")),
    (Decimal("30.00"), _("30,00 €")),
    (Decimal("35.00"), _("35,00 €")),
    (Decimal("40.00"), _("40,00 €")),
    (Decimal("45.00"), _("45,00 €")),
    (Decimal("50.00"), _("50,00 €")),
    (Decimal("55.00"), _("55,00 €")),
    (Decimal("60.00"), _("60,00 €")),
    (Decimal("65.00"), _("65,00 €")),
    (Decimal("70.00"), _("70,00 €")),
]