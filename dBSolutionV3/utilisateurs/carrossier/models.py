from django.db import models
from utilisateurs.models import Utilisateur

class Carrossier(Utilisateur):
    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
