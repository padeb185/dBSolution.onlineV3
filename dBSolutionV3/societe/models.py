from django.db import models
import uuid
from django.utils.text import slugify
from django_tenants.models import TenantMixin, DomainMixin


class Societe(TenantMixin):
    # Champs obligatoires pour django-tenants
    slug = models.SlugField(unique=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True  # ⚠️ indispensable

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
    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Domain(DomainMixin):
    pass
