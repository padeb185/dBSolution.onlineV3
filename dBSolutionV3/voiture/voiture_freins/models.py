import uuid
from django.db import models


class VoitureFreins(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 🔗 Relation principale
    voiture_exemplaire = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="freins",
        blank=True,
    )

    # 🔧 Marques (TEXTES ou modèle Marque)
    marque_disques_av = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    marque_disques_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    marque_plaquettes_av = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    marque_plaquettes_ar = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # 📏 Dimensions
    taille_disque_av = models.FloatField("Taille disque AV (mm)", null=True, blank=True)
    taille_disque_ar = models.FloatField("Taille disque AR (mm)", null=True, blank=True)

    epaisseur_disque_av = models.FloatField("Épaisseur disque AV (mm)", null=True, blank=True)
    epaisseur_disque_ar = models.FloatField("Épaisseur disque AR (mm)", null=True, blank=True)

    epaisseur_min_disque_av = models.FloatField("Épaisseur minimum disque AV (mm)", null=True, blank=True)
    epaisseur_min_disque_ar = models.FloatField("Épaisseur minimum disque AR (mm)", null=True, blank=True)

    plaquettes_av = models.FloatField("Plaquettes AV (mm)", null=True, blank=True)
    plaquettes_ar = models.FloatField("Plaquettes AR (mm)", null=True, blank=True)

    class Meta:
        verbose_name = "Voiture – Freins"
        verbose_name_plural = "Voitures – Freins"

    def __str__(self):
        return f"{self.voiture_exemplaire} – Freins"
