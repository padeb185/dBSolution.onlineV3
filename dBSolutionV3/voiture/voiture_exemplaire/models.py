
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
    kilometres_remplacement_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_remplacement_boite = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_remplacement_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Calculé automatiquement : total - dernièr entretien"
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

    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele.nom_modele} {self.voiture_modele.nom_variante} - {self.immatriculation}"

    def save(self, *args, **kwargs):
        # 🚗 VIN
        if self.numero_vin:
            self.numero_vin = self.numero_vin.upper()
            self.vin_simplifie = self.numero_vin[-10:]
            dixieme = self.numero_vin[9]
            self.annee_production = get_vin_year(dixieme)
        else:
            self.vin_simplifie = None
            self.annee_production = None

        # 🔄 Mise à jour automatique des kilométrages si le kilométrage châssis change
        if self.pk:  # Si l'objet existe déjà
            ancien = VoitureExemplaire.objects.get(pk=self.pk)
            if ancien.kilometres_chassis != self.kilometres_chassis:
                self.update_kilometres()
        else:  # Nouvel objet
            self.update_kilometres()

        # ⚠️ Sauvegarde finale de l'exemplaire
        super().save(*args, **kwargs)

    def update_kilometres(self):
        """
        Synchronise tous les kilométrages avec kilometres_chassis.
        Si un composant a été remplacé, son compteur part de 0.
        """
        km_chassis = self.kilometres_chassis or 0

        # Variation depuis le dernier entretien
        self.variation_kilometres = max(0, km_chassis - (self.kilometres_dernier_entretien or 0))

        # Kilométrages des composants
        if self.kilometres_remplacement_moteur:
            self.kilometres_moteur = km_chassis - self.kilometres_remplacement_moteur
        else:
            self.kilometres_moteur = km_chassis

        if self.kilometres_remplacement_boite:
            self.kilometres_boite = km_chassis - self.kilometres_remplacement_boite
        else:
            self.kilometres_boite = km_chassis

        if self.kilometres_remplacement_embrayage:
            self.kilometres_embrayage = km_chassis - self.kilometres_remplacement_embrayage
        else:
            self.kilometres_embrayage = km_chassis