from django.db import models
from piece.models import Piece

class Essuyage(Piece):

    TYPE_PIECE_ESSUYAGE = (
        ("balai_av", "Balai avant"),
        ("balai_ar", "Balai arrière"),
        ("moteur_essuie_glace_av", "Moteur essuie-glace avant"),
        ("moteur_essuie_glace_ar", "Moteur essuie-glace arrière"),
    )

    type_piece_essuyage = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ESSUYAGE
    )

    # 🔗 compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="essuyages",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce essuyage"
        verbose_name_plural = "Pièces essuyage"

    def __str__(self):
        return f"{self.get_type_piece_essuyage_display()} – {super().__str__()}"
