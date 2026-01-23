import uuid
from django.db import models


class VoitureFreins(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Relations ManyToMany
    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="freins",
        blank=True
    )

    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="freins",
        blank=True
    )
    taille_disque_av = models.FloatField(
        verbose_name="Taille disque AV (mm)",
        null=True,
        blank=True
    )
    taille_disque_ar = models.FloatField(
        verbose_name="Taille disque AR (mm)",
        null=True,
        blank=True
    )

    epaisseur_disque_av = models.FloatField(
        verbose_name="Épaisseur disque AV (mm)",
        null=True,
        blank=True
    )
    epaisseur_disque_ar = models.FloatField(
        verbose_name="Épaisseur disque AR (mm)",
        null=True,
        blank=True
    )

    epaisseur_min_disque_av = models.FloatField(
        verbose_name="Épaisseur minimum disque AV (mm)",
        null=True,
        blank=True
    )
    epaisseur_min_disque_ar = models.FloatField(
        verbose_name="Épaisseur minimum disque AR (mm)",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Voiture – freins"
        verbose_name_plural = "Voitures – freins"

    def __str__(self):
        return f"{self.voiture_exemplaire} – Freins"
