from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantCapteur, TVAConfig, RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


PIECES_ELECTRONIQUE = [
    ("capteur_cliquetis", _("Capteur de cliquetis")),
    ("capteur_vilebrequin", _("Capteur de position de vilebrequin (PMH)")),
    ("capteur_arbre_cames", _("Capteur de position d'arbre à cames")),
    ("sonde_temperature_eau", _("Sonde de température de liquide de refroidissement")),
    ("sonde_temperature_air", _("Sonde de température d'air d'admission")),
    ("sonde_temperature_huile", _("Sonde de température d'huile")),
    ("sonde_temperature_echappement", _("Sonde de température des gaz d'échappement")),
    ("debitmetre", _("Débitmètre d'air (MAF)")),
    ("capteur_pression_admission", _("Capteur de pression d'admission (MAP)")),
    ("capteur_pression_suralimentation", _("Capteur de pression de suralimentation")),
    ("capteur_pression_huile", _("Capteur de pression d'huile")),
    ("capteur_pression_carburant", _("Capteur de pression de carburant (rampe)")),
    ("capteur_pression_differentielle", _("Capteur de pression différentielle (FAP)")),
    ("sonde_lambda_amont", _("Sonde lambda amont")),
    ("sonde_lambda_aval", _("Sonde lambda aval")),
    ("capteur_pedale", _("Capteur de position de pédale d'accélérateur")),
    ("capteur_niveau_huile", _("Capteur de niveau d'huile")),
    ("injecteurs", _("Injecteurs")),
    ("vanne_egr", _("Vanne EGR")),
    ("boitier_papillon", _("Boîtier papillon")),
    ("bobines_allumage", _("Bobines d'allumage")),
    ("bougies_prechauffage", _("Bougies / boîtier de préchauffage")),
    ("actionneur_turbo", _("Électrovanne / actionneur de turbo")),
    ("electrovanne_vvt", _("Électrovanne de déphaseur d'arbre à cames (VVT)")),
    ("regulateur_pression_carburant", _("Régulateur de pression de carburant")),
    ("electrovanne_canister", _("Électrovanne de purge canister")),
    ("volets_admission", _("Actionneur de volets d'admission (swirl)")),
    ("thermostat_pilote", _("Thermostat piloté")),
    ("motoventilateur", _("Motoventilateur")),
    ("calculateur_moteur", _("Calculateur moteur (ECU)")),
    ("faisceau_moteur", _("Faisceau moteur")),
    ("connecteurs", _("Connecteurs / cosses")),
]


class ElectroniqueMoteur(TechnicienMixin, models.Model):



    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )
    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="electronique_moteur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="electronique_moteur",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback")
    )


    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback moteur")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_electronique = models.PositiveIntegerField(
        verbose_name= _("Kilométrage de l'électronique moteur")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # PIECES
    # -------------------------
    def piece_fields(prefix):
        return {
            f"{prefix}": models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK),
            f"{prefix}_prix": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_quantite": models.IntegerField(default=0),
        }




    # -------------------------
    # DIAGNOSTIC
    # -------------------------
    diagnostic_codes_defaut = models.TextField(blank=True, default="", verbose_name=_("Codes défaut relevés (OBD)"), help_text=_("Ex. : P0325, P0401… un code par ligne avec sa description."))
    diagnostic_codes_effaces = models.BooleanField(default=False, verbose_name=_("Codes défaut effacés après intervention"))
    diagnostic_essai_routier = models.BooleanField(default=False, verbose_name=_("Essai routier effectué"))

    # -------------------------
    # CAPTEURS
    # -------------------------
    capteur_cliquetis = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de cliquetis"))
    capteur_cliquetis_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_cliquetis_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_cliquetis_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_vilebrequin = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de position de vilebrequin (PMH)"))
    capteur_vilebrequin_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_vilebrequin_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_vilebrequin_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_arbre_cames = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de position d'arbre à cames"))
    capteur_arbre_cames_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_arbre_cames_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_arbre_cames_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_temperature_eau = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde de température de liquide de refroidissement"))
    sonde_temperature_eau_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_temperature_eau_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_temperature_eau_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_temperature_air = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde de température d'air d'admission"))
    sonde_temperature_air_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_temperature_air_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_temperature_air_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_temperature_huile = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde de température d'huile"))
    sonde_temperature_huile_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_temperature_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_temperature_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_temperature_echappement = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde de température des gaz d'échappement"))
    sonde_temperature_echappement_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_temperature_echappement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_temperature_echappement_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    debitmetre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Débitmètre d'air (MAF)"))
    debitmetre_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    debitmetre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    debitmetre_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pression_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression d'admission (MAP)"))
    capteur_pression_admission_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pression_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pression_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pression_suralimentation = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression de suralimentation"))
    capteur_pression_suralimentation_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pression_suralimentation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pression_suralimentation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pression_huile = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression d'huile"))
    capteur_pression_huile_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pression_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pression_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pression_carburant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression de carburant (rampe)"))
    capteur_pression_carburant_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pression_carburant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pression_carburant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pression_differentielle = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression différentielle (FAP)"))
    capteur_pression_differentielle_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pression_differentielle_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pression_differentielle_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_lambda_amont = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde lambda amont"))
    sonde_lambda_amont_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_lambda_amont_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_lambda_amont_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sonde_lambda_aval = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sonde lambda aval"))
    sonde_lambda_aval_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    sonde_lambda_aval_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sonde_lambda_aval_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_pedale = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de position de pédale d'accélérateur"))
    capteur_pedale_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_pedale_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_pedale_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_niveau_huile = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de niveau d'huile"))
    capteur_niveau_huile_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    capteur_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    capteur_niveau_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # ACTIONNEURS
    # -------------------------
    injecteurs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Injecteurs"))
    injecteurs_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    injecteurs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    injecteurs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    vanne_egr = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Vanne EGR"))
    vanne_egr_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    vanne_egr_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    vanne_egr_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    boitier_papillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Boîtier papillon"))
    boitier_papillon_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    boitier_papillon_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    boitier_papillon_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    bobines_allumage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bobines d'allumage"))
    bobines_allumage_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    bobines_allumage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    bobines_allumage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    bougies_prechauffage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bougies / boîtier de préchauffage"))
    bougies_prechauffage_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    bougies_prechauffage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    bougies_prechauffage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    actionneur_turbo = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Électrovanne / actionneur de turbo"))
    actionneur_turbo_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    actionneur_turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    actionneur_turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    electrovanne_vvt = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Électrovanne de déphaseur d'arbre à cames (VVT)"))
    electrovanne_vvt_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    electrovanne_vvt_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    electrovanne_vvt_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    regulateur_pression_carburant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Régulateur de pression de carburant"))
    regulateur_pression_carburant_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    regulateur_pression_carburant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    regulateur_pression_carburant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    electrovanne_canister = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Électrovanne de purge canister"))
    electrovanne_canister_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    electrovanne_canister_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    electrovanne_canister_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    volets_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Actionneur de volets d'admission (swirl)"))
    volets_admission_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    volets_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    volets_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    thermostat_pilote = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Thermostat piloté"))
    thermostat_pilote_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    thermostat_pilote_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    thermostat_pilote_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    motoventilateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Motoventilateur"))
    motoventilateur_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    motoventilateur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    motoventilateur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # CALCULATEUR / FAISCEAU
    # -------------------------
    calculateur_moteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calculateur moteur (ECU)"))
    calculateur_moteur_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    calculateur_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    calculateur_moteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    faisceau_moteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Faisceau moteur"))
    faisceau_moteur_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    faisceau_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    faisceau_moteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    connecteurs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Connecteurs / cosses"))
    connecteurs_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"))
    connecteurs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    connecteurs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
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

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="electronique_moteur"
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
        related_name="electronique_moteur"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="electronique_moteur",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()

        if self.voiture_exemplaire and self.kilometrage_electronique is not None:
            if self.kilometrage_electronique < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_electronique": _(
                        "Le kilométrage de l'électronique moteur ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Électronique moteur")
        verbose_name_plural = _("Électronique moteur")

    def __str__(self):
        return f"Électronique moteur moteur - {self.voiture_exemplaire}"



    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):
        prix = getattr(
            self,
            f"{prefix}_prix",
            Decimal("0.00"),
        )

        quantite = getattr(
            self,
            f"{prefix}_quantite",
            0,
        )

        if not prix or not self.pays:
            return

        # -------------------------
        # TVA
        # -------------------------
        taux_tva = Decimal(
            str(TVAConfig.get_tva(self.pays))
        )

        tva_rate = taux_tva / Decimal("100")

        # -------------------------
        # PRIX HTVA
        # -------------------------
        prix_htva = Decimal(str(prix))

        prix_htva = prix_htva.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # TVA
        # -------------------------
        tva = (
                prix_htva * tva_rate
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # PRIX TTC
        # -------------------------
        prix_ttc = (
                prix_htva + tva
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # SAUVEGARDE DES CALCULS
        # -------------------------
        setattr(
            self,
            f"{prefix}_prix_vente_htva",
            prix_htva,
        )

        setattr(
            self,
            f"{prefix}_tva_vente",
            tva,
        )

        setattr(
            self,
            f"{prefix}_prix_ttc",
            prix_ttc,
        )

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # 🔥 synchro kilométrage AVANT save
        if hasattr(self, "sync_kilometrage"):
            self.sync_kilometrage()

        # Calculs
        for prefix, _label in PIECES_ELECTRONIQUE:
            self.calcul_piece(prefix)

        # =========================
        # TECHNICIEN
        # =========================
        if (
                not self.tech_technicien_id
                and hasattr(self, "_user")
        ):
            self.assign_technicien(
                self._user
            )

        # =========================
        # VEHICULE
        # =========================
        voiture = None

        if self.voiture_exemplaire_id:
            voiture = type(
                self.voiture_exemplaire
            ).objects.get(
                pk=self.voiture_exemplaire_id
            )

        # =========================
        # ANCIEN KM ADMISSION
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_electronique
                        or ancien_objet.kilometres_chassis
                        or 0
                )

        elif voiture:

            ancien_kilometrage = (
                    voiture.kilometres_chassis
                    or 0
            )

        # =========================
        # VARIATION
        # =========================
        if self.kilometrage_electronique is not None:

            self.kilometrage_variation = (
                    self.kilometrage_electronique
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_electronique
            )

        else:

            self.kilometrage_variation = 0

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if (
                self.main_oeuvre_id
                and self.voiture_exemplaire_id
        ):
            self.main_oeuvre.descriptif = (
                    _("Électronique moteur")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.save(
                update_fields=[
                    "descriptif"
                ]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if (
                self.maintenance_id
                and self.voiture_exemplaire_id
        ):

            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.ELECTRONIQUE_MOTEUR
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_electronique is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_electronique
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE ADMISSION
        # =========================
        super().save(
            *args,
            **kwargs
        )

        # =========================
        # UPDATE VEHICULE
        # =========================
        if (
                voiture is not None
                and self.kilometrage_electronique is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_electronique
            )

            kilometrage_vehicule = int(
                voiture.kilometres_chassis
                or 0
            )

            # Ne jamais faire redescendre
            # le kilométrage général du véhicule
            if nouveau_kilometrage >= kilometrage_vehicule:
                voiture.kilometres_chassis = (
                    nouveau_kilometrage
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis"
                    ]
                )

        # ========================================================
        # SAUVEGARDE
        # ========================================================

        super().save(*args, **kwargs)


    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        pieces = PIECES_ELECTRONIQUE

        for prefix, label in pieces:
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
            ]:
                continue

            # -------------------------
            # FABRICANT
            # -------------------------
            fabricant = getattr(
                self,
                f"{prefix}_fabricant",
                None,
            )

            fabricant_label = fabricant

            try:
                fabricant_field = self._meta.get_field(
                    f"{prefix}_fabricant"
                )

                if fabricant_field.choices:
                    fabricant_label = dict(
                        fabricant_field.choices
                    ).get(
                        fabricant,
                        fabricant,
                    )

            except FieldDoesNotExist:
                fabricant = None
                fabricant_label = None

            # -------------------------
            # PRIX
            # -------------------------
            prix = getattr(
                self,
                f"{prefix}_prix",
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # -------------------------
            # QUANTITÉ
            # -------------------------
            quantite = getattr(
                self,
                f"{prefix}_quantite",
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # Quantité 0 = ne pas ajouter au rapport
            if quantite <= 0:
                continue

            # -------------------------
            # TOTAL
            # -------------------------
            total = prix * quantite
            total_general += total

            # -------------------------
            # RAPPORT
            # -------------------------
            rapport.append(
                {
                    "champ": label,
                    "code": prefix,

                    "etat": etat,
                    "etat_label": dict(
                        EtatOKNotOK.choices
                    ).get(
                        etat,
                        etat,
                    ),

                    "fabricant": fabricant,
                    "fabricant_label": fabricant_label,

                    "prix": prix,
                    "quantite": quantite,
                    "total": total,
                }
            )

        return {
            "lignes": rapport,
            "total_general": total_general,
        }


    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display




    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_electronique is None:
            return

        km = Decimal(str(self.kilometrage_electronique))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km

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