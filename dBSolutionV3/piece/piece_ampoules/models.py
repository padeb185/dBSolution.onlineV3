from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece, CodeBarre
from piece.piece_feux.models import Feux


class Ampoule(Piece):
    # 🔗 Relation avec le feu spécifique
    feu = models.ForeignKey(
        Feux,
        on_delete=models.CASCADE,
        related_name="ampoules",
        verbose_name=_("Feu")
    )

    # 💡 Type d'ampoule
    TYPES_AMP = [
        ("H1", _("H1")),
        ("H3", _("H3")),
        ("H4", _("H4")),
        ("H7", _("H7")),
        ("H11", _("H11")),
        ("HB3", _("HB3")),
        ("HB4", _("HB4")),
        ("LED", _("LED")),
        ("XENON", _("Xénon")),
        ("C5W", _("C5W")),
        ("W5W", _("W5W")),
        ("T10", _("T10")),
        ("T4W", _("T4W")),
    ]

    type_ampoule = models.CharField(
        max_length=10,
        choices=TYPES_AMP,
        verbose_name=_("Type d’ampoule")
    )

    # 🏷️ Code-barres
    code_barre = models.ForeignKey(
        CodeBarre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ampoules",
        verbose_name=_("Code-barres")
    )

    # ⚙️ Caractéristiques
    puissance = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("Puissance"),
        help_text=_("Puissance en watts")
    )

    couleur = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Couleur"),
        help_text=_("Couleur de la lumière")
    )

    tension = models.CharField(
        max_length=10,
        blank=True,
        verbose_name=_("Tension"),
        help_text=_("Tension en volts")
    )

    class Meta:
        verbose_name = _("Ampoule")
        verbose_name_plural = _("Ampoules")

    def __str__(self):
        return f"{self.type_ampoule} - {self.feu} - {self.puissance or ''}W"
