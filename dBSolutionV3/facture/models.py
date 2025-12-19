import uuid
from django.db import models
from adresse.models import Adresse
from client.models import Client
from societe.models import Societe
from societe_cliente.models import SocieteCliente


class Company(models.Model):
    """Émettrice de la facture"""
    id_company = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey(Societe, on_delete=models.PROTECT, related_name="companies", blank=True, null=True)
    adresse = models.ForeignKey(Adresse, on_delete=models.PROTECT, related_name="companies")
    peppol_id = models.CharField(max_length=50, help_text="Ex: 0208:BE0123456789")
    code_pays = models.CharField(max_length=2, default="BE")

    def __str__(self):
        return f"{self.societe} ({self.peppol_id})"


class Facture(models.Model):
    """Facture émise par Company à un Client"""
    id_facture = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.CharField(max_length=50, unique=True)

    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="invoices")
    societe_cliente = models.ForeignKey(SocieteCliente, on_delete=models.PROTECT, related_name="purchases")

    issue_date = models.DateField()
    currency = models.CharField(max_length=3, default="EUR")
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.numero


class FactureLine(models.Model):
    facture = models.ForeignKey(Facture, related_name="lines", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2, help_text="Taux TVA: 6, 12, 21")

    def __str__(self):
        return f"{self.description} ({self.facture.numero})"



