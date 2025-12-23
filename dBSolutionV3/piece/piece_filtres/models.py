# piece/piece_filtres/models.py
from django.db import models
from piece.models import Piece


class TypeFiltre(models.TextChoices):
    AIR = "AIR", "Filtre à air"
    HUILE = "HUILE", "Filtre à huile"
    CARBURANT = "CARBURANT", "Filtre à carburant"
    POLLEN = "POLLEN", "Filtre à pollen"


class Filtre(Piece):
    type_filtre = models.CharField(max_length=20, choices=TypeFiltre.choices)
    nom_filtre = models.CharField(max_length=100, blank=True)



    class Meta:
        verbose_name = "Filtre"
        verbose_name_plural = "Filtres"

    def __str__(self):
        return f"{self.nom_filtre or 'Filtre'} ({self.get_type_filtre_display()})"
