import uuid
from django.db import models
from societe.models import Societe


class VoitureModele(models.Model):
    class NombrePortes(models.IntegerChoices):
        DEUX = 2, "2 portes"
        TROIS = 3, "3 portes"
        CINQ = 5, "5 portes"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations
    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="modeles"
    )
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    # Informations du modèle
    nom_modele = models.CharField(max_length=100)
    nom_variante = models.CharField(max_length=100, blank=True, null=True)
    nombre_portes = models.IntegerField(choices=NombrePortes.choices)

    nbre_places = models.PositiveSmallIntegerField()

    taille_reservoir = models.DecimalField(max_digits=5, decimal_places=2, help_text="En litres")

    capacite_batterie = models.PositiveIntegerField(default=0, help_text="Capacité batterie", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom_modele} {self.nom_variante or ''}".strip()
