from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PieceFreins(Piece):

    TYPE_PIECE_FREINAGE = (
        ("machoire_frein_avg", _("Étrier de frein AVG")),
        ("machoire_frein_avd", _("Étrier de frein AVD")),
        ("machoire_frein_arg", _("Étrier de frein ARG")),
        ("machoire_frein_ard", _("Étrier de frein ARD")),
        ("support_machoire_av", _("Support étrier avant")),
        ("support_machoire_ar", _("Support étrier arrière")),
        ("kit_reparation_machoire", _("Kit réparation étrier")),
        ("plaquettes_av", _("Plaquettes AV")),
        ("plaquettes_ar", _("Plaquettes AR")),
        ("disques_av", _("Disques AV")),
        ("disques_ar", _("Disques AR")),
        ("epaisseur_av", _("Épaisseur AV")),
        ("epaisseur_ar", _("Épaisseur AR")),
        ("epaisseur_min_av", _("Épaisseur min AV")),
        ("epaisseur_min_ar", _("Épaisseur min AR")),
        ("porte_etrier", _("Porte étrier")),
        ("pompe_abs", _("Pompe ABS")),
        ("liquide_qualite", _("Liquide qualité")),
        ("servo_frein", _("Servo-frein")),
        ("maitre_cylindre", _("Maître-cylindre")),
        ("cylindre_recepteur", _("Cylindre récepteur AV/AR G/D")),
        ("petites_fournitures", _("Petites fournitures freins")),
        ("graisse", _("Graisse")),
        ("soufflet", _("Soufflet")),
        ("coulisseaux", _("Coulisseaux")),
        ("visserie", _("Visserie")),
        ("flexibles", _("Flexibles")),
        ("tuyau", _("Tuyau")),
        ("nippe", _("Nippe")),
        ("master_vac", _("Master vac")),
        ("ressort_av", _("Ressort avant")),
        ("ressort_ar", _("Ressort arrière")),
        ("temoin_usure_av", _("Témoin usure avant")),
        ("temoin_usure_ar", _("Témoin usure arrière")),
        ("cable_frein", _("Cable frein à main")),
    )

    type_piece_frein = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_FREINAGE,
        verbose_name=_("Type de pièce de freinage")
    )

    # 🔗 compatibilité moteur (optionnel)
    moteurs_compatibles = models.ManyToManyField(
        "voiture_moteur.MoteurVoiture",
        related_name="freinages",
        blank=True,
        verbose_name=_("Moteurs compatibles")
    )

    class Meta:
        verbose_name = _("Pièce de freinage")
        verbose_name_plural = _("Pièces de freinage")

    def __str__(self):
        return _("%(type)s – %(piece)s") % {
            "type": self.get_type_piece_frein_display(),
            "piece": super().__str__()
        }
