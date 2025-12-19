from django.db import models
import uuid
from django_tenants.models import TenantMixin, DomainMixin

from adresse.models import Adresse


class Societe(TenantMixin):
    # Champs obligatoires pour django-tenants
    slug = models.SlugField(unique=True)
    paid_until = models.DateField()
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True  # crée automatiquement le schéma

    # Champs spécifiques à ta société
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
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
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


class Domain(DomainMixin):
    pass
