from django.db import models
from django.utils.translation import gettext_lazy as _
from adresse.models import Adresse


class Client(models.Model):
    # Informations personnelles
    nom = models.CharField(_("Nom"), max_length=255)
    prenom = models.CharField(_("Prénom"), max_length=255)
    adresse = models.OneToOneField(
        Adresse,
        verbose_name=_("Adresse"),
        on_delete=models.CASCADE
    )
    numero_telephone = models.CharField(
        _("Numéro de téléphone"),
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

    # Informations complémentaires
    age = models.PositiveIntegerField(_("Âge"), null=True, blank=True)
    numero_permis = models.CharField(
        _("Numéro de permis"),
        max_length=50,
        null=True,
        blank=True
    )

    class Niveau(models.TextChoices):
        DEBUTANT = "DEBUTANT", _("Débutant")
        INTERMEDIAIRE = "INTERMEDIAIRE", _("Intermédiaire")
        EXPERT = "EXPERT", _("Expert")
        BRONZE = "BRONZE", _("Bronze")
        SILVER = "SILVER", _("Silver")
        GOLD = "GOLD", _("Gold")

    niveau = models.CharField(
        _("Niveau"),
        max_length=20,
        choices=Niveau.choices,
        default=Niveau.DEBUTANT
    )

    historique = models.TextField(_("Historique"), null=True, blank=True)
    location = models.CharField(_("Location"), max_length=255, null=True, blank=True)

    # Métadonnées
    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return _("%(nom)s %(prenom)s (Client)") % {
            "nom": self.nom,
            "prenom": self.prenom,
        }
