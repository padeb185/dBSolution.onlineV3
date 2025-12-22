import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur

class Vendeur(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, default='Vendeur')


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
