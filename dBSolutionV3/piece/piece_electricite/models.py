from django.db import models
from piece.models import Piece

class Electricite(Piece):

    TYPE_PIECE_ELECTRICITE = (
        ("alternateur", "Alternateur"),
        ("batterie", "Batterie"),
        ("demarreur", "Démarreur"),
        ("leve_vitre_avg", "Lève-vitre AVG"),
        ("leve_vitre_avd", "Lève-vitre AVD"),
        ("leve_vitre_arg", "Lève-vitre ARG"),
        ("leve_vitre_ard", "Lève-vitre ARD"),
    )

    type_piece_electricite = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ELECTRICITE
    )

    # 🔗 compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="electricites",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce électricité"
        verbose_name_plural = "Pièces électricité"

    def __str__(self):
        return f"{self.get_type_piece_electricite_display()} – {super().__str__()}"
