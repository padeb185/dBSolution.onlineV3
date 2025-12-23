from django.db import models
from piece.models import Piece

class PieceJante(Piece):


    largeur = models.DecimalField(max_digits=4, decimal_places=1, help_text="Largeur en pouces, ex: 7, 7.5, 8")
    taille = models.PositiveIntegerField(help_text="Diamètre en pouces")
    entraxe = models.CharField(max_length=20, help_text="Ex: 5x100")
    alésage = models.PositiveIntegerField(help_text="Diamètre central en mm")
    deport_et = models.IntegerField(help_text="Déport ET en mm")

    def __str__(self):
        return f"Jante {self.largeur}x{self.taille} ET{self.deport_et} - {self.entraxe}"
