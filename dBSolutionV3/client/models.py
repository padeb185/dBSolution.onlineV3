from django.db import models
from adresse.models import Adresse



class Client(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.OneToOneField(Adresse, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    # --- Métadonnées ---
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


    def __str__(self):
        return f"{self.nom} (Client)"


