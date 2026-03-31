import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.entretien.models import Entretien



class TypeAutres(models.TextChoices):
    BOITE = "boite", _("Boite")
    ENTRETIEN = "entretien", _("Entretien")
    FREINS = "freins", _("Freins")
    PNEUS = "pneus", _("Pneus")
    NETTOYAGE_EXTERIEUR = "nettoyage_exterieur", _("Nettoyage extérieur")
    NETTOYAGE_INTERIEUR = "nettoyage_interieur", _("Nettoyage intérieur")
    NIVEAUX = "niveaux", _("Niveaux")
    AUTRES = "autres", _("Autres interventions")



class AutresInterventions(models.Model):
    class Tag(models.TextChoices):
        VERT = "VERT", _("Vert")
        JAUNE = "JAUNE", _("Jaune")
        ROUGE = "ROUGE", _("Rouge")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="autres_interventions",
        null=True,
        blank=True,
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        verbose_name=_("Voiture exemplaire"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="autres_interventions"
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
        default=Tag.JAUNE
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


    type_maintenance = models.CharField(
        _("Type de maintenance"),
        max_length=50,
        choices=TypeAutres.choices,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")

    @property
    def kilometres_calcules(self):
        """Kilomètres depuis la dernière intervention"""
        if self.kilometres_derniere_intervention is not None:
            return self.kilometres_total - self.kilometres_derniere_intervention
        return None


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

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe