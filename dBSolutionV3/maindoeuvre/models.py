from django.db import models
from decimal import Decimal
import uuid
from django.utils.translation import gettext_lazy as _


class MainDoeuvre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    utilisateur = models.ForeignKey(
        "utilisateurs.Utilisateur",
        on_delete=models.CASCADE,
        related_name="main_oeuvres",
    )

    temps_minutes = models.PositiveIntegerField(default=0)


    created_at = models.DateTimeField(auto_now_add=True)



    @property
    def heures(self):
        return self.temps_minutes // 60

    @property
    def minutes(self):
        return self.temps_minutes % 60

    @property
    def temps_decimal(self):
        return Decimal(self.temps_minutes) / Decimal(60)

    @property
    def taux_horaire(self):
        return self.utilisateur.salaire_brut_heure or Decimal("0.00")

    def cout_total(self):
        return (self.temps_minutes / 60) * self.taux_horaire

    def temps_display(self):
        return f"{self.heures}h{self.minutes:02d}"