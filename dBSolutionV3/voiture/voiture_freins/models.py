import uuid
from django.db import models


class VoitureFreins(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.CASCADE,
        related_name="freins",
        verbose_name="Voiture modèle"
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="freins",
        verbose_name="Voiture exemplaire"
    )

    taille_disque_av = models.FloatField(
        verbose_name="Taille disque AV (mm)"
    )
    taille_disque_ar = models.FloatField(
        verbose_name="Taille disque AR (mm)"
    )

    epaisseur_disque_av = models.FloatField(
        verbose_name="Épaisseur disque AV (mm)"
    )
    epaisseur_disque_ar = models.FloatField(
        verbose_name="Épaisseur disque AR (mm)"
    )

    epaisseur_min_disque_av = models.FloatField(
        verbose_name="Épaisseur minimum disque AV (mm)"
    )
    epaisseur_min_disque_ar = models.FloatField(
        verbose_name="Épaisseur minimum disque AR (mm)"
    )

    class Meta:
        verbose_name = "Voiture – freins"
        verbose_name_plural = "Voitures – freins"

    def __str__(self):
        return f"{self.voiture_exemplaire} – Freins"
