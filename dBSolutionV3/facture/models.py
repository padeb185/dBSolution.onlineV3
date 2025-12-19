import uuid
from django.db import models
from societe_cliente.models import SocieteCliente
from adresse.models import Adresse

from dBSolutionV3.fournisseur.models import Fournisseur


class Company(models.Model):
     id_company = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
     )
     company= models.ForeignKey(
        SocieteCliente,
        on_delete=models.PROTECT,  # comportement à la suppression
        related_name='company'  # pour accéder aux sociétés clientes depuis la société
     )
     adresse = models.ForeignKey(
         Adresse,
         on_delete=models.PROTECT,
         related_name='sociétés_clientes'
     )
     peppol_id = models.CharField(max_length=50)  # ex: 0208:BE0123456789
     country_code = models.CharField(max_length=2, default="BE")



class Invoice(models.Model):
    id_invoice = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    number = models.CharField(max_length=50)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, related_name="sales")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="purchases")
    issue_date = models.DateField()
    currency = models.CharField(max_length=3, default="EUR")






class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="lines", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=4, decimal_places=2)  # 6, 12, 21








