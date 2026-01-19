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


class TypePlateauPression(models.TextChoices):
    CLASSIQUE = "CLASSIQUE", _("Classique (mono-disque)")
    RESSORTS_CONCENTRIQUES = "CONCENTRIQUES", _("Ressorts concentriques")
    RESSORTS_HELICOIDAUX = "HELICOIDAUX", _("Ressorts hélicoïdaux")
    RENFORCE = "RENFORCE", _("Renforcé / Compétition")
    BIMASSE = "BIMASSE", _("Bimasse (pour volant moteur DMF)")



class VoitureEmbrayage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations (1 des 2 obligatoire)
    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.CASCADE,
        related_name="embrayages",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="embrayages",
        null=True,
        blank=True
    )
    fabricant = models.CharField(max_length=30, null=True, blank=True)

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

    kilometrage_embrayage = models.PositiveIntegerField(
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

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(numero_embrayage__gte=1) & Q(numero_embrayage__lte=10),
                name="numero_embrayage_1_10"
            ),
            models.CheckConstraint(
                condition=Q(voiture_modele__isnull=False) | Q(voiture_exemplaire__isnull=False),
                name="embrayage_liée_a_voiture"
            ),
        ]

    def __str__(self):
        return f"Boîte #{self.numero_embrayage} - {self.kilometrage_embrayage} km"

    def remplacer_embrayage(self):
        if self.numero_embrayage < 10:
            self.numero_embrayage += 1
            self.kilometrage_boite = 0
            self.save()