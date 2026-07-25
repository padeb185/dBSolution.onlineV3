from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES

from maintenance.models import Maintenance
from maindoeuvre.models import MainDoeuvre
from utils.mixin import TechnicienMixin


# ==========================================================
# CHOIX
# ==========================================================

class EtatRefroidissement(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")



class EtatInterventionRefroidissement(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("À faire")
    FAIT = "FAIT", _("Fait")
    REPORTE = "REPORTE", _("Reporté")


class EtatLiquideRefroidissement(models.TextChoices):
    BON = "BON", _("Bon")
    A_COMPLETER = "A_COMPLETER", _("À compléter")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class QualiteLiquideRefroidissement(models.TextChoices):
    BONNE = "BONNE", _("Bonne")
    MOYENNE = "MOYENNE", _("Moyenne")
    MAUVAISE = "MAUVAISE", _("Mauvaise")
    CONTAMINE = "CONTAMINE", _("Contaminé")


class Refroidissement(TechnicienMixin, models.Model):

    # ======================================================
    # TVA
    # ======================================================

    TVA_PIECES = {
        "BE": Decimal("21.00"),
        "LU": Decimal("16.00"),
        "DE": Decimal("19.00"),
    }

    PAYS_CHOICES = [
        ("BE", _("Belgique")),
        ("LU", _("Luxembourg")),
        ("DE", _("Allemagne")),
    ]

    # ======================================================
    # RELATIONS
    # ======================================================

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controles_refroidissement",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True,
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controles_refroidissement",
        verbose_name=_("Véhicule"),
        null=True,
        blank=True,
    )

    main_oeuvre = models.ForeignKey(
        MainDoeuvre,
        on_delete=models.SET_NULL,
        related_name="controles_refroidissement",
        verbose_name=_("Main-d'œuvre"),
        null=True,
        blank=True,
    )

    # ======================================================
    # INFORMATIONS GÉNÉRALES
    # ======================================================

    date_controle = models.DateField(
        verbose_name=_("Date du contrôle"),
        auto_now_add=True,
    )
    kilometres_chassis = models.PositiveIntegerField(
        verbose_name=_("Kilométrage du châssis"),
        default=0,
        blank=True,
    )

    kilometrage_refroidissement = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
    )



    pays = models.CharField(
        max_length=2,
        choices=PAYS_CHOICES,
        verbose_name=_("Pays"),
        default="BE",
    )

    # ======================================================
    # DIAGNOSTIC GÉNÉRAL
    # ======================================================

    presence_fuite = models.BooleanField(
        verbose_name=_("Présence d'une fuite"),
        default=False,
    )

    presence_fuite_localisation = models.TextField(
        verbose_name=_("Localisation de la fuite"),
        blank=True,
    )

    pression_circuit = models.DecimalField(
        verbose_name=_("Pression du circuit"),
        help_text=_("Pression mesurée en bar"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    pression_circuit_constructeur = models.DecimalField(
        verbose_name=_("Pression constructeur"),
        help_text=_("Pression constructeur en bar"),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    temperature_moteur = models.DecimalField(
        verbose_name=_("Température du moteur"),
        help_text=_("Température mesurée en °C"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )

    temperature_declenchement_ventilateur = models.DecimalField(
        verbose_name=_("Température de déclenchement du ventilateur"),
        help_text=_("Température mesurée en °C"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )

    temperature_sortie_chauffage = models.DecimalField(
        verbose_name=_("Température de sortie du chauffage"),
        help_text=_("Température mesurée en °C"),
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )

    montee_en_temperature_normale = models.BooleanField(
        verbose_name=_("Montée en température normale"),
        default=True,
    )

    maintien_temperature_normal = models.BooleanField(
        verbose_name=_("Maintien de la température normal"),
        default=True,
    )

    circulation_liquide_correcte = models.BooleanField(
        verbose_name=_("Circulation du liquide correcte"),
        default=True,
    )

    # ======================================================
    # LIQUIDE DE REFROIDISSEMENT
    # ======================================================

    liquide_etat = models.CharField(
        max_length=20,
        choices=EtatLiquideRefroidissement.choices,
        verbose_name=_("État du liquide de refroidissement"),
        default=EtatLiquideRefroidissement.BON,
    )

    liquide_qualite = models.CharField(
        max_length=20,
        choices=QualiteLiquideRefroidissement.choices,
        verbose_name=_("Qualité du liquide de refroidissement"),
        default=QualiteLiquideRefroidissement.BONNE,
    )

    liquide_type = models.CharField(
        max_length=100,
        verbose_name=_("Type de liquide de refroidissement"),
        blank=True,
    )

    liquide_couleur = models.CharField(
        max_length=50,
        verbose_name=_("Couleur du liquide de refroidissement"),
        blank=True,
    )

    liquide_temperature_protection = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name=_("Température de protection du liquide"),
        help_text=_("Protection antigel mesurée en °C"),
        null=True,
        blank=True,
    )

    liquide_quantite = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name=_("Quantité de liquide utilisée"),
        help_text=_("Quantité en litres"),
        default=Decimal("0.00"),
    )

    liquide_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du liquide de refroidissement"),
        default=Decimal("0.00"),
    )



    # ======================================================
    # PURGE
    # ======================================================

    purge_circuit = models.CharField(
        max_length=15,
        choices=EtatInterventionRefroidissement.choices,
        verbose_name=_("Purge du circuit de refroidissement"),
        default=EtatInterventionRefroidissement.A_FAIRE,
    )

    purge_presence_air = models.BooleanField(
        verbose_name=_("Présence d'air dans le circuit"),
        default=False,
    )

    purge_effectuee_sous_vide = models.BooleanField(
        verbose_name=_("Purge effectuée sous vide"),
        default=False,
    )

    purge_remarques = models.TextField(
        verbose_name=_("Remarques concernant la purge"),
        blank=True,
    )

    # ======================================================
    # VENTILATEUR
    # ======================================================

    ventilateur_etat = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Ventilateur de refroidissement"),
        default=EtatRefroidissement.OK,
    )

    ventilateur_declenchement = models.BooleanField(
        verbose_name=_("Déclenchement du ventilateur"),
        default=True,
    )

    ventilateur_vitesse_1 = models.BooleanField(
        verbose_name=_("Première vitesse du ventilateur"),
        default=True,
    )

    ventilateur_vitesse_2 = models.BooleanField(
        verbose_name=_("Deuxième vitesse du ventilateur"),
        default=True,
    )

    ventilateur_bruit_anormal = models.BooleanField(
        verbose_name=_("Bruit anormal du ventilateur"),
        default=False,
    )

    ventilateur_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du ventilateur"),
        default=Decimal("0.00"),
    )

    ventilateur_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de ventilateurs"),
        default=0,
    )


    # ======================================================
    # RADIATEUR
    # ======================================================

    radiateur = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Radiateur moteur"),
        default=EtatRefroidissement.OK,
    )

    radiateur_fuite = models.BooleanField(
        verbose_name=_("Fuite au radiateur"),
        default=False,
    )

    radiateur_obstruction = models.BooleanField(
        verbose_name=_("Radiateur obstrué"),
        default=False,
    )

    radiateur_ailettes_endommagees = models.BooleanField(
        verbose_name=_("Ailettes du radiateur endommagées"),
        default=False,
    )

    radiateur_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du radiateur"),
        default=Decimal("0.00"),
    )

    radiateur_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de radiateurs"),
        default=1,
    )


    # ======================================================
    # THERMOSTAT
    # ======================================================

    thermostat = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Thermostat"),
        default=EtatRefroidissement.OK,
    )

    thermostat_ouverture_correcte = models.BooleanField(
        verbose_name=_("Ouverture correcte du thermostat"),
        default=True,
    )

    thermostat_temperature_ouverture = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name=_("Température d'ouverture du thermostat"),
        help_text=_("Température en °C"),
        null=True,
        blank=True,
    )

    thermostat_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du thermostat"),
        default=Decimal("0.00"),
    )

    thermostat_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de thermostats"),
        default=1,
    )

    # ======================================================
    # BOÎTIER D'EAU
    # ======================================================

    boitier_eau = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Boîtier d'eau"),
        default=EtatRefroidissement.OK,
    )

    boitier_eau_fuite = models.BooleanField(
        verbose_name=_("Fuite au boîtier d'eau"),
        default=False,
    )

    boitier_eau_fissure = models.BooleanField(
        verbose_name=_("Fissure du boîtier d'eau"),
        default=False,
    )

    boitier_eau_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du boîtier d'eau"),
        default=Decimal("0.00"),
    )

    boitier_eau_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de boîtiers d'eau"),
        default=1,
    )


    # ======================================================
    # SONDE DE TEMPÉRATURE
    # ======================================================

    sonde_t_etat = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Sonde de température du liquide"),
        default=EtatRefroidissement.OK,
    )

    sonde_t_valeur = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        verbose_name=_("Valeur mesurée par la sonde"),
        help_text=_("Température mesurée en °C"),
        null=True,
        blank=True,
    )

    sonde_t_signal_correct = models.BooleanField(
        verbose_name=_("Signal de la sonde correct"),
        default=True,
    )

    sonde_t_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA de la sonde de température"),
        default=Decimal("0.00"),
    )

    sonde_t_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de sondes de température"),
        default=1,
    )

    # ======================================================
    # DURITES
    # ======================================================

    durites = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Durites de refroidissement"),
        default=EtatRefroidissement.OK,
    )

    durites_fissurees = models.BooleanField(
        verbose_name=_("Durites fissurées"),
        default=False,
    )

    durites_poreuses = models.BooleanField(
        verbose_name=_("Durites poreuses"),
        default=False,
    )

    durites_gonflees = models.BooleanField(
        verbose_name=_("Durites gonflées"),
        default=False,
    )

    durites_colliers_corrects = models.BooleanField(
        verbose_name=_("Colliers des durites correctement serrés"),
        default=True,
    )

    durites_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA des durites"),
        default=Decimal("0.00"),
    )

    durites_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de durites"),
        default=1,
    )


    # ======================================================
    # CHAUFFERETTE / RADIATEUR DE CHAUFFAGE
    # ======================================================

    chaufferette = models.CharField(
        max_length=20,
        choices=EtatRefroidissement.choices,
        verbose_name=_("Radiateur de chauffage"),
        default=EtatRefroidissement.OK,
    )

    chaufferette_fuite = models.BooleanField(
        verbose_name=_("Fuite au radiateur de chauffage"),
        default=False,
    )

    chaufferette_obstruction = models.BooleanField(
        verbose_name=_("Radiateur de chauffage obstrué"),
        default=False,
    )

    chaufferette_chauffage_correct = models.BooleanField(
        verbose_name=_("Fonctionnement correct du chauffage"),
        default=True,
    )

    chaufferette_odeur_liquide = models.BooleanField(
        verbose_name=_("Odeur de liquide dans l'habitacle"),
        default=False,
    )

    chaufferette_buee_anormale = models.BooleanField(
        verbose_name=_("Buée anormale dans l'habitacle"),
        default=False,
    )

    chaufferette_prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HTVA du radiateur de chauffage"),
        default=Decimal("0.00"),
    )

    chaufferette_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité de radiateurs de chauffage"),
        default=1,
    )



    # ======================================================
    # REMARQUES ET ÉTIQUETTE
    # ======================================================

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
    )

    tag = models.CharField(
        max_length=10,
        choices=Maintenance.Tag.choices,
        verbose_name=_("Étiquette"),
        default=Maintenance.Tag.JAUNE,
    )

    # ------------------------------------------------------
    # TECHNICIEN
    # ------------------------------------------------------

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="refroidissement",
    )

    tech_nom_technicien = models.CharField(
        _("Nom du technicien"),
        max_length=255,
        blank=True,
    )

    tech_role_technicien = models.CharField(
        _("Rôle du technicien"),
        max_length=255,
        blank=True,
    )

    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="refroidissement",
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date"),
    )

    created_at = models.DateTimeField(
        _("Créé le"),
        auto_now_add=True,
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        _("Mis à jour le"),
        auto_now=True,
        blank=True,
        null=True,
    )



    class Meta:
        verbose_name = _("Contrôle du système de refroidissement")
        verbose_name_plural = _("Contrôles du système de refroidissement")
        ordering = ["-date_controle", "-id"]

    def __str__(self):
        vehicule = self.voiture_exemplaire or _("Véhicule inconnu")
        return _("Contrôle refroidissement — %(vehicule)s") % {
            "vehicule": vehicule,
        }

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    # ======================================================
    # VALIDATION
    # ======================================================

    def clean(self):
        super().clean()

        erreurs = {}

        champs_numeriques = [
            "liquide_prix_achat",
            "liquide_quantite",
            "ventilateur_prix_achat",
            "ventilateur_quantite",
            "radiateur_prix_achat",
            "radiateur_quantite",
            "thermostat_prix_achat",
            "thermostat_quantite",
            "boitier_eau_prix_achat",
            "boitier_eau_quantite",
            "sonde_t_prix_achat",
            "sonde_t_quantite",
            "durites_prix_achat",
            "durites_quantite",
        ]

        for nom_champ in champs_numeriques:
            valeur = getattr(self, nom_champ, None)

            if valeur is not None and valeur < 0:
                erreurs[nom_champ] = _(
                    "Cette valeur ne peut pas être négative."
                )

        if (
                self.presence_fuite
                and not self.presence_fuite_localisation
        ):
            erreurs["presence_fuite_localisation"] = _(
                "Précisez la localisation de la fuite."
            )

        if erreurs:
            raise ValidationError(erreurs)

    # ======================================================
    # CALCUL DES PIÈCES
    # ======================================================

    def calcul_piece(self, prefix):
        prix_achat = getattr(
            self,
            f"{prefix}_prix_achat",
            Decimal("0.00"),
        ) or Decimal("0.00")

        quantite = getattr(
            self,
            f"{prefix}_quantite",
            1,
        ) or 0

        taux_tva = (
            Decimal(str(self.TVA_PIECES.get(self.pays, Decimal("0.00"))))
            / Decimal("100")
        )

        prix_achat = Decimal(str(prix_achat))
        quantite = Decimal(str(quantite))

        total_achat = prix_achat * quantite

        tva_achat = (total_achat * taux_tva).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        prix_vente_htva = total_achat.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        tva_vente = (prix_vente_htva * taux_tva).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        prix_ttc = (prix_vente_htva + tva_vente).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        setattr(self, f"{prefix}_tva_achat", tva_achat)
        setattr(
            self,
            f"{prefix}_prix_vente_htva",
            prix_vente_htva,
        )
        setattr(self, f"{prefix}_tva_vente", tva_vente)
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)



    def calcul_liquide(self):
        prix_achat = self.liquide_prix_achat or Decimal("0.00")
        quantite = self.liquide_quantite or Decimal("0.00")

        taux_tva = (
            Decimal(str(self.TVA_PIECES.get(self.pays, Decimal("0.00"))))
            / Decimal("100")
        )

        total_achat = Decimal(str(prix_achat)) * Decimal(str(quantite))

        self.liquide_tva_achat = (total_achat * taux_tva).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        self.liquide_prix_vente_htva = total_achat.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        self.liquide_tva_vente = (
            self.liquide_prix_vente_htva * taux_tva
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        self.liquide_prix_ttc = (
            self.liquide_prix_vente_htva
            + self.liquide_tva_vente
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    # ======================================================
    # SYNCHRONISATION DU KILOMÉTRAGE
    # ======================================================

    def sync_kilometrage(self):
        if not self.voiture_exemplaire_id:
            return

        if self.kilometrage_refroidissement is None:
            return

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        kilometrage_actuel = voiture.kilometres_chassis or 0
        nouveau_kilometrage = self.kilometrage_refroidissement

        if nouveau_kilometrage < kilometrage_actuel:
            raise ValidationError({
                "kilometrage_refroidissement": _(
                    "Le kilométrage ne peut pas être inférieur au "
                    "kilométrage actuel du véhicule."
                )
            })

        voiture.kilometres_chassis = nouveau_kilometrage
        voiture.save(update_fields=["kilometres_chassis"])

        self.kilometres_chassis = nouveau_kilometrage

    # ======================================================
    # SAVE
    # ======================================================

    def save(self, *args, **kwargs):
        self.full_clean()

        self.sync_kilometrage()

        prefixes = [
            "ventilateur",
            "radiateur",
            "thermostat",
            "boitier_eau",
            "sonde_t_",
            "durites",
            "chaufferette",
        ]

        for prefix in prefixes:
            self.calcul_piece(prefix)

        self.calcul_liquide()

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            self.main_oeuvre.descriptif = _(
                "Contrôle du système de refroidissement — %(vehicule)s"
            ) % {
                "vehicule": self.voiture_exemplaire,
            }

            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        super().save(*args, **kwargs)

    # ======================================================
    # RAPPORT DES PIÈCES
    # ======================================================

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        composants = [
            {
                "etat_champ": "ventilateur_etat",
                "prefix": "ventilateur",
                "libelle": _("Ventilateur"),
            },
            {
                "etat_champ": "radiateur",
                "prefix": "radiateur",
                "libelle": _("Radiateur"),
            },
            {
                "etat_champ": "thermostat",
                "prefix": "thermostat",
                "libelle": _("Thermostat"),
            },
            {
                "etat_champ": "boitier_eau",
                "prefix": "boitier_eau",
                "libelle": _("Boîtier d'eau"),
            },
            {
                "etat_champ": "sonde_t_etat",
                "prefix": "sonde_t",
                "libelle": _("Sonde de température du liquide"),
            },
            {
                "etat_champ": "durites",
                "prefix": "durites",
                "libelle": _("Durites"),
            },
            {
                "etat_champ": "chaufferette",
                "prefix": "chaufferette",
                "libelle": _("Radiateur de chauffage"),
            },
        ]

        etats_a_facturer = {
            EtatRefroidissement.A_REMPLACER,
            EtatRefroidissement.REMPLACE,
        }

        for composant in composants:
            etat_champ = composant["etat_champ"]
            prefix = composant["prefix"]
            libelle = composant["libelle"]

            etat = getattr(self, etat_champ, None)

            if etat not in etats_a_facturer:
                continue

            prix = getattr(
                self,
                f"{prefix}_prix_achat",
                Decimal("0.00"),
            ) or Decimal("0.00")

            quantite = getattr(
                self,
                f"{prefix}_quantite",
                0,
            ) or 0

            prix = Decimal(str(prix))
            quantite = Decimal(str(quantite))

            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": libelle,
                "code": prefix,
                "etat": etat,
                "etat_label": dict(
                    EtatRefroidissement.choices
                ).get(etat, etat),
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        if (
                self.liquide_etat
                in {
            EtatLiquideRefroidissement.A_REMPLACER,
            EtatLiquideRefroidissement.REMPLACE,
            EtatLiquideRefroidissement.A_COMPLETER,
        }
                and self.liquide_quantite
        ):
            prix_liquide = (
                    self.liquide_prix_achat or Decimal("0.00")
            )

            quantite_liquide = (
                    self.liquide_quantite or Decimal("0.00")
            )

            prix_liquide = Decimal(str(prix_liquide))
            quantite_liquide = Decimal(str(quantite_liquide))

            total_liquide = prix_liquide * quantite_liquide
            total_general += total_liquide

            rapport.append({
                "champ": _("Liquide de refroidissement"),
                "code": "liquide_refroidissement",
                "etat": self.liquide_etat,
                "etat_label": self.get_liquide_etat_display(),
                "prix": prix_liquide,
                "quantite": quantite_liquide,
                "total": total_liquide,
            })

        return {
            "lignes": rapport,
            "total_general": total_general.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
        }

    # ======================================================
    # MAIN-D'ŒUVRE
    # ======================================================

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        heures, minutes = divmod(temps_minutes, 60)

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if (
            self.main_oeuvre
            and self.main_oeuvre.taux_horaire is not None
        ):
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = (
            self.main_oeuvre.taux_horaire or Decimal("0.00")
        )

        cout = (
            Decimal(str(temps_minutes))
            / Decimal("60")
            * Decimal(str(taux_horaire))
        )

        return cout.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()

        return (
            rapport["total_general"]
            + self.cout_main_oeuvre
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )