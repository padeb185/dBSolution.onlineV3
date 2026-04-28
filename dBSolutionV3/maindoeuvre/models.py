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

    temps = models.DecimalField(max_digits=6, decimal_places=2)


    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def taux_horaire(self):
        return self.utilisateur.salaire_brut_heure or Decimal("0.00")

    @property
    def cout_total(self):
        return self.temps * self.taux_horaire