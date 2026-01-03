from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class TrainArriere(Piece):

    TYPE_PIECE_TRAIN_AR = (
        ("pont", _("Pont")),
        ("berceau", _("Berceau")),
        ("barre_torsion", _("Barre de torsion")),
        ("triangle_sup_g", _("Triangle supérieur gauche")),
        ("triangle_sup_d", _("Triangle supérieur droit")),
        ("triangle_inf_g", _("Triangle inférieur gauche")),
        ("triangle_inf_d", _("Triangle inférieur droit")),
        ("silent_bloc", _("Silent bloc")),
        ("kit_silent_bloc", _("Kit silent bloc")),
        ("roulement_roue", _("Roulement de roue")),
        ("moyeu", _("Moyeu")),
        ("porte_fusee", _("Porte fusée")),
        ("fusee", _("Fusée")),
        ("amortisseur_gd", _("Amortisseur G/D")),
        ("ressort", _("Ressort")),
        ("barre_stabilisatrice", _("Barre stabilisatrice")),
        ("biellette_barre_stab", _("Biellette de barre stabilisatrice")),
        ("train_ar_directeur_gd", _("Train AR directeur G/D")),
        ("cardan_g", _("Cardan G")),
        ("cardan_d", _("Cardan D")),
        ("arbre_transmission", _("Arbre de transmission")),
    )

    type_piece_train = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_TRAIN_AR,
        verbose_name=_("Type de pièce train arrière")
    )

    # 🔗 compatibilité modele
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="train_arriere",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce train arrière")
        verbose_name_plural = _("Pièces train arrière")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_train_display(),
            "nom": super().__str__()
        }
