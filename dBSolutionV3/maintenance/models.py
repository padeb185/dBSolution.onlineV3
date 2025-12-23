from django.db import models
import uuid
from voiture.voiture_exemplaire.models import VoitureExemplaire
from utilisateurs.mecanicien.models import Mecanicien

class Maintenance(models.Model):
    TAG_CHOICES = [
        ('GREEN', 'Green'),
        ('YELLOW', 'Yellow'),
        ('RED', 'Red'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voiture_exemplaire = models.ForeignKey(
        'voiture_exemplaire.VoitureExemplaire',  # ou le bon modèle
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="maintenances"
    )

    mecanicien = models.ForeignKey(Mecanicien, on_delete=models.SET_NULL, null=True, blank=True)
    immatriculation = models.CharField(max_length=20)
    date_intervention = models.DateField()
    date_derniere_intervention = models.DateField(null=True, blank=True)
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='GREEN')

    # Kilométrage général
    kilometres_total = models.PositiveIntegerField(default=0)
    kilometres_derniere_intervention = models.PositiveIntegerField(null=True, blank=True)
    kilometres_chassis = models.PositiveIntegerField(null=True, blank=True)

    # Kilométrage spécifiques
    kilometres_moteur = models.PositiveIntegerField(default=0)
    kilometres_boite = models.PositiveIntegerField(default=0)

    # Suivi des remplacements
    remplacement_moteur = models.BooleanField(default=False)
    remplacement_boite = models.BooleanField(default=False)

    @property
    def kilometres_calcules(self):
        """Kilomètres depuis la dernière intervention"""
        if self.kilometres_derniere_intervention is not None:
            return self.kilometres_total - self.kilometres_derniere_intervention
        return None

    def save(self, *args, **kwargs):
        # Remise à zéro des compteurs si remplacement
        if self.remplacement_moteur:
            self.kilometres_moteur = 0
        if self.remplacement_boite:
            self.kilometres_boite = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Maintenance {self.vehicule} ({self.date_intervention})"
