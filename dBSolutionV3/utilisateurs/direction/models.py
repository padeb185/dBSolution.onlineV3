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

    password = models.CharField(max_length=256)

    # Champ non stocké en base, juste pour validation du formulaire
    password_confirm = None

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Empêche le double hachage
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom} - {self.role_direction}"
