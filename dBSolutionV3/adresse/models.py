from django.db import models
import uuid


class Adresse(models.Model):
    id_adresse = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    rue = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, default="Belgique")

    def __str__(self):
        return f"{self.rue} {self.numero}, {self.code_postal} {self.ville}"

