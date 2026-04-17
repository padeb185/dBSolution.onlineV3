import uuid
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _



class Fournisseur(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="fournisseurs",
        null=True,
        blank=True,
    )

    nom = models.CharField(
        _("Nom du fournisseur"),
        max_length=200,
        unique=True
    )

    adresse = models.ForeignKey(
        "adresse.Adresse",
        verbose_name=_("Adresse"),
        on_delete=models.CASCADE
    )

    numero_tva = models.CharField(
        _("Numéro de TVA"),
        max_length=20,
        unique=True
    )

    taux_tva = models.DecimalField(
        _("Taux de TVA (%)"),
        max_digits=5,
        decimal_places=2,
        default=21.00
    )

    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Identifiant Peppol, ex : 0208:BE0123456789")
    )

    country_code = models.CharField(
        _("Code pays"),
        max_length=2,
        default="BE",
        help_text=_("ISO 3166-1 alpha-2"),
        null=True,
        blank=True
    )

    email = models.EmailField(
        _("Email"),
        max_length=254,
        blank=True,
        null=True,
        help_text=_("Email du fournisseur")
    )

    telephone_fixe = models.CharField(
        _("Téléphone fixe"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Numéro de téléphone fixe")
    )

    gsm = models.CharField(
        _("GSM"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Numéro de téléphone mobile")
    )

    # --- Métadonnées ---

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Fournisseur")
        verbose_name_plural = _("Fournisseurs")
        indexes = [
            models.Index(fields=["numero_tva"]),
            models.Index(fields=["peppol_id"]),
        ]

    def __str__(self):
        return _("%(nom)s (Fournisseur)") % {"nom": self.nom}

    @property
    def peppol_scheme(self):
        return self.peppol_id.split(":")[0]

    @property
    def peppol_value(self):
        return self.peppol_id.split(":")[1]





class Achat(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    fournisseur = models.ForeignKey(
        "fournisseur.Fournisseur",
        on_delete=models.CASCADE,
        related_name="achats",
        verbose_name=_("Fournisseur")
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
        _("Taux TVA (%)"),
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