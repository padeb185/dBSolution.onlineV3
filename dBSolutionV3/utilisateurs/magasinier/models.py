from django.db import models
from utilisateurs.models import Utilisateur


# Create your models here.
class Magasinier(Utilisateur):
    pass


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
