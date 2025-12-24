from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class PieceRoueRechange(Piece):

    SITES_CHOICES = [
        ('BE', _('Belgique')),
        ('GE', _('Allemagne')),
        ('O', _('Autre')),
    ]
    SIDE_CHOICES = [
        ('AV', _('Avant')),
        ('AR', _('Arrière')),
    ]
    TYPE_CHOICES = [
        ('SLICK', _('Slick')),
        ('SEMI-SLICK', _('Semi-slick')),
        ('PLUIE', _('Pluie')),
        ('NEIGE', _('Neige')),
    ]

    sites = models.CharField(max_length=20, choices=SITES_CHOICES, verbose_name=_("Site"))
    side = models.CharField(max_length=20, choices=SIDE_CHOICES, verbose_name=_("Côté"))
    type_roue = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("Type de roue"))
    quantite = models.PositiveIntegerField(default=1, verbose_name=_("Quantité"))

    class Meta:
        verbose_name = _("Roue de rechange")
        verbose_name_plural = _("Roues de rechange")

    def __str__(self):
        return _("%(quantite)s roue(s) %(type)s sur %(site)s") % {
            "quantite": self.quantite,
            "type": self.get_type_roue_display(),
            "site": self.get_sites_display()
        }
