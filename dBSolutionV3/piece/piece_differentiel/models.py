from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Differentiel(Piece):

    TYPE_PIECE_DIFFERENTIEL = (
        ("huile_differentiel", _("Huile de différentiel")),
        ("arbre_transmission", _("Arbre de transmission")),
        ("joint", _("Joint")),
        ("vidange", _("Vidange")),
        ("couronne_pignon", _("Couronne et pignon")),
        ("roulements_differentiel", _("Roulements de différentiel")),
        ("carter_differentiel", _("Carter de différentiel")),
        ("visserie", _("Visserie")),
        ("soufflet", _("Soufflet")),
        ("synchroniseur", _("Synchroniseur")),
        ("axe_satellite", _("Axe satellite")),
        ("satellites_planetaires", _("Satellites planétaires")),
    )

    type_piece_differentiel = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_DIFFERENTIEL,
        verbose_name=_("Type de pièce de différentiel")
    )

    # 🔗 Compatibilité moteur ou véhicule
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="differentiels",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce de différentiel")
        verbose_name_plural = _("Pièces de différentiel")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_differentiel_display(),
            "piece": super().__str__()
        }
