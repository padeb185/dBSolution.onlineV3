from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal



class Voiture(models.Model):
    nombre_proprietaires = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )

    def clean(self):
        total = sum([p.part_proprietaire_pourcent for p in self.proprietaires.all()])
        if total != 100:
            raise ValidationError("Le total des parts des propriétaires doit être égal à 100%.")






class ProprietairePart(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, related_name="proprietaires")
    nom_proprietaire = models.CharField(max_length=100)
    part_proprietaire_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100'))]
    )

    def __str__(self):
        return f"{self.nom_proprietaire} - {self.part_proprietaire_pourcent}%"


