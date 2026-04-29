from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal



class Proprietaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)


    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.CASCADE,
        related_name="proprietaires",
        null=True,
        blank=True,
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires"
    )


class ProprietaireVoiture(models.Model):
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture"
    )

    proprietaire = models.ForeignKey(
        "proprietaire.Proprietaire",
        on_delete=models.CASCADE,
        related_name="proprietaire_voitures"
    )

    part_proprietaire_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture",
        null=True,
        blank=True,
    )