from django.db import models
from django.utils.translation import gettext_lazy as _
from fournisseur.models import Fournisseur


class Outillage(models.Model):
    id_outillage = models.AutoField(
        primary_key=True,
        verbose_name=_("Identifiant")
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.CASCADE,
        related_name="outillages",
        verbose_name=_("Fournisseur")
    )

    libelle = models.CharField(
        max_length=255,
        verbose_name=_("Libellé")
    )

    reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence")
    )

    quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    prix_htva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix HTVA")
    )

    taux_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=21.00,
        verbose_name=_("Taux de TVA (%)")
    )

    montant_calcule = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        verbose_name=_("Montant calculé")
    )

    tva_a_recuperer = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        verbose_name=_("TVA à récupérer")
    )

    class Meta:
        verbose_name = _("Outillage")
        verbose_name_plural = _("Outillages")

    def save(self, *args, **kwargs):
        # Calcul automatique du montant total et de la TVA à récupérer
        self.montant_calcule = self.prix_htva * self.quantite
        self.tva_a_recuperer = self.montant_calcule * (self.taux_tva / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        ref = self.reference or _("Sans référence")
        return _("%(libelle)s (%(reference)s) – %(quantite)s pcs") % {
            "libelle": self.libelle,
            "reference": ref,
            "quantite": self.quantite,
        }
