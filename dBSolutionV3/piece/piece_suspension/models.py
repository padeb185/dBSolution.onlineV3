from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class PieceSuspension(Piece):

    TYPE_PIECE_SUSPENSION = (
        ("amortisseur_av", _("Amortisseur avant")),
        ("amortisseur_ar", _("Amortisseur arrière")),
        ("amortisseur_gd", _("Amortisseur G/D")),
        ("ressort_av", _("Ressort avant")),
        ("ressort_ar", _("Ressort arrière")),
        ("coupelle_amortisseur", _("Coupelle d’amortisseur")),
        ("butée_suspension", _("Butée de suspension")),
        ("soufflet_amortisseur", _("Soufflet d’amortisseur")),
        ("silent_bloc_suspension", _("Silent bloc de suspension")),
        ("kit_suspension", _("Kit de suspension")),
        ("cales_ressort", _("Cales de ressort")),
        ("correcteur_assiette", _("Correcteur d’assiette")),
        ("suspension_hydraulique", _("Suspension hydraulique")),
        ("suspension_pneumatique", _("Suspension pneumatique")),
    )

    type_piece_suspension = models.CharField(
        max_length=50,
        choices=TYPE_PIECE_SUSPENSION,
        verbose_name=_("Type de pièce suspension")
    )

    # 🔗 compatibilité modèle voiture
    voiture_modele = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="pieces_suspension",
        blank=True
    )

    class Meta:
        verbose_name = _("Pièce de suspension")
        verbose_name_plural = _("Pièces de suspension")

    def __str__(self):
        return _("%(type)s – %(nom)s") % {
            "type": self.get_type_piece_suspension_display(),
            "nom": super().__str__()
        }
