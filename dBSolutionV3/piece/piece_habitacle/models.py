# piece_habitacle/models.py
from django.db import models
from piece.models import Piece  # On suppose que ton modèle de base s'appelle Piece

class PieceHabitacle(Piece):
    """
    Modèle principal pour les pièces de l'habitacle
    """
    pass  # On peut ajouter des champs communs ici si nécessaire

# Sous-modèles spécifiques
class Siege(PieceHabitacle):
    TYPE_CHOICES = [
        ("conducteur", "Siège conducteur"),
        ("passager", "Siège passager"),
        ("ar_droit", "Siège arrière droit"),
        ("ar_gauche", "Siège arrière gauche"),
    ]
    type_siege = models.CharField(max_length=20, choices=TYPE_CHOICES)

class Volant(PieceHabitacle):
    pass

class GPS(PieceHabitacle):
    pass

class Radio(PieceHabitacle):
    pass

class Tapis(PieceHabitacle):
    pass

class CeintureSecurite(PieceHabitacle):
    pass

class Harnais(PieceHabitacle):
    pass

class CompteursCommodo(PieceHabitacle):
    pass

class Airbag(PieceHabitacle):
    POSITION_CHOICES = [
        ("conducteur", "Conducteur"),
        ("passager", "Passager"),
        ("lat_gauche", "Latéral gauche"),
        ("lat_droit", "Latéral droit"),
        ("siege_conducteur", "Siège conducteur"),
        ("siege_passager", "Siège passager"),
        ("sieges_ar_droit", "Sièges arrière droit"),
        ("sieges_ar_gauche", "Sièges arrière gauche"),
    ]
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
