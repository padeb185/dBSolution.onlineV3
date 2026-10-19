"""
Factures d'achat fournisseurs (achats MDS, outillage…) : calculs TVA (marchandise + transport)
et écritures du journal des achats (PCMN belge). Partagé par AchatMds et Outillage.

Le modèle doit fournir : fournisseur, reference_facture, date_facture, date_paiement,
achat_montant_htva, achat_tva, transport_montant_htva, transport_tva.
"""
from decimal import Decimal

from django.utils.translation import gettext_lazy as _

R2 = Decimal("0.01")


def _r(x):
    return Decimal(x or 0).quantize(R2)


class FactureAchatMixin:
    COMPTE_ACHATS = "604000"
    LIBELLE_COMPTE_ACHATS = _("Achats de marchandises / pièces")
    COMPTE_TRANSPORT = "604100"
    LIBELLE_COMPTE_TRANSPORT = _("Frais accessoires d'achat – transport")
    COMPTE_TVA = "411000"
    COMPTE_FOURNISSEURS = "440000"
    COMPTE_BANQUE = "550000"

    # ------------------------ montants ------------------------
    @property
    def montant_htva_total(self):
        return _r(self.achat_montant_htva) + _r(self.transport_montant_htva)

    @property
    def taux_tva_transport(self):
        return self.transport_tva if self.transport_tva is not None else (self.achat_tva or Decimal("0"))

    @property
    def montant_tva_achat(self):
        return (Decimal(self.achat_montant_htva or 0) * Decimal(self.achat_tva or 0) / Decimal("100")).quantize(R2)

    @property
    def montant_tva_transport(self):
        return (Decimal(self.transport_montant_htva or 0) * Decimal(self.taux_tva_transport) / Decimal("100")).quantize(R2)

    @property
    def montant_tva(self):
        return self.montant_tva_achat + self.montant_tva_transport

    @property
    def total_tvac(self):
        return self.montant_htva_total + self.montant_tva

    @property
    def est_paye(self):
        return self.date_paiement is not None

    # ------------------------ journal ------------------------
    def ecritures_comptables(self, deductible_achat=Decimal("100"), deductible_transport=Decimal("100"), avec_paiement=True):
        """
        Journal des achats :
          - marchandise HTVA → COMPTE_ACHATS ; transport HTVA → COMPTE_TRANSPORT
            (frais accessoires d'achat, incorporés au coût – art. 35 AR 30/01/2001) ;
          - TVA déductible → 411000 ; la part non déductible s'ajoute à la charge ;
          - total TVAC → 440000 fournisseur ; paiement : 440000 / 550000.
        """
        z = Decimal("0.00")
        lib = f"{self.fournisseur.nom} {self.reference_facture or ''}".strip()

        tva_achat_ded = _r(self.montant_tva_achat * Decimal(deductible_achat) / Decimal("100"))
        tva_transport_ded = _r(self.montant_tva_transport * Decimal(deductible_transport) / Decimal("100"))
        charge_achat = _r(Decimal(self.achat_montant_htva or 0) + self.montant_tva_achat - tva_achat_ded)
        charge_transport = _r(Decimal(self.transport_montant_htva or 0) + self.montant_tva_transport - tva_transport_ded)

        lignes = []

        def ligne(journal, jour, compte, intitule, debit=z, credit=z):
            if debit or credit:
                lignes.append({"journal": journal, "date": jour, "compte": compte, "intitule": intitule,
                               "libelle": lib, "debit": _r(debit), "credit": _r(credit)})

        ligne("ACH", self.date_facture, self.COMPTE_ACHATS, self.LIBELLE_COMPTE_ACHATS, debit=charge_achat)
        ligne("ACH", self.date_facture, self.COMPTE_TRANSPORT, self.LIBELLE_COMPTE_TRANSPORT, debit=charge_transport)
        ligne("ACH", self.date_facture, self.COMPTE_TVA, _("TVA à récupérer"), debit=tva_achat_ded + tva_transport_ded)
        ligne("ACH", self.date_facture, self.COMPTE_FOURNISSEURS, _("Fournisseurs"), credit=self.total_tvac)
        if avec_paiement and self.date_paiement:
            ligne("BQE", self.date_paiement, self.COMPTE_FOURNISSEURS, _("Fournisseurs"), debit=self.total_tvac)
            ligne("BQE", self.date_paiement, self.COMPTE_BANQUE, _("Banque – compte courant"), credit=self.total_tvac)
        return lignes
