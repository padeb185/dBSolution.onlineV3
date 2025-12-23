from django.db import models
from piece.models import Piece

class Echappement(Piece):

    TYPE_PIECE_ECHAPPEMENT = (
        ("collecteur_echappement", "Collecteur Échappement"),
        ("filtre_particule", "Filtre à Particule"),
        ("pot_de_deNox", "Pot de deNOx"),
        ("pot_catalytique", "Pot Catalytique"),
        ("ligne_echappement", "Ligne d’Échappement"),
        ("silencieux", "Silencieux"),
        ("colliers", "Colliers"),
        ("silent_blocs", "Silent Blocs"),
        ("joint_collecteur", "Joint Collecteur"),
        ("joint_ligne", "Joint Ligne"),
        ("materiau", "Matériau"),
        ("soudure", "Soudure"),
    )

    type_piece_echappement = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ECHAPPEMENT
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="echappements",
        blank=True
    )

    class Meta:
        verbose_name = "Pièce d'échappement"
        verbose_name_plural = "Pièces d'échappement"

    def __str__(self):
        return f"{self.get_type_piece_echappement_display()} – {super().__str__()}"
