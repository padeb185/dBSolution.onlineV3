import uuid
from django.db import models


class Entretien(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="entretiens"
    )

    kilometrage_prevu = models.PositiveIntegerField()
    kilometrage_realise = models.PositiveIntegerField(null=True, blank=True)

    alerte_avant_km = models.PositiveIntegerField(default=400)

    date_prevue = models.DateField(null=True, blank=True)
    date_realisation = models.DateField(null=True, blank=True)

    termine = models.BooleanField(default=False)

    class Meta:
        ordering = ["kilometrage_prevu"]

    def doit_alerter(self, km_actuel):
        return (
            not self.termine
            and km_actuel >= self.kilometrage_prevu - self.alerte_avant_km
        )



class EntretienOperation(models.Model):
    entretien = models.ForeignKey(
        Entretien,
        on_delete=models.CASCADE,
        related_name="operations"
    )

    type_operation = models.CharField(
        max_length=50,
        choices=[
            ("VIDANGE", "Vidange"),
            ("FILTRE_HUILE", "Filtre à huile"),
            ("BOUGIES", "Bougies"),
            ("FILTRE_AIR", "Filtre à air"),
            ("FILTRE_HABITACLE", "Filtre habitacle"),
        ]
    )

    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantite = models.FloatField(null=True, blank=True)


class EntretienFluide(models.Model):
    entretien = models.ForeignKey(
        Entretien,
        on_delete=models.CASCADE,
        related_name="fluides"
    )

    piece_fluide = models.ForeignKey(
        "piece_fluides.Fluide",
        on_delete=models.CASCADE
    )

    quantite = models.FloatField(help_text="Litres")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fluide.mettre_a_jour_stock(-self.quantite)




    def mettre_a_jour_stock(self, delta):
        self.stock += delta
        self.save(update_fields=["stock"])

