from utilisateurs.models import Utilisateur
from django.db import models


class InstructeurExterne(Utilisateur):


    numero_facture = models.PositiveIntegerField(default=0, blank=True, null=True)
    facture = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
