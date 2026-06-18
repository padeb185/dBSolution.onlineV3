import uuid

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





class ClientAtelier(models.Model):

    id_client_particulier = models.UUIDField(default=uuid.uuid4)  # sans unique pour commencer

    client_particulier = models.ForeignKey(
        "client_particulier.ClientParticulier",
        verbose_name=_("Client atelier"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="client_atelier",
        null=True,
        blank=True,
    )

    societe_cliente = models.ForeignKey(
        "societe_cliente.SocieteCliente",
        on_delete=models.CASCADE,
        related_name="client_atelier",
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


    voitures = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        verbose_name=_("Voitures"),
        related_name="client_atelier",
        blank=True,
    )


    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def __str__(self):
        cp = self.client_particulier

        return _("Client : %(nom)s %(prenom)s") % {
            "nom": cp.nom,
            "prenom": cp.prenom,
        }

