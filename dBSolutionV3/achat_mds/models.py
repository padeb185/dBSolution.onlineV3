import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _

from .comptabilite import FactureAchatMixin
from .documents import DocumentAchatModel



class AchatMds(FactureAchatMixin, DocumentAchatModel):
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

    transport_montant_htva = models.DecimalField(
        _("Montant HTVA du transport"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    achat_tva = models.DecimalField(
        _("Taux de TVA (%)"),
        max_digits=5,
        decimal_places=2,
        default=21.00
    )

    # Frais de transport : taux propre si différent de celui de la marchandise
    # (vide = même taux que l'achat, cas des frais accessoires facturés par le fournisseur)
    transport_tva = models.DecimalField(
        _("Taux de TVA du transport (%)"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Laisser vide : même taux que la marchandise (frais accessoires facturés par le fournisseur)."),
    )

    date_facture = models.DateField(
        _("Date de la facture")
    )

    date_paiement = models.DateField(
        _("Date de paiement"),
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
        prefixe = "Achat" if self.est_facture else self.libelle_document
        ref = f" {self.reference_facture}" if self.reference_facture else ""
        return f"{prefixe} {self.fournisseur.nom}{ref} - {self.date_facture}"

    # ------------------------
    # CALCULS FINANCIERS
    # ------------------------
    # Montants, TVA (marchandise + transport) et écritures : voir achat_mds/comptabilite.py
