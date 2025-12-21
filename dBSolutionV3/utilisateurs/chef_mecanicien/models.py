# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from utilisateurs.models import Utilisateur  # ton

class ChefMecanicien(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="chefs_mecanicien")
    role = models.CharField(max_length=50, default='Chef Mécanicien')
    password = models.CharField(max_length=128)
    password_confirm = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
