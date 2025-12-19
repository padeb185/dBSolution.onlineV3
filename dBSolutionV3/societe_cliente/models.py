from django.db import models
import uuid
from societe.models import Societe
from adresse.models import Adresse


class SocieteCliente(models.Model):
    id_societe_cliente = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,  # comportement à la suppression
        related_name='societe_cliente'  #  pour accéder aux sociétés clientes depuis la société
    )

    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la société"
    )
    adresse = models.ForeignKey(
        Adresse,
        on_delete=models.PROTECT,
        related_name='sociétés_clientes'
    )

    directeur = models.CharField(
        max_length=100,
        verbose_name="Directeur"
    )
    numero_tva = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Numéro de TVA"
    )
    site = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Site web"
    )

    class Meta:
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"
        ordering = ['nom']

    def __str__(self):
        return self.nom
