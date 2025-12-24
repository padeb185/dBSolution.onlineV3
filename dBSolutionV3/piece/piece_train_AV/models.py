from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class TrainAvant(Piece):

    TYPE_PIECE_TRAIN = (
        ("berceau", _("Berceau")),
        ("cardan_g", _("Cardan G")),
        ("cardan_d", _("Cardan D")),
        ("triangle_sup_g", _("Triangle supérieur gauche")),
        ("triangle_sup_d", _("Triangle supérieur droit")),
        ("triangle_inf_g", _("Triangle inférieur gauche")),
        ("triangle_inf_d", _("Triangle inférieur droit")),
        ("multi_bras_g", _("Multi-bras G")),
        ("multi_bras_d", _("Multi-bras D")),
        ("barres_torsion", _("Barres de torsion")),
        ("silent_bloc", _("Silent bloc")),
        ("kit_silent_bloc", _("Kit silent bloc")),
        ("roulement_roue", _("Roulement de roue")),
        ("moyeu", _("Moyeu")),
        ("porte_fusee", _("Porte fusée")),
        ("fusee", _("Fusée")),
        ("amortisseur_gd", _("Amortisseur G/D")),
        ("ressort", _("Ressort")),
        ("roulement_suspension", _("Roulement de suspension")),
        ("barre_stabilisatrice", _("Barre stabilisatrice")),
        ("biellette_barre_stab", _("Biellette de barre stabilisatrice")),
    )

    type_piece_train = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_TRAIN,
        verbose_name=_("Type de pièce train avant")
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="train_avant",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce train avant")
        verbose_name_plural = _("Pièces train avant")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_train_display(),
            "nom": super().__str__()
        }
