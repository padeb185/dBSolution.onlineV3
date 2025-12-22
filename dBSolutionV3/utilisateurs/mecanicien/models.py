import uuid
from utilisateurs.models import Utilisateur
from django.db import models




class Mecanicien(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, default='Mecanicien')



    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
