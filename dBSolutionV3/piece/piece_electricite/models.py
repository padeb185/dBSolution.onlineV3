from django.db import models
from piece.models import Piece

class Electricite(Piece):
    from django.utils.translation import gettext_lazy as _

    TYPE_PIECE_ELECTRICITE = (
        ("alternateur", _("Alternateur")),
        ("batterie", _("Batterie")),
        ("demarreur", _("Démarreur")),
        ("leve_vitre_avg", _("Lève-vitre avant gauche")),
        ("leve_vitre_avd", _("Lève-vitre avant droit")),
        ("leve_vitre_arg", _("Lève-vitre arrière gauche")),
        ("leve_vitre_ard", _("Lève-vitre arrière droit")),
        ("pompe_lave_glace_av", _("Pompe lave-glace avant")),
        ("pompe_lave_glace_ar", _("Pompe lave-glace arrière")),
        ("klaxon", _("Klaxon")),
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
