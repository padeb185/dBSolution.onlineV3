from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from fournisseur.models import Fournisseur
from decimal import Decimal
from achat_mds.comptabilite import FactureAchatMixin
from achat_mds.documents import DocumentAchatModel

class Outillage(FactureAchatMixin, DocumentAchatModel):
    # Outillage : compte de charge propre (à adapter au plan comptable ;
    # un outillage durable au-delà du seuil d'immobilisation va en 230000)
    COMPTE_ACHATS = "613000"
    LIBELLE_COMPTE_ACHATS = _("Outillage")
    COMPTE_TRANSPORT = "613000"
    LIBELLE_COMPTE_TRANSPORT = _("Outillage – frais de transport")

    id_outillage = models.AutoField(
        primary_key=True,
        verbose_name=_("Identifiant")
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="outillage",
        null=True,
        blank=True,
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

    date_facture = models.DateField(
        default=timezone.localdate,
        verbose_name=_("Date de la facture")
    )

    # Facture fournisseur (mêmes propriétés que les achats MDS)
    reference_facture = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Référence facture"),
    )

    transport_montant_htva = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Montant HTVA du transport"),
    )

    transport_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Taux de TVA du transport (%)"),
        help_text=_("Laisser vide : même taux que la marchandise (frais accessoires facturés par le fournisseur)."),
    )

    date_paiement = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Date de paiement"),
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_("Mis à jour le"),default=timezone.now, editable=False)

    class Meta:
        verbose_name = _("Outillage")
        verbose_name_plural = _("Outillages")

    # Interface FactureAchatMixin
    @property
    def achat_montant_htva(self):
        return (Decimal(self.prix_htva or 0) * Decimal(self.quantite or 0)).quantize(Decimal("0.01"))

    @property
    def achat_tva(self):
        return self.taux_tva

    def save(self, *args, **kwargs):
        # Montant TVAC (outillage + transport) et TVA à récupérer
        self.montant_calcule = self.total_tvac
        self.tva_a_recuperer = self.montant_tva
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        ref = self.reference or _("Sans référence")
        return _("%(libelle)s (%(reference)s) – %(quantite)s pcs") % {
            "libelle": self.libelle,
            "reference": ref,
            "quantite": self.quantite,
        }