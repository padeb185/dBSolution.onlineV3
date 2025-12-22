from utilisateurs.models import Utilisateur
from django.db import models


class Instructeur(Utilisateur):

    role_direction = models.CharField(max_length=50, default='Instructeur')

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
