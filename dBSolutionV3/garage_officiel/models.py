import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupeAutomobile(models.TextChoices):
    VAG = "VAG", _("Groupe Volkswagen (VAG : VW, Audi, Seat, Cupra, Škoda, Porsche, Bentley, Lamborghini)")
    STELLANTIS = "STELLANTIS", _("Stellantis (Peugeot, Citroën, DS, Opel, Fiat, Alfa Romeo, Jeep, Lancia, Maserati)")
    BMW = "BMW", _("BMW Group (BMW, Mini, Rolls-Royce)")
    MERCEDES = "MERCEDES", _("Mercedes-Benz Group (Mercedes-Benz, Mercedes-AMG, Smart)")
    RENAULT = "RENAULT", _("Renault Group (Renault, Dacia, Alpine)")
    TOYOTA = "TOYOTA", _("Toyota (Toyota, Lexus)")
    HYUNDAI = "HYUNDAI", _("Hyundai Motor Group (Hyundai, Kia, Genesis)")
    NISSAN = "NISSAN", _("Nissan / Mitsubishi")
    GEELY = "GEELY", _("Geely (Volvo, Polestar, Lotus, Lynk & Co)")
    JLR = "JLR", _("Jaguar Land Rover")
    FORD = "FORD", _("Ford")
    HONDA = "HONDA", _("Honda")
    MAZDA = "MAZDA", _("Mazda")
    SUBARU = "SUBARU", _("Subaru")
    SUZUKI = "SUZUKI", _("Suzuki")
    TESLA = "TESLA", _("Tesla")
    FERRARI = "FERRARI", _("Ferrari")
    ASTON_MARTIN = "ASTON_MARTIN", _("Aston Martin")
    MCLAREN = "MCLAREN", _("McLaren")
    AUTRE = "AUTRE", _("Autre groupe")


class GarageOfficiel(models.Model):
    """Garage de la marque (concession / atelier agréé) utilisé pour les maintenances externes."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="garages_officiels",
    )

    nom = models.CharField(_("Nom"), max_length=255)

    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.PROTECT,
        related_name="garages_officiels",
        null=True,
        blank=True,
        verbose_name=_("Adresse"),
    )

    numero_tva = models.CharField(_("Numéro de TVA"), max_length=30, blank=True)
    peppol_id = models.CharField(
        _("Identifiant Peppol"), max_length=100, blank=True,
        help_text=_("Format schéma:identifiant, ex. 0208:0123456789"),
    )
    telephone = models.CharField(_("Téléphone"), max_length=30, blank=True)
    email = models.EmailField(_("E-mail"), blank=True)

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.SET_NULL,
        related_name="garages_officiels",
        null=True,
        blank=True,
        verbose_name=_("Marque"),
    )

    groupe = models.CharField(
        _("Groupe automobile"),
        max_length=20,
        choices=GroupeAutomobile.choices,
        blank=True,
    )

    remarques = models.TextField(_("Remarques"), blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Garage officiel")
        verbose_name_plural = _("Garages officiels")
        ordering = ["nom"]

    def __str__(self):
        ville = getattr(self.adresse, "ville", "") if self.adresse_id else ""
        return f"{self.nom} ({ville})" if ville else self.nom

    @property
    def marque_ou_groupe(self):
        if self.voiture_marque_id:
            return self.voiture_marque.nom_marque
        return self.get_groupe_display() if self.groupe else ""

    @property
    def code_pays(self):
        return (getattr(self.adresse, "code_pays", "") or "BE")[:2].upper() if self.adresse_id else "BE"

    def clean(self):
        super().clean()
        if not self.voiture_marque_id and not self.groupe:
            raise ValidationError(_("Indiquez la marque ou le groupe automobile."))
        if self.peppol_id and ":" not in self.peppol_id:
            raise ValidationError({"peppol_id": _("Format attendu : schéma:identifiant, ex. 0208:0123456789")})
        if self.numero_tva:
            self.numero_tva = self.numero_tva.replace(" ", "").replace(".", "").upper()
