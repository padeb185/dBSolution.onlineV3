
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from societe.models import Societe
from voiture.voiture_exemplaire.utils_vin import get_vin_year


class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")
    INTERNE = "interne", _("Interne")

class NomPays(models.TextChoices):
    BE = "Belgique", _("Belgique")
    LU = "Luxembourg", _("Luxembourg")
    DE = "Allemagne", _("Allemagne")



class VoitureExemplaire(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="voitures"
    )

    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.PROTECT,
        related_name="voitures"
    )

    voiture_embrayage = models.ForeignKey(
        "voiture_embrayage.VoitureEmbrayage",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    voiture_boite = models.ForeignKey(
        "voiture_boite.VoitureBoite",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    voiture_moteur = models.ForeignKey(
        "voiture_moteur.MoteurVoiture",
        on_delete=models.PROTECT,
        related_name="voitures",
        null=True,
        blank=True
    )

    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    # 🚗 Identification
    immatriculation = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    pays = models.CharField(
        max_length=20,
        choices=NomPays.choices,
        null=True,
        blank=True
    )

    vin_validator = RegexValidator(
        regex=r'^[A-HJ-NPR-Z0-9]{17}$',
        message=_("Le numéro VIN doit contenir exactement 17 caractères alphanumériques (lettres A-H, J-N, P, R-Z et chiffres).")
    )

    numero_vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="Numéro VIN",
        validators=[vin_validator],
        null=True,
        blank=True,
    )
    vin_simplifie = models.CharField(
        max_length=10,
        verbose_name="VIN simplifié",
        editable=False,
        blank=True,
        null=True,
    )
    est_apres_2010 = models.BooleanField(default=True)

    annee_production = models.PositiveIntegerField(
        verbose_name="Année de production",
        editable=False,
        blank=True,
        null=True,
    )
    mois_production = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    type_utilisation = models.CharField(
        max_length=10,
        choices=TypeUtilisation.choices,
        default=TypeUtilisation.CLIENT
    )

    # 📏 Kilométrage châssis
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_dernier_entretien = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Calculé automatiquement : total - dernière intervention"
    )

    date_derniere_intervention = models.DateField(blank=True, null=True)

    # 🏭 Production




    # ⚙️ Moteur / transmission
    numero_moteur = models.CharField(max_length=50, null=True, blank=True)

    date_mise_en_circulation = models.DateField(null=True, blank=True)


    couleur = models.CharField(max_length=50, blank=True, null=True)
    code_couleur = models.CharField(max_length=50, blank=True, null=True)

    # 💰 Données financières
    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    assurance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    taxe_mise_en_circulation = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    taxe_roulage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # 👥 Propriétaires
    nombre_proprietaires = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )

    part_proprietaires_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True
    )

    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="exemplaires",
        null=True,
        blank=True
    )


    last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="entretien_voitures"
    )

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]

    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="JAUNE",
        verbose_name=_("État visuel / Tag"),
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        # 🚗 VIN
        if self.numero_vin:
            self.numero_vin = self.numero_vin.upper()

            # VIN simplifié
            self.vin_simplifie = self.numero_vin[-10:]

            # Année via VIN (10e caractère = index 9)
            dixieme = self.numero_vin[9]
            self.annee_production = get_vin_year(dixieme)
        else:
            self.vin_simplifie = None
            self.annee_production = None

            # Met à jour tous les kilométrages
        self.update_kilometres()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatriculation} ({self.voiture_marque} {self.voiture_modele})"

    def update_kilometres(self):
        """
        Met à jour tous les kilométrages dépendants de kilometres_chassis
        """
        # Variation depuis le dernier entretien
        if self.kilometres_chassis is not None and self.kilometres_dernier_entretien is not None:
            self.variation_kilometres = max(0, self.kilometres_chassis - self.kilometres_dernier_entretien)
        else:
            self.variation_kilometres = 0

        # Kilométrages des composants
        if self.voiture_moteur:
            self.kilometres_moteur = max(0,
                                         self.kilometres_chassis - self.voiture_moteur.kilometres_remplacement_moteur)

        if self.voiture_boite:
            self.kilometres_boite = max(0, self.kilometres_chassis - self.voiture_boite.kilometres_remplacement_boite)

        if self.voiture_embrayage:
            self.kilometres_embrayage = max(0,
                                            self.kilometres_chassis - self.voiture_embrayage.kilometres_remplacement_embrayage)

