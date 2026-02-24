from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


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
    disque_a_remplacer_av = models.BooleanField(
        default=False,
        verbose_name=_("Disques avant à remplacer")
    )
    disque_a_remplacer_ar = models.BooleanField(
        default=False,
        verbose_name=_("Disques arrière à remplacer")
    )

    plaquettes_a_remplacer_av = models.BooleanField(
        default=False,
        verbose_name=_("Plaquettes avant à remplacer")
    )
    plaquettes_a_remplacer_ar = models.BooleanField(
        default=False,
        verbose_name=_("Plaquettes arrière à  remplacer")
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



class RemplacementFreins(models.Model):
    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="remplacements_freins",
        verbose_name=_("Maintenance")
    )

    piece = models.ForeignKey(
        Piece,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Pièce remplacée"),
        help_text=_("La pièce de frein remplacée, ex : plaquettes, disques, étrier…")
    )

    # Durée en minutes
    duree_remplacement = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Durée de remplacement (minutes)"),
        help_text=_("Temps estimé ou réel pour effectuer le remplacement")
    )

    # Description libre
    description = models.TextField(
        blank=True,
        verbose_name=_("Détails"),
        help_text=_("Notes ou détails supplémentaires sur le remplacement effectué")
    )

    date_remplacement = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de remplacement"))

    class Meta:
        verbose_name = _("Remplacement des freins")
        verbose_name_plural = _("Remplacements des freins")
        ordering = ["-date_remplacement"]

    def __str__(self):
        return _(
            "Remplacement – %(piece)s (%(date)s)"
        ) % {
            "piece": self.piece.nom if self.piece else _("Pièce non spécifiée"),
            "date": self.date_remplacement.strftime("%Y-%m-%d %H:%M")
        }