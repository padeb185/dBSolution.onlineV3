from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
import uuid



class VoitureMarque(models.Model):
    id_marque = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nom_marque = models.CharField(
        max_length=50,  # on augmente un peu pour pouvoir stocker des marques plus longues
        unique=True,    # évite les doublons
        validators=[
            MinLengthValidator(2, message="Le nom de la marque doit contenir au moins 2 caractères"),
            MaxLengthValidator(50, message="Le nom de la marque ne peut pas dépasser 50 caractères")
        ]
    )

    class Meta:
        ordering = ['nom_marque']  # affichage trié par nom
        verbose_name = "Marque de voiture"
        verbose_name_plural = "Marques de voitures"

    def __str__(self):
        return self.nom_marque



