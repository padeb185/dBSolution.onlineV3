from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur  # ton modèle utilisateur personnalisé


class Direction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="directions")

    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('finance', 'Finance'),
        ('rh', 'Ressources Humaines'),
        ('operations', 'Operations'),
    ]
    role_direction = models.CharField(max_length=50, choices=ROLE_CHOICES)

    password = models.CharField(max_length=128)

    # Champ non stocké en base, juste pour validation du formulaire
    password_confirm = None

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        """Chiffre le mot de passe avant de le sauvegarder"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Vérifie le mot de passe"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} - {self.role_direction}"
