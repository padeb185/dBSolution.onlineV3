from django.db import models
from utilisateurs.models import Utilisateur
from django.utils.translation import gettext_lazy as _


class Direction(Utilisateur):


    ROLE_DIR_CHOICES = [
        ('admin', _('Administrateur')),
        ('finance', _('Finance')),
        ('rh', _('Ressources Humaines')),
        ('operations', _('Operations')),
    ]
    role_direction = models.CharField(max_length=50, choices=ROLE_DIR_CHOICES)




    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_direction_display()}"
