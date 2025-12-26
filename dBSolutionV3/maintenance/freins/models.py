from django.db import models
from django.utils.translation import gettext_lazy as _



class PartieFrein(models.TextChoices):
    AVANT = "AVANT", _("Avant")
    ARRIERE = "ARRIERE", _("Arrière")
    AVANT_AR = "AV_AR", _("Avant et arrière")


class ControleFreins(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="controles_freins",
        verbose_name=_("Maintenance")
    )

    partie = models.CharField(
        max_length=10,
        choices=PartieFrein.choices,
        verbose_name=_("Partie contrôlée")
    )

    # Plaquettes
    usure_plaquettes = models.FloatField(
        verbose_name=_("Usure des plaquettes (%)")
    )

    # Disques
    epaisseur_disques = models.FloatField(
        verbose_name=_("Épaisseur des disques (mm)")
    )
    fentes_disques = models.BooleanField(
        default=False,
        verbose_name=_("Présence de fentes sur les disques")
    )

    # Fuites
    fuites = models.BooleanField(
        default=False,
        verbose_name=_("Présence de fuite")
    )

    # Remplacement
    a_remplacer_av = models.BooleanField(
        default=False,
        verbose_name=_("À remplacer avant")
    )
    a_remplacer_ar = models.BooleanField(
        default=False,
        verbose_name=_("À remplacer arrière")
    )

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return _(
            "Contrôle freins – %(partie)s (%(date)s)"
        ) % {
            "partie": self.get_partie_display(),
            "date": self.date.strftime("%Y-%m-%d %H:%M")
        }

    def plaque_critique(self, seuil_usure=30):
        """Retourne True si les plaquettes sont trop usées (critique)."""
        return self.usure_plaquettes >= seuil_usure

    def disque_critique(self, epaisseur_min=20):
        """Retourne True si les disques sont trop fins ou fendus."""
        return self.epaisseur_disques <= epaisseur_min or self.fentes_disques

    def fuite_critique(self):
        """Retourne True si une fuite est détectée."""
        return self.fuites

    def is_critique(self):
        """Retourne True si l'une des conditions critiques est remplie."""
        return self.plaque_critique() or self.disque_critique() or self.fuite_critique()
