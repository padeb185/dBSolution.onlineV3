from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Echappement(Piece):

    TYPE_PIECE_ECHAPPEMENT = (
        ("collecteur_echappement", _("Collecteur d’échappement")),
        ("filtre_particules", _("Filtre à particules")),
        ("pot_denox", _("Pot de déNOx")),
        ("pot_catalytique", _("Pot catalytique")),
        ("ligne_echappement", _("Ligne d’échappement")),
        ("silencieux", _("Silencieux")),
        ("colliers", _("Colliers")),
        ("silent_blocs", _("Silent blocs")),
        ("joint_collecteur", _("Joint de collecteur")),
        ("joint_ligne", _("Joint de ligne")),
        ("materiau", _("Matériau")),
        ("soudure", _("Soudure")),
    )

    type_piece_echappement = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_ECHAPPEMENT,
        verbose_name=_("Type de pièce d’échappement")
    )

    # 🔗 Compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="echappements",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce d’échappement")
        verbose_name_plural = _("Pièces d’échappement")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_echappement_display(),
            "piece": super().__str__()
        }
