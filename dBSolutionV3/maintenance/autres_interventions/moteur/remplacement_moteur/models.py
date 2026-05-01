import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
from django.conf import settings
from societe.models import Societe
from voiture.voiture_exemplaire.utils_vin import get_vin_year
from voiture.voiture_exemplaire.models import VoitureExemplaire
from maintenance.niveaux.models import Niveau, NiveauxEtat, validate_step_0_1, HuileEtat, RefroidissementQualiteEtat
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin


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



class RemplacementMoteur(TechnicienMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    TVA_PIECES = {
        'BE': 21,
        'LU': 16,
        'DE': 19,
    }

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )



    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="remplacement_moteur"
    )

    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.PROTECT,
        related_name="remplacement_moteur"
    )

    voiture_moteur = models.ForeignKey(
        "voiture_moteur.MoteurVoiture",
        on_delete=models.PROTECT,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    proprietaire = models.ForeignKey(
        "proprietaire.ProprietaireVoiture",
        on_delete=models.PROTECT,
        related_name="remplacement_moteur",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )


    immatriculation = models.CharField(
        max_length=10,
        unique=True,
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
        verbose_name=_("Numéro VIN"),
        validators=[vin_validator],
        null=True,
        blank=True,
    )
    vin_simplifie = models.CharField(
        max_length=10,
        verbose_name=_("VIN simplifié"),
        editable=False,
        blank=True,
        null=True,
    )
    est_apres_2010 = models.BooleanField(default=True)

    annee_production = models.PositiveIntegerField(
        verbose_name=_("Année de production"),
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


    kilometres_dernier_entretien = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_remplacement_moteur = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres au remplacement moteur")
    )

    variation_kilometres = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variationde kilomètres depuis le dernier entretien"),
        help_text=_("Calculé automatiquement : total - dernièr entretien")
    )

    date_derniere_intervention = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Date de derniere entretien"),
    )

    remplacement_numero_moteur = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name=_("Numéro de série du moteur")
    )

    remplacement_nombre_moteur = models.PositiveIntegerField(
        default=1,
        null=True,
        blank=True,
        verbose_name=_("Nombre de moteur")
    )


    prix_moteur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix moteur"),
    )


    client = models.ForeignKey(
        ClientParticulier,
        on_delete=models.CASCADE,
        related_name="remplacement_moteur",
        null=True,
        blank=True,
        verbose_name=_("Client"),
    )

    last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="remplacement_moteur_maintained",
        verbose_name=_("Dernière maintenance effectuée par")
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

    niveaux = models.ForeignKey(
        Niveau,
        on_delete=models.PROTECT,
        related_name="remplacement_moteur",
        verbose_name=_("Niveaux"),
        null=True,
        blank=True
    )

    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"),validators=[validate_step_0_1])
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))


    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"), validators=[validate_step_0_1])
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))



    remplacement_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement effectué"),
    )

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="remplacement_moteur"
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="remplacement_moteur"
    )
    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="remplacement_moteur",
        verbose_name=_("Main d'oeuvre")
    )

    temps_minutes = models.PositiveIntegerField(default=0)


    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)



    def __str__(self):
        return f"{self.voiture_marque.nom_marque} {self.voiture_modele.nom_modele} {self.voiture_modele.nom_variante} - {self.immatriculation}"

    def save(self, *args, **kwargs):
        ancien_remplacement = False

        if self.pk:
            ancien_remplacement = type(self).objects.filter(pk=self.pk) \
                .values_list("remplacement_effectue", flat=True) \
                .first()

        # 🚗 VIN
        if self.numero_vin:
            self.numero_vin = self.numero_vin.upper()

            if len(self.numero_vin) == 17:
                self.vin_simplifie = self.numero_vin[-10:]

                try:
                    dixieme = self.numero_vin[9]
                    self.annee_production = get_vin_year(dixieme)
                except Exception:
                    self.annee_production = None
            else:
                self.vin_simplifie = None
                self.annee_production = None
        else:
            self.vin_simplifie = None
            self.annee_production = None

        # 🔁 Détection réelle du remplacement moteur
        if self.remplacement_effectue and not ancien_remplacement:
            self.kilometres_remplacement_moteur = self.kilometres_chassis or 0

        # 🔄 Mise à jour km
        self.update_kilometres()

        super().save(*args, **kwargs)

    def update_kilometres(self):
        km_chassis = self.kilometres_chassis or 0

        self.variation_kilometres = max(
            0,
            km_chassis - (self.kilometres_dernier_entretien or 0)
        )

        if self.kilometres_remplacement_moteur is not None:
            self.kilometres_moteur = max(
                0,
                km_chassis - self.kilometres_remplacement_moteur
            )
        else:
            self.kilometres_moteur = km_chassis