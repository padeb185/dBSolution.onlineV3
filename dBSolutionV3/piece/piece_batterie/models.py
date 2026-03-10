from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PieceBatterie(Piece):

    TYPE_PIECE_BATTERIE = (

        # 🔋 Batteries
        ("batterie_12v", _("Batterie 12V")),
        ("batterie_agm", _("Batterie AGM")),
        ("batterie_eFB", _("Batterie EFB")),
        ("batterie_lithium", _("Batterie lithium")),
        ("batterie_haute_tension", _("Batterie haute tension (hybride/électrique)")),

        # ⚡ Gestion et sécurité
        ("capteur_batterie", _("Capteur de batterie (IBS)")),
        ("boitier_batterie", _("Boîtier de batterie")),
        ("cache_batterie", _("Cache batterie")),
        ("systeme_maintien_batterie", _("Système de maintien batterie")),

        # 🔩 Connexions et câblage
        ("cosse_batterie_pos", _("Cosse batterie positive")),
        ("cosse_batterie_neg", _("Cosse batterie négative")),
        ("cable_batterie", _("Câble de batterie")),
        ("borne_batterie", _("Borne de batterie")),
        ("fusible_batterie", _("Fusible batterie")),
        ("porte_fusible_batterie", _("Porte-fusible batterie")),

        # 🧰 Fixation
        ("bride_batterie", _("Bride de batterie")),
        ("support_batterie", _("Support de batterie")),
        ("vis_fixation_batterie", _("Vis de fixation batterie")),

        # 🧴 Isolation et protection
        ("gaine_protection", _("Gaine de protection")),
        ("isolant_batterie", _("Isolant de batterie")),
        ("tapis_batterie", _("Tapis de batterie")),

        # 🧰 Kits
        ("kit_fixation_batterie", _("Kit fixation batterie")),
        ("kit_cosses_batterie", _("Kit cosses batterie")),
        ("kit_cables_batterie", _("Kit câbles batterie")),
    )

    type_piece_batterie = models.CharField(
        max_length=70,
        choices=TYPE_PIECE_BATTERIE,
        verbose_name=_("Type de pièce batterie")
    )

    # 🔗 compatibilité modèle voiture
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pieces_batterie",
        blank=True
    )

    amperage = models.IntegerField(
        default=0,
        verbose_name=_("Amperage"),
        help_text=_("Ampèrage Maximum")
    )

    ampere_heures = models.IntegerField(
        default=0,
        verbose_name=_("Ampere heures"),
    )

    class Meta:
        verbose_name = _("Pièce de batterie")
        verbose_name_plural = _("Pièces de batterie")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_batterie_display(),
            "nom": super().__str__()
        }
