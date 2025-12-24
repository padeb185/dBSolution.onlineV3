from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class PieceHydraulique(Piece):
    FRONT_LIFT = "FRONT_LIFT"
    REAR_LIFT = "REAR_LIFT"
    COMPRESSEUR = "COMPRESSEUR"
    HUILE_COMPRESSEUR = "HUILE_COMPRESSEUR"

    TYPE_HYDRAULIQUE_CHOICES = [
        (FRONT_LIFT, _("Front lift")),
        (REAR_LIFT, _("Rear lift")),
        (COMPRESSEUR, _("Compresseur")),
        (HUILE_COMPRESSEUR, _("Huile compresseur")),
    ]

    type_hydraulique = models.CharField(
        max_length=50,
        choices=TYPE_HYDRAULIQUE_CHOICES,
        verbose_name=_("Type de pièce hydraulique")
    )

    class Meta:
        verbose_name = _("Pièce hydraulique")
        verbose_name_plural = _("Pièces hydrauliques")

    def __str__(self):
        return f"{self.nom} ({self.get_type_hydraulique_display()})"
