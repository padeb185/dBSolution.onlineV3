from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Essuyage(Piece):

    TYPE_PIECE_ESSUYAGE = (
        ("balai_av", _("Balai avant")),
        ("balai_ar", _("Balai arrière")),
        ("moteur_essuie_glace_av", _("Moteur essuie-glace avant")),
        ("moteur_essuie_glace_ar", _("Moteur essuie-glace arrière")),
    )

    type_piece_essuyage = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ESSUYAGE,
        verbose_name=_("Type de pièce d'essuyage")
    )

    # 🔗 Compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="essuyages",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce d'essuyage")
        verbose_name_plural = _("Pièces d'essuyage")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_essuyage_display(),
            "piece": super().__str__()
        }
