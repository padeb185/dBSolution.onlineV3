from django.db import models
from piece.models import Piece

class PieceRoueRechange(Piece):


    SITES_CHOICES = [
        ('BE', 'Belgique'),
        ('GE', 'Germany'),
        ('O', 'Other'),
    ]
    SIDE_CHOICES = [
        ('AV', 'Avant'),
        ('AR', 'Arrière')
    ]
    TYPE_CHOICES = [
        ('SLICK', 'Slick'),
        ('SEMI-SLICK', 'Semi-slick'),
        ('PLUIE', 'Pluie'),
        ('NEIGE', 'Neige'),
    ]

    sites = models.CharField(max_length=20, choices=SITES_CHOICES)
    side = models.CharField(max_length=20, choices=SIDE_CHOICES)
    type_roue = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} roue(s) {self.get_type_roue_display()} sur {self.get_site_roue_display()}"
