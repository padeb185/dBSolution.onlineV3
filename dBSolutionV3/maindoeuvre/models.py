import uuid
from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _


class MainDoeuvre(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="main_oeuvres",
        null=True,
        blank=True,
    )

    utilisateur = models.ForeignKey(
        "utilisateurs.Utilisateur",
        on_delete=models.CASCADE,
        related_name="main_oeuvres",
    )

    # 💰 Prix facturé au client
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Taux horaire client")
    )

    # ⏱ Temps total en minutes
    temps_minutes = models.PositiveIntegerField(default=0)

    descriptif = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    remarques = models.TextField(
        blank=True,
        null=True
    )

    date = models.DateTimeField(auto_now_add=True)

    # -------------------------
    # TEMPS
    # -------------------------
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
    def temps_display(self):
        return f"{self.heures}h{self.minutes:02d}"

    # -------------------------
    # FACTURATION
    # -------------------------
    @property
    def cout_total(self):
        return self.temps_decimal * self.taux_horaire

    @property
    def cout_interne(self):
        salaire = getattr(
            self.utilisateur,
            "salaire_brut_heure",
            0
        ) or 0

        return self.temps_decimal * Decimal(salaire)

    @property
    def prix_facture(self):
        return self.cout_total

    def __str__(self):
        return f"{self.temps_display} - {self.utilisateur}"