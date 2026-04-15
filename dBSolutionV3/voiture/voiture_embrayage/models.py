import uuid
from django.db.models import Q
from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeEmbrayage(models.TextChoices):
    MONDISQUE = "MONDISQUE", _("Monodisque")
    MULTIDISQUE = "MULTIDISQUE", _("Multidisque")
    AUTOMATIQUE = "AUTOMATIQUE", _("Automatique")
    HYDRAULIQUE = "HYDRAULIQUE", _("Hydraulique")
    MECANIQUE = "MECANIQUE", _("Mécanique")

class TypeVolantMoteur(models.TextChoices):
    MONOMASSE = "MONOMASSE", _("Monomasse")
    BIMASSE = "BIMASSE", _("Bimasse")
    ALLEGE = "ALLEGE", _("Allégé / Performance")
    SEGMENTE = "SEGMENTE", _("Segmenté / Compétition")
    AUTOMATIQUE = "AUTOMATIQUE", _("Automatique / Plaque flexible")


class TypePlateauPression(models.TextChoices):
    CLASSIQUE = "CLASSIQUE", _("Classique (mono-disque)")
    RESSORTS_CONCENTRIQUES = "CONCENTRIQUES", _("Ressorts concentriques")
    RESSORTS_HELICOIDAUX = "HELICOIDAUX", _("Ressorts hélicoïdaux")
    RENFORCE = "RENFORCE", _("Renforcé / Compétition")
    BIMASSE = "BIMASSE", _("Bimasse (pour volant moteur DMF)")
    AUTOMATIQUE = "AUTOMATIQUE", _("Automatique / non présent")

class TypeButeeDEmbryage(models.TextChoices):
    MECANIQUE = "MECANIQUE", _("Mécanique")
    HYDRAULIQUE = "HYDRAULIQUE", _("Hydraulique")
    AROULEMENT = "AROULEMENT", _("A roulement")
    CONCENTRIQUES = "CONCENTRIQUES", _("Concentriques")
    ACABLE = "ACABLE", _("A cable")


class VoitureEmbrayage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="embrayages",
        null=True,
        blank=True,
    )

    # Relations (1 des 2 obligatoire)
    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="embrayages",
        blank=True
    )

    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="embrayages",
        blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True)

    fabricant = models.CharField(max_length=30, null=True, blank=True)

    oem = models.CharField(max_length=50, null=True, blank=True)

    type_embrayage = models.CharField(
        max_length=20,
        choices=TypeEmbrayage.choices,
        default=TypeEmbrayage.MONDISQUE,
        null=True,
        blank=True,
    )
    volant_moteur = models.CharField(
        max_length=30, choices=TypeVolantMoteur,
        default=TypeVolantMoteur.MONOMASSE,
        null=True, blank=True)

    plateau_pression = models.CharField(
        max_length=30, choices=TypePlateauPression.choices,
        default=TypePlateauPression.CLASSIQUE,
        null=True, blank=True

    )

    butee_embrayage = models.CharField(
        max_length=30, choices=TypeButeeDEmbryage.choices,
        default=TypeButeeDEmbryage.AROULEMENT,
        null=True,
        blank=True

    )

    kilometres_embrayage = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    numero_embrayage = models.PositiveSmallIntegerField(
        default=1,
        help_text="1 à 10 (incrémenté à chaque remplacement)",
        null=True,
        blank=True
    )
    kilometres_remplacement_embrayage = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    remarques = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [

        ]

    def __str__(self):
        return f"Embrayage #{self.numero_embrayage} - {self.kilometres_embrayage} km"

    def remplacer_embrayage(self):
        if self.numero_embrayage < 10:
            self.numero_embrayage += 1
            # On remet à zéro le kilométrage de l’embrayage
            self.kilometres_remplacement_embrayage = self.kilometres_chassis  # mise à jour du kilométrage de remplacement
            self.kilometres_embrayage = 0
            self.save()