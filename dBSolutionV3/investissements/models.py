from django.db import models
from django.utils.translation import gettext_lazy as _
from fournisseur.models import Fournisseur


class Investissement(models.Model):
    id_investissement = models.AutoField(primary_key=True)

    fournisseur = models.ForeignKey(
        Fournisseur,
        verbose_name=_("Fournisseur"),
        on_delete=models.CASCADE,
        related_name="investissements"
    )

    # Libellé de l'investissement
    class Libelle(models.TextChoices):
        PONT = "PONT", _("Pont")
        MACHINE_GEOMETRIE = "MACHINE_GEOMETRIE", _("Machine de géométrie")
        MACHINE_PNEUS = "MACHINE_PNEUS", _("Machine à pneus")
        EQUILIBREUSE = "EQUILIBREUSE", _("Équilibreuse")
        COMPRESSEUR = "COMPRESSEUR", _("Compresseur")
        BOOSTER_BATTERIE = "BOOSTER_BATTERIE", _("Booster batterie")
        BOOSTER_PNEUS = "BOOSTER_PNEUS", _("Booster pneus")
        TUYAUX_AIR = "TUYAUX_AIR", _("Tuyaux pression d’air")
        CONNECTEURS = "CONNECTEURS", _("Connecteurs")
        MOBILIER = "MOBILIER", _("Mobilier")
        ORDINATEUR = "ORDINATEUR", _("Ordinateur")
        APPAREIL_DIAGNOSTIC = "APPAREIL_DIAGNOSTIC", _("Appareil de diagnostic")

    libelle = models.CharField(
        _("Libellé"),
        max_length=50,
        choices=Libelle.choices
    )

    # Détails de l'investissement
    details = models.TextField(_("Détails"), blank=True, null=True)

    temps_amortissement = models.PositiveIntegerField(
        _("Durée d'amortissement"),
        help_text=_("Durée d'amortissement en mois ou années")
    )

    # Type d'amortissement
    class TypeAmortissement(models.TextChoices):
        LINEAIRE = "LINEAIRE", _("Linéaire")
        DEGRESSIF = "DEGRESSIF", _("Dégressif")
        AUTRE = "AUTRE", _("Autre")

    type_amortissement = models.CharField(
        _("Type d'amortissement"),
        max_length=20,
        choices=TypeAmortissement.choices,
        default=TypeAmortissement.LINEAIRE
    )

    class Meta:
        verbose_name = _("Investissement")
        verbose_name_plural = _("Investissements")

    def __str__(self):
        return _("%(libelle)s - Fournisseur: %(fournisseur)s") % {
            "libelle": self.get_libelle_display(),
            "fournisseur": self.fournisseur
        }
