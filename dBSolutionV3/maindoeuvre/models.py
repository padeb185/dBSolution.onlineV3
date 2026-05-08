import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _


class MainDoeuvre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="main_oeuvre",
        null=True,
        blank=True,
    )

    utilisateur = models.ForeignKey(
        "utilisateurs.Utilisateur",
        on_delete=models.CASCADE,
        related_name="main_oeuvres",
    )

    temps_minutes = models.PositiveIntegerField(default=0)

    descriptif = models.CharField(max_length=255, blank=True, null=True)
    remarques = models.TextField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

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
        return getattr(self.utilisateur, "salaire_brut_heure", Decimal("0.00")) or Decimal("0.00")

    @property
    def cout_total(self):
        return (Decimal(self.temps_minutes) / Decimal("60")) * self.taux_horaire

    @property
    def temps_display(self):
        return f"{self.heures}h{self.minutes:02d}"