from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _



class ClientPilotage(models.Model):

    client_particulier = models.ForeignKey(
        "client_particulier.ClientParticulier",
        verbose_name=_("Client pilotage"),
        on_delete=models.CASCADE,

    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="client_pilotage",
        null=True,
        blank=True,
    )

    adresse = models.OneToOneField(
        "adresse.Adresse",
        verbose_name=_("Adresse"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class NiveauPilotage(models.TextChoices):
        DEBUTANT = "DEBUTANT", _("Débutant")
        INTERMEDIAIRE = "INTERMEDIAIRE", _("Intermédiaire")
        EXPERT = "PRO", _("Pro")
        BRONZE = "BRONZE", _("Bronze")
        SILVER = "SILVER", _("Silver")
        GOLD = "GOLD", _("Gold")

    niveau = models.CharField(
        _("Niveau"),
        max_length=20,
        choices=NiveauPilotage.choices,
        default=NiveauPilotage.DEBUTANT,
    )

    historique = models.TextField(
        _("Historique pilotage"),
        null=True,
        blank=True,
    )

    location = models.TextField(
        _("historique des locations"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Client pilotage")
        verbose_name_plural = _("Clients pilotages")
        indexes = [
            models.Index(fields=["societe"]),
            models.Index(fields=["niveau"]),
        ]

    def __str__(self):
        cp = self.client_particulier
        return f"{cp.prenom} {cp.nom} ({self.niveau})"

    def clean(self):
        super().clean()

        if self.date_naissance:
            today = date.today()
            age = today.year - self.date_naissance.year - (
                    (today.month, today.day) <
                    (self.date_naissance.month, self.date_naissance.day)
            )

            if age < 18:
                raise ValidationError({
                    'date_naissance': _("La personne doit avoir au moins 18 ans.")
                })

    @property
    def age(self):
        if not self.date_naissance:
            return None

        today = date.today()
        return today.year - self.date_naissance.year - (
                (today.month, today.day) <
                (self.date_naissance.month, self.date_naissance.day)
        )

