from django.db import models
from piece.models import Piece

class TrainArriere(Piece):

    TYPE_PIECE_TRAIN_AR = (
        ("pont", "Pont"),
        ("berceau", "Berceau"),
        ("barre_torsion", "Barre de torsion"),
        ("triangle_sup_g", "Triangle supérieur gauche"),
        ("triangle_sup_d", "Triangle supérieur droit"),
        ("triangle_inf_g", "Triangle inférieur gauche"),
        ("triangle_inf_d", "Triangle inférieur droit"),
        ("silent_bloc", "Silent bloc"),
        ("kit_silent_bloc", "Kit silent bloc"),
        ("roulement_roue", "Roulement de roue"),
        ("moyeu", "Moyeu"),
        ("porte_fusee", "Porte fusée"),
        ("fusee", "Fusée"),
        ("amortisseur_gd", "Amortisseur G/D"),
        ("ressort", "Ressort"),
        ("barre_stabilisatrice", "Barre stabilisatrice"),
        ("biellette_barre_stab", "Biellette de barre stabilisatrice"),
        ("train_ar_directeur_gd", "Train AR directeur G/D"),
        ("cardan_g", "Cardan G"),
        ("cardan_d", "Cardan D"),
        ("arbre_transmission", "Arbre de transmission"),
    )

    type_piece_train = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_TRAIN_AR
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="train_arriere",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce train arrière"
        verbose_name_plural = "Pièces train arrière"

    def __str__(self):
        return f"{self.get_type_piece_train_display()} – {super().__str__()}"
