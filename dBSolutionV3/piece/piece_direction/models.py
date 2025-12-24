from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Direction(Piece):

    TYPE_PIECE_DIRECTION = (
        ("cremaillere_direction", _("Crémaillère de direction")),
        ("pompe_direction", _("Pompe de direction")),
        ("biellette_direction_g", _("Biellette de direction gauche")),
        ("biellette_direction_d", _("Biellette de direction droite")),
        ("rotule_direction_g", _("Rotule de direction gauche")),
        ("rotule_direction_d", _("Rotule de direction droite")),
        ("soufflets", _("Soufflets")),
        ("durite_direction", _("Durite de direction")),
        ("huile_direction_quantite", _("Huile de direction (quantité)")),
        ("huile_direction_qualite", _("Huile de direction (qualité)")),
        ("reservoir", _("Réservoir")),
    )

    type_piece_direction = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_DIRECTION,
        verbose_name=_("Type de pièce de direction")
    )

    # 🔗 Compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="directions",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce de direction")
        verbose_name_plural = _("Pièces de direction")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_direction_display(),
            "piece": super().__str__()
        }
