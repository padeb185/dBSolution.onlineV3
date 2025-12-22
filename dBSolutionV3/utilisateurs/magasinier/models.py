from django.db import models
from utilisateurs.models import Utilisateur


# Create your models here.
class Magasinier(Utilisateur):

    role = models.CharField(max_length=50, default='Magasinier')


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
