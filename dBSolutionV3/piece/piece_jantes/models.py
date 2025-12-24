from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class PieceJante(Piece):

    largeur = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        help_text=_("Largeur en pouces, ex: 7, 7.5, 8")
    )
    taille = models.PositiveIntegerField(
        help_text=_("Diamètre en pouces")
    )
    entraxe = models.CharField(
        max_length=20,
        help_text=_("Ex: 5x100")
    )
    alesage = models.PositiveIntegerField(
        help_text=_("Diamètre central en mm")
    )
    deport_et = models.IntegerField(
        help_text=_("Déport ET en mm")
    )

    class Meta:
        verbose_name = _("Jante")
        verbose_name_plural = _("Jantes")

    def __str__(self):
        return _("Jante %(largeur)sx%(taille)s ET%(et)s - %(entraxe)s") % {
            "largeur": self.largeur,
            "taille": self.taille,
            "et": self.deport_et,
            "entraxe": self.entraxe
        }
