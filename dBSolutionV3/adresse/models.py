from django.utils import timezone
from django.db import models
import uuid


class Adresse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rue = models.CharField("Rue", max_length=255)
    numero = models.CharField("Numéro", max_length=10)
    code_postal = models.CharField("Code postal", max_length=10)
    ville = models.CharField("Ville", max_length=100)

    pays = models.CharField("Pays", max_length=100, default="Belgique")
    code_pays = models.CharField("Code pays", max_length=5, default="BE")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Adresse"
        verbose_name_plural = "Adresses"
        ordering = ["ville", "rue"]

    def __str__(self):
        return f"{self.rue} {self.numero}, {self.code_postal} {self.ville}"
