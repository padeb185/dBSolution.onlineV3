from django.db import models
from piece.models import Piece
from piece.models import CodeBarre
from piece.piece_feux.models import Feux


class Ampoule(Piece):
    # Relation avec le feu spécifique
    feu = models.ForeignKey(
        Feux,
        on_delete=models.CASCADE,
        related_name="ampoules"
    )

    # Type d'ampoule
    TYPES_AMP = [
        ("H1", "H1"),
        ("H3", "H3"),
        ("H4", "H4"),
        ("H7", "H7"),
        ("H11", "H11"),
        ("HB3", "HB3"),
        ("HB4", "HB4"),
        ("LED", "LED"),
        ("XENON", "Xénon"),
        ("C5W", "C5W"),
        ("W5W", "W5W"),
        ("T10", "T10"),
        ("T4W", "T4W"),
        # Ajoute d'autres types si nécessaire
    ]

    type_ampoule = models.CharField(
        max_length=10,
        choices=TYPES_AMP,
        verbose_name="Type d'ampoule"
    )

    # Relation Code-Barre si nécessaire
    code_barre = models.ForeignKey(
        CodeBarre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ampoules"
    )

    # Caractéristiques supplémentaires
    puissance = models.CharField(max_length=10, blank=True, help_text="Puissance en Watts")
    couleur = models.CharField(max_length=20, blank=True, help_text="Couleur de la lumière")
    tension = models.CharField(max_length=10, blank=True, help_text="Tension en Volts")

    class Meta:
        verbose_name = "Ampoule"
        verbose_name_plural = "Ampoules"

    def __str__(self):
        return f"{self.type_ampoule} - {self.feu} - {self.puissance or ''}W"
