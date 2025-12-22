from django.db import models
from utilisateurs.models import Utilisateur



class Apprenti(Utilisateur):

    role = models.CharField(max_length=50, default='Apprenti')

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"

