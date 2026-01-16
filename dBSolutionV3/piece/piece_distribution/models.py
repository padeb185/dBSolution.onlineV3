from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Distribution(Piece):
    """
    Pièces liées à la distribution d'une voiture.
    """

    TYPE_PIECE_DISTRIBUTION = (
        ("courroie_distribution", _("Courroie de distribution")),
        ("chaine_distribution", _("Chaîne de distribution")),
        ("galet_tendeur", _("Galet tendeur")),
        ("galet_libre", _("Galet libre")),
        ("pompe_eau", _("Pompe à eau")),
        ("guide_chaine", _("Guide de chaîne")),  # <-- ajouté
        ("joint_culot", _("Joint de culot")),
        ("tendeur_hydraulique", _("Tendeur hydraulique")),
        ("cache_distribution", _("Cache distribution")),

    )

    type_piece_distribution = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_DISTRIBUTION,
        verbose_name=_("Type de pièce de distribution")
    )

    # 🔗 Compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="distributions",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce de distribution")
        verbose_name_plural = _("Pièces de distribution")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_distribution_display(),
            "piece": super().__str__()
        }
