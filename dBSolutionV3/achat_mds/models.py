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
        return f"Achat {self.fournisseur.nom} - {self.date_facture}"

    # ------------------------
    # CALCULS FINANCIERS
    # ------------------------

    @property
    def montant_htva_total(self):
        return (self.achat_montant_htva or Decimal("0.00")) + (self.transport_montant_htva or Decimal("0.00"))

    @property
    def taux_tva_transport(self):
        return self.transport_tva if self.transport_tva is not None else (self.achat_tva or Decimal("0"))

    @property
    def montant_tva_achat(self):
        return (Decimal(self.achat_montant_htva or 0) * Decimal(self.achat_tva or 0) / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def montant_tva_transport(self):
        return (Decimal(self.transport_montant_htva or 0) * Decimal(self.taux_tva_transport) / Decimal("100")).quantize(Decimal("0.01"))

    @property
    def montant_tva(self):
        return self.montant_tva_achat + self.montant_tva_transport

    @property
    def total_tvac(self):
        return self.montant_htva_total + self.montant_tva

    # ------------------------
    # COMPTABILISATION (PCMN belge)
    # ------------------------
    COMPTE_ACHATS = "604000"
    COMPTE_TRANSPORT = "604100"
    COMPTE_TVA = "411000"
    COMPTE_FOURNISSEURS = "440000"
    COMPTE_BANQUE = "550000"

    def ecritures_comptables(self, deductible_achat=Decimal("100"), deductible_transport=Decimal("100"), avec_paiement=True):
        """
        Journal des achats :
          - marchandises HTVA → 604000 ;
          - frais de transport HTVA → 604100 (frais accessoires d'achat, incorporés au coût
            d'acquisition – art. 35 AR 30/01/2001) ;
          - TVA déductible → 411000 ; la part non déductible s'ajoute à la charge ;
          - total TVAC → 440000 fournisseur ; paiement : 440000 / 550000.
        """
        z = Decimal("0.00")
        r = lambda x: Decimal(x).quantize(Decimal("0.01"))
        lib = f"{self.fournisseur.nom} {self.reference_facture or ''}".strip()

        tva_achat_ded = r(self.montant_tva_achat * Decimal(deductible_achat) / Decimal("100"))
        tva_transport_ded = r(self.montant_tva_transport * Decimal(deductible_transport) / Decimal("100"))
        charge_achat = r(Decimal(self.achat_montant_htva or 0) + self.montant_tva_achat - tva_achat_ded)
        charge_transport = r(Decimal(self.transport_montant_htva or 0) + self.montant_tva_transport - tva_transport_ded)

        lignes = []
        def ligne(journal, compte, intitule, libelle, debit=z, credit=z):
            if debit or credit:
                lignes.append({"journal": journal, "date": self.date_facture, "compte": compte, "intitule": intitule,
                               "libelle": libelle, "debit": r(debit), "credit": r(credit)})

        ligne("ACH", self.COMPTE_ACHATS, _("Achats de marchandises / pièces"), lib, debit=charge_achat)
        ligne("ACH", self.COMPTE_TRANSPORT, _("Frais accessoires d'achat – transport"), lib, debit=charge_transport)
        ligne("ACH", self.COMPTE_TVA, _("TVA à récupérer"), lib, debit=tva_achat_ded + tva_transport_ded)
        ligne("ACH", self.COMPTE_FOURNISSEURS, _("Fournisseurs"), lib, credit=self.total_tvac)
        if avec_paiement and self.date_paiement:
            lignes.append({"journal": "BQE", "date": self.date_paiement, "compte": self.COMPTE_FOURNISSEURS,
                           "intitule": _("Fournisseurs"), "libelle": lib, "debit": r(self.total_tvac), "credit": z})
            lignes.append({"journal": "BQE", "date": self.date_paiement, "compte": self.COMPTE_BANQUE,
                           "intitule": _("Banque – compte courant"), "libelle": lib, "debit": z, "credit": r(self.total_tvac)})
        return lignes