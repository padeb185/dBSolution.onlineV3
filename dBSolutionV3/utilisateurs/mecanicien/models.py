from utilisateurs.models import Utilisateur
from django.db import models




class Mecanicien(Utilisateur):

    pass



    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
