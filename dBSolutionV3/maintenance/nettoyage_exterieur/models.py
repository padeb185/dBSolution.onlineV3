from django.db import models
from django.utils.translation import gettext_lazy as _
from utilisateurs.models import Utilisateur
from maintenance.models import Maintenance

class NettoyageExterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Check up")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_exterieur",
        verbose_name=_("Véhicule")
    )

    mecanicien = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="nettoyage_exterieur",
        verbose_name=_("Mécanicien")
    )

    traces_gomme = models.BooleanField(default=False, verbose_name=_("Traces de gomme"))
    carrosserie = models.BooleanField(default=False, verbose_name=_("Carrosserie"))
    jantes = models.BooleanField(default=False, verbose_name=_("Jantes"))

    validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage extérieur")
        verbose_name_plural = _("Nettoyages extérieurs")

    def __str__(self):
        return f"Nettoyage extérieur – {self.vehicule} ({self.date:%Y-%m-%d})"
