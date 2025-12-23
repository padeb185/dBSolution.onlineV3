from django.db import models
from piece.models import Piece

class TrainAvant(Piece):

    TYPE_PIECE_TRAIN = (
        ("berceau", "Berceau"),
        ("cardan_g", "Cardan G"),
        ("cardan_d", "Cardan D"),
        ("triangle_sup_g", "Triangle Supérieur gauche"),
        ("triangle_sup_d", "Triangle Supérieur droit"),
        ("triangle_inf_g", "Triangle inférieur gauche"),
        ("triangle_inf_d", "Triangle inférieur droit"),
        ("multi_bras_g", "Multi-bras G"),
        ("multi_bras_d", "Multi-bras D"),
        ("barres_torsion", "Barres de torsion"),
        ("silent_bloc", "Silent bloc"),
        ("kit_silent_bloc", "Kit silent bloc"),
        ("roulement_roue", "Roulement de roue"),
        ("moyeu", "Moyeu"),
        ("porte_fusee", "Porte fusée"),
        ("fusee", "Fusée"),
        ("amortisseur_gd", "Amortisseur G/D"),
        ("ressort", "Ressort"),
        ("roulement_suspension", "Roulement de suspension"),
        ("barre_stabilisatrice", "Barre stabilisatrice"),
        ("biellette_barre_stab", "Biellette de barre stabilisatrice"),
    )

    type_piece_train = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_TRAIN
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="train_avant",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce train avant"
        verbose_name_plural = "Pièces train avant"

    def __str__(self):
        return f"{self.get_type_piece_train_display()} – {super().__str__()}"
