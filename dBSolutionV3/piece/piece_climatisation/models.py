from django.db import models
from piece.models import Piece

class Climatisation(Piece):

    TYPE_PIECE_CLIM = (
        ("qualite_gaz", "Qualité de gaz"),
        ("quantite_gaz", "Quantité de gaz"),
        ("compresseur", "Compresseur"),
        ("evaporateur", "Évaporateur"),
        ("condenseur", "Condenseur"),
        ("filtre", "Filtre"),
        ("dehydrateur", "Déshydrateur"),
        ("valves", "Valves"),
        ("durites", "Durites"),
        ("huile_clim", "Huile de climatisation"),
    )

    type_piece_clim = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_CLIM
    )

    # 🔗 compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="climatisations",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce climatisation"
        verbose_name_plural = "Pièces climatisation"

    def __str__(self):
        return f"{self.get_type_piece_clim_display()} – {super().__str__()}"
