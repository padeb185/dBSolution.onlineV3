from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator
import uuid
from functools import lru_cache
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from societe.models import Societe


LOGO_PAR_DEFAUT = "images/marques/default.png"


@lru_cache(maxsize=None)
def _logo_existe(chemin):
    """Vrai si le fichier statique existe (mis en cache jusqu'au redémarrage du serveur)."""
    if finders.find(chemin):
        return True
    try:
        return staticfiles_storage.exists(chemin)
    except Exception:
        return False


class VoitureMarque(models.Model):
    id_marque = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    nom_marque = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(2, message="Le nom de la marque doit contenir au moins 2 caractères"),
            MaxLengthValidator(50, message="Le nom de la marque ne peut pas dépasser 50 caractères")
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["societe", "nom_marque"],
                name="unique_marque_par_societe"
            )
        ]

    def __str__(self):
        return self.nom_marque

    def est_favori_par(self, societe):
        """Retourne True si la société a cette marque dans ses favoris"""
        from .models import MarqueFavorite  # import local pour éviter boucle
        if societe:  # societe doit être un objet valide
            return MarqueFavorite.objects.filter(societe=societe, marque=self).exists()
        return False

    @property
    def nom_fichier_logo(self):
        return f"{self.nom_marque.strip().lower()}.png"

    @property
    def logo_static(self):
        """Chemin statique du logo, ou du logo par défaut s'il n'existe pas (évite les 404)."""
        chemin = f"images/marques/{self.nom_fichier_logo}"
        return chemin if _logo_existe(chemin) else LOGO_PAR_DEFAUT


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
