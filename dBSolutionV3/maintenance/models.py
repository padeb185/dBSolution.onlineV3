import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.entretien.models import Entretien


class Maintenance(models.Model):
    class Tag(models.TextChoices):
        VERT = "VERT", _("Vert")
        JAUNE = "JAUNE", _("Jaune")
        ROUGE = "ROUGE", _("Rouge")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        verbose_name=_("Voiture exemplaire"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="maintenances"
    )

    mecanicien = models.ForeignKey(
        "mecanicien.Mecanicien",
        verbose_name=_("Mécanicien"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    apprentis = models.ForeignKey(
        "apprentis.Apprenti",
        verbose_name=_("Apprenti"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    chef_mecanicien = models.ForeignKey(
        "chef_mecanicien.ChefMecanicien",
        verbose_name=_("Apprentis"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )



    immatriculation = models.CharField(_("Immatriculation"), max_length=20)
    date_intervention = models.DateField(_("Date d'intervention"))
    date_derniere_intervention = models.DateField(
        _("Date de la dernière intervention"),
        null=True,
        blank=True
    )
    tag = models.CharField(
        _("Étiquette"),
        max_length=10,
        choices=Tag.choices,
        default=Tag.VERT
    )

    # Kilométrage général
    kilometres_total = models.PositiveIntegerField(_("Kilométrage total"), default=0)
    kilometres_derniere_intervention = models.PositiveIntegerField(
        _("Kilométrage à la dernière intervention"),
        null=True,
        blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(_("Kilométrage châssis"), null=True, blank=True)

    # Kilométrage spécifiques
    kilometres_moteur = models.PositiveIntegerField(_("Kilométrage moteur"), default=0)
    kilometres_boite = models.PositiveIntegerField(_("Kilométrage boîte"), default=0)

    # Suivi des remplacements
    remplacement_moteur = models.BooleanField(_("Remplacement moteur"), default=False)
    remplacement_boite = models.BooleanField(_("Remplacement boîte"), default=False)

    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")

    @property
    def kilometres_calcules(self):
        """Kilomètres depuis la dernière intervention"""
        if self.kilometres_derniere_intervention is not None:
            return self.kilometres_total - self.kilometres_derniere_intervention
        return None

    def save(self, *args, **kwargs):
        # Remise à zéro des compteurs si remplacement
        if self.remplacement_moteur:
            self.kilometres_moteur = 0
        if self.remplacement_boite:
            self.kilometres_boite = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return _("Maintenance %(voiture)s (%(date)s)") % {
            "voiture": self.voiture_exemplaire or self.immatriculation,
            "date": self.date_intervention
        }



    def verifier_entretiens(km_actuel):
        entretiens = Entretien.objects.filter(termine=False)
        return [
            e for e in entretiens if e.doit_alerter(km_actuel)
        ]
