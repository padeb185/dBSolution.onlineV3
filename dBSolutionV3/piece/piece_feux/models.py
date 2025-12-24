from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Feux(Piece):

    POSITIONS = [
        ("AVG", _("Avant Gauche")),
        ("AVD", _("Avant Droit")),
        ("ARG", _("Arrière Gauche")),
        ("ARD", _("Arrière Droit")),
        ("STOP", _("Troisième feu stop")),
        ("AB_AV", _("Antibrouillard AV")),
        ("AB_AR", _("Antibrouillard AR")),
        ("CL_AVG", _("Clignotant Avant Gauche")),
        ("CL_AVD", _("Clignotant Avant Droit")),
        ("CL_ARG", _("Clignotant Arrière Gauche")),
        ("CL_ARD", _("Clignotant Arrière Droit")),
    ]

    type_feu = models.CharField(
        max_length=20,
        choices=POSITIONS,
        verbose_name=_("Type / Position du feu")
    )

    puissance = models.CharField(max_length=20, blank=True, verbose_name=_("Puissance"))
    couleur = models.CharField(max_length=20, blank=True, verbose_name=_("Couleur"))

    class Meta:
        verbose_name = _("Feu")
        verbose_name_plural = _("Feux")

    def __str__(self):
        return _("%(organe)s - %(type)s") % {
            "organe": self.organe or _("Feu"),
            "type": self.get_type_feu_display()
        }
