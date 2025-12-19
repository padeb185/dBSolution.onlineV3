import uuid
from django.db import models
from societe_cliente.models import SocieteCliente
from adresse.models import Adresse
from fournisseur.models import Fournisseur
from client.models import Client




class Company(models.Model):
    id_company = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    societe = models.ForeignKey(
        SocieteCliente,
        on_delete=models.PROTECT,
        related_name="companies"
    )

    adresse = models.ForeignKey(
        Adresse,
        on_delete=models.PROTECT,
        related_name="companies"
    )

    peppol_id = models.CharField(
        max_length=50,
        help_text="Ex: 0208:BE0123456789"
    )

    code_pays = models.CharField(
        max_length=2,
        default="BE"
    )

    def __str__(self):
        return f"{self.societe} ({self.peppol_id})"




class Invoice(models.Model):
    id_invoice = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    numero = models.CharField(
        max_length=50,
        unique=True
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="invoices"
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name="sales"
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="purchases"
    )

    issue_date = models.DateField()
    currency = models.CharField(max_length=3, default="EUR")

    def __str__(self):
        return self.numero






class InvoiceLine(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        related_name="lines",
        on_delete=models.CASCADE
    )

    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    vat_rate = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Taux TVA: 6, 12, 21"
    )

    def __str__(self):
        return f"{self.description} ({self.invoice.numero})"







