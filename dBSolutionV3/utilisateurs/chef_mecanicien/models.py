
from django.db import models
from utilisateurs.models import Utilisateur



class ChefMecanicien(Utilisateur):

    role = models.CharField(max_length=50, default='Chef Mécanicien')

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
