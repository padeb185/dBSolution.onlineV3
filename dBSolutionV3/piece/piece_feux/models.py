from django.db import models
from piece.models import Piece  #

class Feux(Piece):


    POSITIONS = [
        ("AVG", "Avant Gauche"),
        ("AVD", "Avant Droit"),
        ("ARG", "Arrière Gauche"),
        ("ARD", "Arrière Droit"),
        ("STOP", "Troisième feu stop"),
        ("AB_AV", "Antibrouillard AV"),
        ("AB_AR", "Antibrouillard AR"),
        ("CL_AVG", "Clignotant Avant Gauche"),
        ("CL_AVD", "Clignotant Avant Droit"),
        ("CL_ARG", "Clignotant Arrière Gauche"),
        ("CL_ARD", "Clignotant Arrière Droit"),
    ]

    type_feu = models.CharField(
        max_length=20,
        choices=POSITIONS,
        verbose_name="Type / Position du feu"
    )

    # Si tu veux ajouter d'autres infos spécifiques aux feux
    puissance = models.CharField(max_length=20, blank=True)
    couleur = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Feu"
        verbose_name_plural = "Feux"

    def __str__(self):
        return f"{self.organe or 'Feu'} - {self.get_type_feu_display()}"
