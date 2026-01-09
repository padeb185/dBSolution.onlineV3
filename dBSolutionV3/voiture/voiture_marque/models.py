from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
import uuid
from django.conf import settings


class VoitureMarque(models.Model):
    id_marque = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    nom_marque = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(2, message="Le nom de la marque doit contenir au moins 2 caractères"),
            MaxLengthValidator(50, message="Le nom de la marque ne peut pas dépasser 50 caractères")
        ]
    )

    class Meta:
        ordering = ['nom_marque']
        verbose_name = "Marque de voiture"
        verbose_name_plural = "Marques de voitures"

    def __str__(self):
        return self.nom_marque

    def est_favori_par(self, societe):
        """Retourne True si la société a cette marque dans ses favoris"""
        from .models import MarqueFavorite  # import local pour éviter boucle
        if societe:  # societe doit être un objet valide
            return MarqueFavorite.objects.filter(societe=societe, marque=self).exists()
        return False


class MarqueFavorite(models.Model):
    societe = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="marques_favorites"
    )
    marque = models.ForeignKey(
        VoitureMarque,
        on_delete=models.CASCADE,
        related_name="favoris"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("societe", "marque")
        ordering = ["-created_at"]
        verbose_name = "Marque favorite"
        verbose_name_plural = "Marques favorites"

    def __str__(self):
        return f"{self.societe} ❤️ {self.marque}"
