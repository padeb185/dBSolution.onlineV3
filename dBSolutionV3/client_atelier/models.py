import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from stdnum import iban


def validate_iban(value):
    if not iban.is_valid(value):
        raise ValidationError("IBAN invalide")



class ClientAtelier(models.Model):

    id_client_particulier = models.UUIDField(default=uuid.uuid4)  # sans unique pour commencer

    prenom = models.CharField(_("Prénom du client"), max_length=50)

    nom = models.CharField(_("Nom du client"), max_length=50)

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

    numero_telephone = models.CharField(
        _("Numéro de téléphone"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_carte_id = models.CharField(
        _("Numéro de carte d'identité"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_compte = models.CharField(
        _("Numéro de compte bancaire"),
        max_length=34,
        null=True,
        blank=True,
        validators=[validate_iban]
    )

    numero_carte_bancaire = models.CharField(
        _("Numéro de carte bancaire"),
        max_length=20,
        null=True,
        blank=True
    )

    email = models.EmailField(
        _("Email"),
        max_length=100,
        null=True,
        blank=True
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
        return _("Client : %(nom)s %(prenom)s") % {
            "nom": self.nom,
            "prenom": self.prenom,
        }


