from utilisateurs.models import Utilisateur
from django.db import models


class Comptable(Utilisateur):




    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
