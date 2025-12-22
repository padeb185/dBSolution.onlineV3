import uuid
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur
from django.db import models


class Instructeur(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_direction = models.CharField(max_length=50, default='Instructeur')

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
