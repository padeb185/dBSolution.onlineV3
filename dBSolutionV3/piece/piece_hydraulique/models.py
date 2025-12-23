from django.db import models
from piece.models import Piece

class PieceHydraulique(Piece):
    FRONT_LIFT = "FRONT_LIFT"
    REAR_LIFT = "REAR_LIFT"
    COMPRESSEUR = "COMPRESSEUR"
    HUILE_COMPRESSEUR = "HUILE_COMPRESSEUR"

    TYPE_HYDRAULIQUE_CHOICES = [
        (FRONT_LIFT, "Front lift"),
        (REAR_LIFT, "Rear lift"),
        (COMPRESSEUR, "Compresseur"),
        (HUILE_COMPRESSEUR, "Huile compresseur"),
    ]

    type_hydraulique = models.CharField(
        max_length=50,
        choices=TYPE_HYDRAULIQUE_CHOICES,
        verbose_name="Type de pièce hydraulique"
    )

    def __str__(self):
        return f"{self.nom} ({self.get_type_hydraulique_display()})"
