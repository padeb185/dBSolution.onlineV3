import uuid
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur  # ton
from django.db import models

# Create your models here.
class Magasinier(Utilisateur):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, default='Magasinier')
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # Empêche le double hachage
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)