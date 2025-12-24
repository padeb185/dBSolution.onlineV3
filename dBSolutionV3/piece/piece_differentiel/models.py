from django.db import models
from piece.models import Piece

class Differentiel(Piece):

    TYPE_PIECE_DIFFERENTIEL = (
        ("huile_differentiel", "Huile différentiel"),
        ("arbre_transmission", "Arbre de transmission"),
        ("joint", "Joint"),
        ("vidange", "Vidange"),
        ("couronne_pignon", "Couronne et pignon"),
        ("roulements_differentiel", "Roulements différentiel"),
        ("carter_differentiel", "Carter différentiel"),
        ("visserie", "Visserie"),
        ("soufflet", "Soufflet"),
        ("synchroniseur", "Synchroniseur"),
        ("axe_satellite", "Axe satellite"),
        ("satellites_planétaires", "Satellites planétaires"),
    )

    type_piece_differentiel = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_DIFFERENTIEL
    )

    # 🔗 compatibilité moteur ou véhicule
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="differentiel",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce différentiel"
        verbose_name_plural = "Pièces différentiel"

    def __str__(self):
        return f"{self.get_type_piece_differentiel_display()} – {super().__str__()}"
