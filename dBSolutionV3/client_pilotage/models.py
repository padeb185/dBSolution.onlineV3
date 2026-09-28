from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from stdnum import iban


def validate_iban(value):
    if not value:
        return

    value = value.replace(" ", "").upper()

    if not iban.is_valid(value):
        raise ValidationError(_("IBAN invalide"))




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

    adresse = models.ForeignKey(
        "adresse.Adresse",
        verbose_name=_("Adresse"),
        on_delete=models.RESTRICT,  # ← au lieu de CASCADE
        related_name="client_pilotage",
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
        _("Niveau de pilotage"),
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

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Client pilotage")
        verbose_name_plural = _("Clients pilotages")
        indexes = [
            models.Index(fields=["societe"]),
            models.Index(fields=["niveau"]),
        ]

    def __str__(self):
        cp = self.client_particulier
        return f"{cp.prenom} {cp.nom} ({self.get_niveau_display()})"

