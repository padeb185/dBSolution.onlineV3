from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur


class NettoyageInterieur(models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Check up")
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyages_interieur",
        verbose_name=_("Véhicule")
    )

    mecanicien = models.ForeignKey(
        Utilisateur,
        on_delete=models.PROTECT,
        related_name="nettoyages_interieur",
        verbose_name=_("Mécanicien")
    )

    vitres = models.BooleanField(default=False, verbose_name=_("Vitres"))
    pare_brise = models.BooleanField(default=False, verbose_name=_("Pare-brise"))
    aspirateur = models.BooleanField(default=False, verbose_name=_("Aspirateur"))
    interieur_portes = models.BooleanField(default=False, verbose_name=_("Intérieurs de porte"))
    tableau_de_bord = models.BooleanField(default=False, verbose_name=_("Tableau de bord"))
    plastiques = models.BooleanField(default=False, verbose_name=_("Plastiques"))

    validation = models.BooleanField(default=False, verbose_name=_("Validation finale"))

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Nettoyage intérieur")
        verbose_name_plural = _("Nettoyages intérieurs")

    def __str__(self):
        return f"Nettoyage intérieur – {self.vehicule} ({self.date:%Y-%m-%d})"
