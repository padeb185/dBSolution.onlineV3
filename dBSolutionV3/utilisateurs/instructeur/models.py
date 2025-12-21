import uuid
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur
from django.db import models


class Instructeur(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_direction = models.CharField(max_length=50, default='Instructeur')
    password = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        # Empêche le double hachage
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.get_role_display()}"
