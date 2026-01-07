from django.db import models
from utilisateurs.models import Utilisateur



class ChefMecanicien(Utilisateur):


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
