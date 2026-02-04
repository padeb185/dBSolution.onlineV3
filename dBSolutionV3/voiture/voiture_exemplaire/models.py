import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings

class TypeUtilisation(models.TextChoices):
    SOCIETE = "societe", _("Société")
    CLIENT = "client", _("Client")
    PRIVE = "prive", _("Privé")
    LOCATION = "location", _("Location")


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

    # 🚗 Identification
    immatriculation = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True
    )

    pays = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    numero_vin = models.CharField(
        max_length=17,
        unique=True,
        verbose_name="Numéro VIN",
        null=True,
        blank=True,
    )

    type_utilisation = models.CharField(
        max_length=10,
        choices=TypeUtilisation.choices,
        default=TypeUtilisation.CLIENT
    )

    # 📏 Kilométrage châssis
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_total = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_derniere_intervention = models.PositiveIntegerField(default=0, null=True, blank=True)

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Calculé automatiquement : total - dernière intervention"
    )

    date_derniere_intervention = models.DateField(blank=True, null=True)

    # 🏭 Production
    annee_production = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(timezone.now().year + 1)]
    )

    mois_production = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    # ⚙️ Moteur / transmission
    numero_moteur = models.CharField(max_length=50, null=True, blank=True)

    date_mise_en_circulation = models.DateField(null=True, blank=True)

    kilometres_moteur = models.PositiveIntegerField(default=0)
    nombre_moteurs = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    kilometres_boite_vitesse = models.PositiveIntegerField(default=0)
    nombre_boites_vitesse = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0)
    nombre_embrayages = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(15)]
    )

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


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ⚙️ Logique métier
    def save(self, *args, **kwargs):
        self.variation_kilometres = max(
            0,
            self.kilometres_total - self.kilometres_derniere_intervention
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.immatriculation} ({self.voiture_marque} {self.voiture_modele})"
