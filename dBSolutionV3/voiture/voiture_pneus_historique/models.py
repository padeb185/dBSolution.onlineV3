from django.db import models
import uuid


class VoiturePneusHistorique(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    voiture_pneus = models.ForeignKey(
        "voiture_pneus.VoiturePneus",
        on_delete=models.CASCADE,
        related_name="historiques"
    )
    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="historique_pneus",
        blank=True
    )

    kilometre_montage = models.PositiveIntegerField
    kilometres_effectues = models.PositiveIntegerField()

    date_remplacement = models.DateField(auto_now_add=True)

    numero_remplacement = models.PositiveSmallIntegerField()

    def __str__(self):
        return (
            f"{self.voiture_pneus} | "
            f"Remplacement #{self.numero_remplacement} | "
            f"{self.kilometres_effectues} km"
        )
