import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _



class AchatMds(models.Model):
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="achats_mds",
        null=True,
        blank=True,
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    fournisseur = models.ForeignKey(
        "fournisseur.Fournisseur",
        on_delete=models.CASCADE,
        related_name="achats",
        verbose_name=_("Fournisseur")
    )

    libelle_facture = models.CharField(
        _("Libellé"),
        max_length=100,
        blank=True,
        null=True
    )

    reference_facture = models.CharField(
        _("Référence facture"),
        max_length=100,
        blank=True,
        null=True
    )

    achat_montant_htva = models.DecimalField(
        _("Montant HTVA"),
        max_digits=10,
        decimal_places=2
    )

    achat_tva = models.DecimalField(
        _("Taux de TVA (%)"),
        max_digits=5,
        decimal_places=2,
        default=21.00
    )

    date_facture = models.DateField(
        _("Date facture")
    )

    date_paiement = models.DateField(
        _("Date paiement"),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Achat")
        verbose_name_plural = _("Achats")
        ordering = ["-date_facture"]

    def __str__(self):
        return f"Achat {self.fournisseur.nom} - {self.date_facture}"

    # ------------------------
    # CALCULS FINANCIERS
    # ------------------------

    @property
    def montant_tva(self):
        if not self.achat_montant_htva:
            return Decimal("0.00")

        return self.achat_montant_htva * self.achat_tva / Decimal("100")

    @property
    def total_tvac(self):
        if not self.achat_montant_htva:
            return Decimal("0.00")

        return self.achat_montant_htva + self.montant_tva