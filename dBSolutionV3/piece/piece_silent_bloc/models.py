from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PieceSilentBloc(Piece):

    TYPE_PIECE_SILENT_BLOC = (

        # 🚗 Suspension / trains
        ("silent_bloc_triangle_sup", _("Silent-bloc de triangle supérieur")),
        ("silent_bloc_triangle_inf", _("Silent-bloc de triangle inférieur")),
        ("silent_bloc_bras_suspension", _("Silent-bloc de bras de suspension")),
        ("silent_bloc_train_av", _("Silent-bloc de train avant")),
        ("silent_bloc_train_ar", _("Silent-bloc de train arrière")),
        ("silent_bloc_barre_stab", _("Silent-bloc de barre stabilisatrice")),
        ("silent_bloc_berceau", _("Silent-bloc de berceau")),
        ("silent_bloc_pont", _("Silent-bloc de pont")),

        # ⚙️ Transmission
        ("silent_bloc_boite", _("Silent-bloc de boîte de vitesses")),
        ("silent_bloc_transmission", _("Silent-bloc de transmission")),
        ("silent_bloc_arbre_transmission", _("Silent-bloc d’arbre de transmission")),

        # 🔩 Moteur
        ("silent_bloc_moteur", _("Silent-bloc moteur")),
        ("support_moteur", _("Support moteur")),
        ("support_boite", _("Support de boîte")),

        # 🚙 Châssis / carrosserie
        ("silent_bloc_chassis", _("Silent-bloc de châssis")),
        ("silent_bloc_carrosserie", _("Silent-bloc de carrosserie")),
        ("silent_bloc_echappement", _("Silent-bloc d’échappement")),
        ("silent_bloc_direction", _("Silent-bloc de direction")),

        # 🧰 Kits
        ("kit_silent_bloc", _("Kit de silent-blocs")),
        ("kit_silent_bloc_train_av", _("Kit silent-blocs train avant")),
        ("kit_silent_bloc_train_ar", _("Kit silent-blocs train arrière")),
    )

    type_piece_silent_bloc = models.CharField(
        max_length=70,
        choices=TYPE_PIECE_SILENT_BLOC,
        verbose_name=_("Type de silent-bloc")
    )

    # 🔗 compatibilité modèle voiture
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pieces_silent_bloc",
        blank=True
    )

    class Meta:
        verbose_name = _("Silent-bloc")
        verbose_name_plural = _("Silent-blocs")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_silent_bloc_display(),
            "nom": super().__str__()
        }
