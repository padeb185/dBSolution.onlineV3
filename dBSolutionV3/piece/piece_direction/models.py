from django.db import models
from piece.models import Piece

class Direction(Piece):

    TYPE_PIECE_DIRECTION = (
        ("cremailere_direction", "Crémaillère de direction"),
        ("pompe_direction", "Pompe de direction"),
        ("biellette_direction_g", "Biellette de direction G"),
        ("biellette_direction_d", "Biellette de direction D"),
        ("rotule_direction_g", "Rotule direction G"),
        ("rotule_direction_d", "Rotule direction D"),
        ("soufflets", "Soufflets"),
        ("durite_direction", "Durite de direction"),
        ("huile_direction_quantite", "Huile de direction quantité"),
        ("huile_direction_qualite", "Huile de direction qualité"),
        ("reservoir", "Réservoir"),
    )

    type_piece_direction = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_DIRECTION
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="directions",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce de direction"
        verbose_name_plural = "Pièces de direction"

    def __str__(self):
        return f"{self.get_type_piece_direction_display()} – {super().__str__()}"
