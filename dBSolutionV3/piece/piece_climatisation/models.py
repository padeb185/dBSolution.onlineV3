from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Climatisation(Piece):

    TYPE_PIECE_CLIM = (
        ("qualite_gaz", _("Qualité de gaz")),
        ("quantite_gaz", _("Quantité de gaz")),
        ("compresseur", _("Compresseur")),
        ("evaporateur", _("Évaporateur")),
        ("condenseur", _("Condenseur")),
        ("filtre", _("Filtre")),
        ("dehydrateur", _("Déshydrateur")),
        ("valves", _("Valves")),
        ("durites", _("Durites")),
        ("huile_clim", _("Huile de climatisation")),
    )

    type_piece_clim = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_CLIM,
        verbose_name=_("Type de pièce de climatisation")
    )

    # 🔗 Compatibilité moteur ou véhicule (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="climatisations",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce de climatisation")
        verbose_name_plural = _("Pièces de climatisation")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_clim_display(),
            "piece": super().__str__()
        }
