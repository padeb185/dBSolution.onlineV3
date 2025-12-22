from django.db import models
from piece.models import Piece


class PieceMoteur(models.Model):
    piece = models.ForeignKey(
        Piece,
        on_delete=models.CASCADE,
        related_name="pieces_moteur"
    )
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

