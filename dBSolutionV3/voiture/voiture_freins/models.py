import uuid
from django.db import models


class VoitureFreins(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 🔗 Relation principale
    voitures_exemplaires = models.ManyToManyField(
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


    marque_plaquettes_av = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    # 📏 Dimensions
    taille_disque_av = models.FloatField("Taille disque AV (mm)", null=True, blank=True)


    epaisseur_disque_av = models.FloatField("Épaisseur disque AV (mm)", null=True, blank=True)


    epaisseur_min_disque_av = models.FloatField("Épaisseur minimum disque AV (mm)", null=True, blank=True)


    plaquettes_av = models.FloatField("Plaquettes AV (mm)", null=True, blank=True)


    class Meta:
        verbose_name = "Voiture – Freins"
        verbose_name_plural = "Voitures – Freins"

    def __str__(self):
        voitures = ", ".join([str(v) for v in self.voitures_exemplaires.all()])
        return f"{voitures or self.id} – Freins"