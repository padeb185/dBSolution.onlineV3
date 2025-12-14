from django.db import models
import uuid

class Societe(models.Model):
    id_societe = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nom de la société"
    )
    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.PROTECT,
        related_name='societes'
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
