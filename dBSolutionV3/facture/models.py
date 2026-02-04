from adresse.models import Adresse
from societe.models import Societe
from societe_cliente.models import SocieteCliente
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Company(models.Model):
    """
    Société émettrice de la facture (par tenant)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    adresse = models.ForeignKey(
        Adresse,
        verbose_name=_("Adresse"),
        on_delete=models.PROTECT,
        related_name="companies"
    )

    peppol_id = models.CharField(
        _("Identifiant Peppol"),
        max_length=50,
        help_text=_("Ex : 0208:BE0123456789")
    )

    code_pays = models.CharField(
        _("Code pays"),
        max_length=2,
        default="BE"
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Société émettrice")
        verbose_name_plural = _("Sociétés émettrices")

    def __str__(self):
        return self.peppol_id


class Facture(models.Model):
    """Facture émise par une société à un client"""
    id_facture = models.UUIDField(
        _("Identifiant facture"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    numero = models.CharField(
        _("Numéro de facture"),
        max_length=50,
        unique=True
    )

    company = models.ForeignKey(
        Company,
        verbose_name=_("Société émettrice"),
        on_delete=models.PROTECT,
        related_name="invoices"
    )

    societe_cliente = models.ForeignKey(
        SocieteCliente,
        verbose_name=_("Client"),
        on_delete=models.PROTECT,
        related_name="purchases",
        null=True,
        blank=True
    )

    issue_date = models.DateField(_("Date d’émission"))
    currency = models.CharField(_("Devise"), max_length=3, default="EUR")
    total = models.DecimalField(
        _("Total"),
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = _("Facture")
        verbose_name_plural = _("Factures")

    def __str__(self):
        return _("Facture %(numero)s") % {"numero": self.numero}


class FactureLine(models.Model):
    facture = models.ForeignKey(
        Facture,
        verbose_name=_("Facture"),
        related_name="lines",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    description = models.CharField(_("Description"), max_length=255)

    quantity = models.DecimalField(
        _("Quantité"),
        max_digits=10,
        decimal_places=2
    )

    unit_price = models.DecimalField(
        _("Prix unitaire"),
        max_digits=10,
        decimal_places=2
    )

    vat_rate = models.DecimalField(
        _("Taux de TVA"),
        max_digits=4,
        decimal_places=2,
        help_text=_("Taux de TVA : 6, 12, 21")
    )

    class Meta:
        verbose_name = _("Ligne de facture")
        verbose_name_plural = _("Lignes de facture")

    def __str__(self):
        return _("%(desc)s (%(facture)s)") % {
            "desc": self.description,
            "facture": self.facture.numero,
        }
