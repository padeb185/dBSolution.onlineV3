from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PiecePont(Piece):

    TYPE_PIECE_PONT = (

        # ⚙️ Pont / différentiel complets
        ("pont_av", _("Pont avant")),
        ("pont_ar", _("Pont arrière")),
        ("pont_central", _("Pont central")),
        ("differentiel_complet", _("Différentiel complet")),

        # 🦷 Engrenages
        ("couronne", _("Couronne")),
        ("pignon_attaque", _("Pignon d’attaque")),
        ("couple_conique", _("Couple conique")),
        ("satellite", _("Satellite")),
        ("planetaire", _("Planétaire")),
        ("axe_satellite", _("Axe de satellite")),

        # ⚙️ Carter et structure
        ("carter_pont", _("Carter de pont")),
        ("couvercle_pont", _("Couvercle de pont")),
        ("bouchon_vidange", _("Bouchon de vidange")),
        ("bouchon_remplissage", _("Bouchon de remplissage")),
        ("reniflard", _("Reniflard de pont")),

        # 🔩 Roulements et calage
        ("roulement_pignon", _("Roulement de pignon")),
        ("roulement_differentiel", _("Roulement de différentiel")),
        ("cage_roulement", _("Cage de roulement")),
        ("cale_reglage", _("Cale de réglage")),
        ("entretoise", _("Entretoise")),

        # 🧴 Étanchéité
        ("joint_spy", _("Joint spi")),
        ("joint_carter", _("Joint de carter")),
        ("joint_etancheite", _("Joint d’étanchéité")),

        # 🔧 Fixation
        ("bride_pont", _("Bride de pont")),
        ("vis_couronne", _("Vis de couronne")),
        ("boulonnerie_pont", _("Boulonnerie de pont")),

        # 🧰 Kits
        ("kit_roulements_pont", _("Kit roulements de pont")),
        ("kit_joints_pont", _("Kit joints de pont")),
        ("kit_revision_pont", _("Kit révision de pont")),
    )

    type_piece_pont = models.CharField(
        max_length=60,
        choices=TYPE_PIECE_PONT,
        verbose_name=_("Type de pièce de pont")
    )

    # 🔗 compatibilité modèle voiture
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pieces_pont",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce de pont")
        verbose_name_plural = _("Pièces de pont")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_pont_display(),
            "nom": super().__str__()
        }
