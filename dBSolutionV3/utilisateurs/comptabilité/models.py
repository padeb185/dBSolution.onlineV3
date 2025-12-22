from utilisateurs.models import Utilisateur
from django.db import models


class Comptable(Utilisateur):

    role = models.CharField(max_length=50, default='Comptable')


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
