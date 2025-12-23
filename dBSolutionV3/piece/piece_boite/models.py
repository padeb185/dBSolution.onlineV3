from django.db import models
from piece.models import Piece  # ton modèle de base Piece

# Pièces d'une boîte mécanique
class BoiteMecanique(Piece):
    NB_VITESSES_CHOICES = [(5, "5 vitesses"), (6, "6 vitesses"), (7, "7 vitesses")]

    nb_vitesses = models.IntegerField(choices=NB_VITESSES_CHOICES)
    embrayage = models.CharField(max_length=255, blank=True, null=True)
    disque_embreyage = models.CharField(max_length=255, blank=True, null=True)
    plateau_embreyage = models.CharField(max_length=255, blank=True, null=True)
    butee_embreyage = models.CharField(max_length=255, blank=True, null=True)
    pignon = models.CharField(max_length=255, blank=True, null=True)
    synchro = models.CharField(max_length=255, blank=True, null=True)
    arbre_principal = models.CharField(max_length=255, blank=True, null=True)
    arbre_secondaire = models.CharField(max_length=255, blank=True, null=True)
    fourchette_vitesse = models.CharField(max_length=255, blank=True, null=True)
    tringlerie = models.CharField(max_length=255, blank=True, null=True)
    huile = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Boîte Mécanique {self.nb_vitesses} vitesses"

# Pièces d'une boîte automatique
class BoiteAutomatique(Piece):
    NB_VITESSES_CHOICES = [(4, "4 vitesses"), (5, "5 vitesses"), (6, "6 vitesses"), (8, "8 vitesses")]

    nb_vitesses = models.IntegerField(choices=NB_VITESSES_CHOICES)
    convertisseur_torque = models.CharField(max_length=255, blank=True, null=True)
    embrayage_hydraulique = models.CharField(max_length=255, blank=True, null=True)
    train_planetaire = models.CharField(max_length=255, blank=True, null=True)
    frein_planetaire = models.CharField(max_length=255, blank=True, null=True)
    piston = models.CharField(max_length=255, blank=True, null=True)
    valve_body = models.CharField(max_length=255, blank=True, null=True)
    solenoides = models.CharField(max_length=255, blank=True, null=True)
    huile_transmission = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Boîte Automatique {self.nb_vitesses} vitesses"
