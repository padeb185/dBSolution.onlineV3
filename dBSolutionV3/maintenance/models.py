import uuid
from django.db import models
from utilisateurs.mecanicien.models import Mecanicien
from django.utils import timezone


class Maintenance(models.Model):
    id_maintenance = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name='maintenances'
    )


    mecanicien = models.ForeignKey(
        Mecanicien,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenances'
    )

    immatriculation = models.CharField(max_length=20)

    date_intervention = models.DateField()
    date_derniere_intervention = models.DateField(null=True, blank=True)
    date_heure_creation = models.DateTimeField(default=timezone.now)

    TAG_CHOICES = [
        ('GREEN', 'Green'),
        ('YELLOW', 'Yellow'),
        ('RED', 'Red')
    ]
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default='GREEN')

    class Meta:
        verbose_name = "Maintenance"
        verbose_name_plural = "Maintenances"
        ordering = ['-date_heure_creation']

    def __str__(self):
        return f"Maintenance {self.immatriculation} ({self.get_tag_display()})"
