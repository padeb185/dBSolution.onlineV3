from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PieceTransmission(Piece):

    TYPE_PIECE_TRANSMISSION = (

        # 🔧 Cardans complets
        ("cardan_av_g", _("Cardan avant gauche")),
        ("cardan_av_d", _("Cardan avant droit")),
        ("cardan_ar_g", _("Cardan arrière gauche")),
        ("cardan_ar_d", _("Cardan arrière droit")),

        # ⚙️ Pièces internes de cardan
        ("noix_cardan", _("Noix de cardan")),
        ("tulipe_cardan", _("Tulipe de cardan")),
        ("joint_homocinetique_ext", _("Joint homocinétique extérieur")),
        ("joint_homocinetique_int", _("Joint homocinétique intérieur")),
        ("tripode", _("Tripode")),
        ("galet_tripode", _("Galet de tripode")),
        ("etoile_cardan", _("Étoile de cardan")),
        ("cage_billes", _("Cage à billes")),
        ("billes_cardan", _("Billes de cardan")),
        ("axe_cardan", _("Axe de cardan")),

        # 🧴 Étanchéité et fixation
        ("soufflet_cardan_int", _("Soufflet de cardan intérieur")),
        ("soufflet_cardan_ext", _("Soufflet de cardan extérieur")),
        ("collier_serrage", _("Collier de serrage")),
        ("joint_etancheite", _("Joint d’étanchéité")),
        ("circlip", _("Circlip")),
        ("graisse_cardan", _("Graisse de cardan")),

        # 🔩 Arbre de transmission
        ("arbre_transmission", _("Arbre de transmission")),
        ("palier_arbre_transmission", _("Palier d’arbre de transmission")),
        ("support_palier", _("Support de palier")),
        ("croisillon", _("Croisillon")),
        ("flector", _("Flector")),
        ("bride_transmission", _("Bride de transmission")),



        ("kit_soufflet_cardan", _("Kit soufflet de cardan")),
        ("kit_joint_cardan", _("Kit joint de cardan")),
        ("kit_cardan_complet", _("Kit cardan complet")),
        ("kit_arbre_transmission", _("Kit arbre de transmission")),
    )

    type_piece_transmission = models.CharField(
        max_length=70,
        choices=TYPE_PIECE_TRANSMISSION,
        verbose_name=_("Type de pièce de transmission")
    )

    # 🔗 compatibilité modèle voiture
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pieces_transmission",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce de transmission")
        verbose_name_plural = _("Pièces de transmission")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_transmission_display(),
            "nom": super().__str__()
        }

