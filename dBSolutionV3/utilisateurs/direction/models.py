import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur


class Direction(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('finance', 'Finance'),
        ('rh', 'Ressources Humaines'),
        ('operations', 'Operations'),
    ]
    role_direction = models.CharField(max_length=50, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_direction_display()}"
