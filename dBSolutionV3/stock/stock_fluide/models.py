import uuid

from django.db import models
from piece.piece_fluides.models import PieceFluide
from societe.models import Societe



class StockFluide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    piece_fluide = models.ForeignKey(
        "piece_fluides.PieceFluide",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantite_litre = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    seuil_alerte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5
    )

    class Meta:
        unique_together = ("societe", "fluide")