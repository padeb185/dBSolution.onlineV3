from django.db import models
import uuid
from django.utils.text import slugify
from django_tenants.models import TenantMixin, DomainMixin

from django.db import models
import uuid
from django.utils.text import slugify
from django_tenants.models import TenantMixin, DomainMixin


class Societe(TenantMixin):
    schema_name = models.CharField(max_length=63, unique=True)

    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.CASCADE,
        related_name='société',
        verbose_name='Adresse',
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)

    auto_create_schema = True

    id_societe = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    nom = models.CharField(max_length=100, unique=True)
    directeur = models.CharField(max_length=100)
    numero_tva = models.CharField(max_length=20, unique=True)
    site = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Société"
        verbose_name_plural = "Sociétés"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)

        if not self.schema_name:
            self.schema_name = slugify(self.nom).replace("-", "_")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Domain(DomainMixin):
    pass