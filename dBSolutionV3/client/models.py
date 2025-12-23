from django.db import models
from adresse.models import Adresse

class Client(models.Model):
    # Informations personnelles
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    # Nouveaux champs correctement définis
    age = models.PositiveIntegerField(null=True, blank=True)
    numero_permis = models.CharField(max_length=50, null=True, blank=True)

    NIVEAU_CHOICES = [
        ('DEBUTANT', 'Débutant'),
        ('INTERMEDIAIRE', 'Intermédiaire'),
        ('EXPERT', 'Expert'),
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
    ]
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='DEBUTANT')

    historique = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    # Métadonnées
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.nom} {self.prenom} (Client)"
