from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class TypeFiltre(models.TextChoices):
    AIR = "AIR", _("Filtre à air")
    HUILE = "HUILE", _("Filtre à huile")
    CARBURANT = "CARBURANT", _("Filtre à carburant")
    POLLEN = "POLLEN", _("Filtre à pollen")


class Filtre(Piece):
    type_filtre = models.CharField(
        max_length=20,
        choices=TypeFiltre.choices,
        verbose_name=_("Type de filtre")
    )
    nom_filtre = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Nom du filtre")
    )

    class Meta:
        verbose_name = _("Filtre")
        verbose_name_plural = _("Filtres")

    def __str__(self):
        return _("%(nom)s (%(type)s)") % {
            "nom": self.nom_filtre or _("Filtre"),
            "type": self.get_type_filtre_display()
        }
