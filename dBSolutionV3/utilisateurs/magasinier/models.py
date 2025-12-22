import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from dBSolutionV3 import utilisateurs


# Create your models here.
class Magasinier(utilisateurs):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, default='Magasinier')


    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.role}"
