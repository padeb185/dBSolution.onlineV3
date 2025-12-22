from django.db import models
from utilisateurs.models import Utilisateur


class Direction(Utilisateur):


    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('finance', 'Finance'),
        ('rh', 'Ressources Humaines'),
        ('operations', 'Operations'),
    ]
    role_direction = models.CharField(max_length=50, choices=ROLE_CHOICES)




    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_direction_display()}"
