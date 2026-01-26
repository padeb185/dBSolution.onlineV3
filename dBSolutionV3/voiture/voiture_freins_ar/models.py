import uuid
from django.db import models


class VoitureFreinsAR(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # 🔗 Relation principale
    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="freins_ar",
        blank=True,
    )


    marque_disques_ar = models.CharField(
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

    taille_disque_ar = models.FloatField("Taille disque AR (mm)", null=True, blank=True)


    epaisseur_disque_ar = models.FloatField("Épaisseur disque AR (mm)", null=True, blank=True)


    epaisseur_min_disque_ar = models.FloatField("Épaisseur minimum disque AR (mm)", null=True, blank=True)


    plaquettes_ar = models.FloatField("Plaquettes AR (mm)", null=True, blank=True)

    class Meta:
        verbose_name = "Voiture – Freins Arrière"
        verbose_name_plural = "Voitures – Freins Arrière"

    def __str__(self):
        voitures = ", ".join([str(v) for v in self.voitures_exemplaires.all()])
        return f"{voitures or self.id} – Freins arrière"
