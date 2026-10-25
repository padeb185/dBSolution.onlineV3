from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantCapteur, FabricantTurbo, FabricantEchappement, FabricantIntercooler, FabricantDurite, \
    FabricantInjecteur, FabricantPompeCarburant, FabricantCapteurEchappement, FabricantEmbrayage, RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
    RouesSerrageEtat, RefroidissementQualiteEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")


class EtatOptionnel(models.TextChoices):
    """Opération optionnelle (calibrage, diagnostic…)."""
    NON_PRESENT = "NON_PRESENT", _("Non concerné")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")


class TypeTurbo(models.TextChoices):
    NON_RENSEIGNE = "", _("—")
    FIXE_WASTEGATE = "FIXE_WASTEGATE", _("Géométrie fixe – wastegate interne")
    FIXE_WG_EXTERNE = "FIXE_WG_EXTERNE", _("Géométrie fixe – wastegate externe")
    GEOMETRIE_VARIABLE = "GEOMETRIE_VARIABLE", _("Géométrie variable (VNT / VGT)")
    TWIN_SCROLL = "TWIN_SCROLL", _("Twin-scroll")
    BI_TURBO = "BI_TURBO", _("Bi-turbo / séquentiel")
    ELECTRIQUE = "ELECTRIQUE", _("Turbo à assistance électrique")


class TypePalier(models.TextChoices):
    NON_RENSEIGNE = "", _("—")
    LISSE = "LISSE", _("Paliers lisses (journal bearing)")
    BILLES = "BILLES", _("Roulements à billes (ball bearing)")


class RefroidissementTurbo(models.TextChoices):
    NON_RENSEIGNE = "", _("—")
    HUILE = "HUILE", _("Huile")
    HUILE_EAU = "HUILE_EAU", _("Huile + eau")


class BrideTurbine(models.TextChoices):
    NON_RENSEIGNE = "", _("—")
    T25 = "T25", "T25"
    T28 = "T28", "T28"
    T3 = "T3", "T3"
    T4 = "T4", "T4"
    VBAND = "VBAND", "V-band"
    SPECIFIQUE = "SPECIFIQUE", _("Spécifique constructeur")

PIECES_MONTAGE_TURBO = [
    ("turbo_neuf", _("Turbo (nouveau, plus gros)")),
    ("collecteur_turbo", _("Collecteur d'échappement / adaptateur")),
    ("downpipe", _("Downpipe / descente de turbo")),
    ("wastegate_externe", _("Wastegate externe")),
    ("dump_valve", _("Dump valve / blow-off")),
    ("intercooler_upgrade", _("Intercooler")),
    ("durites_suralim", _("Durites de suralimentation (silicone)")),
    ("lignes_huile_turbo", _("Lignes d'huile (arrivée / retour)")),
    ("lignes_eau_turbo", _("Lignes de refroidissement (eau)")),
    ("joints_goujons", _("Joints, goujons et visserie")),
    ("injecteurs_upgrade", _("Injecteurs (plus gros débit)")),
    ("pompe_carburant_upgrade", _("Pompe à carburant renforcée")),
    ("capteur_map", _("Capteur de pression de suralimentation (MAP)")),
    ("sonde_egt", _("Sonde de température d'échappement (EGT)")),
    ("sonde_lambda_lb", _("Sonde lambda large bande")),
    ("embrayage_renforce", _("Embrayage renforcé")),
    ("huile_filtre_turbo", _("Huile moteur et filtre (après montage)")),
    ("reprogrammation", _("Reprogrammation / cartographie")),
    ("passage_banc", _("Passage au banc de puissance")),
]


class MontageTurbo(TechnicienMixin, models.Model):



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
        related_name="montage_turbo",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="montage_turbo",
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
    kilometrage_montage_turbo = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # Moteur monté sur le véhicule au moment de l'intervention (l'historique suit le moteur)
    moteur_lie = models.ForeignKey(
        "voiture_moteur.MoteurVoiture",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interventions_%(app_label)s",
        verbose_name=_("Moteur"),
    )

    # -------------------------
    # ANCIEN TURBO (déposé)
    # -------------------------
    anc_fabricant = models.CharField(max_length=25, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, blank=True, verbose_name=_("Fabricant"))
    anc_reference = models.CharField(max_length=100, blank=True, verbose_name=_("Référence / modèle"))
    anc_type = models.CharField(max_length=20, choices=TypeTurbo.choices, blank=True, default="", verbose_name=_("Type de turbo"))
    anc_comp_inducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Compresseur – inducer (mm)"))
    anc_comp_exducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Compresseur – exducer (mm)"))
    anc_turb_inducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Turbine – inducer (mm)"))
    anc_turb_exducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Turbine – exducer (mm)"))
    anc_ar_turbine = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("A/R carter turbine"))
    anc_debit_max_lbmin = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Débit d'air maxi (lb/min)"))
    anc_pression_max_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression de suralimentation maxi (bar)"))
    anc_puissance_max_ch = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance maxi supportée (ch)"))

    # -------------------------
    # NOUVEAU TURBO (monté) – dimensions, capacité et limites
    # -------------------------
    nv_fabricant = models.CharField(max_length=25, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, blank=True, verbose_name=_("Fabricant"))
    nv_reference = models.CharField(max_length=100, blank=True, verbose_name=_("Référence / modèle"))
    nv_type = models.CharField(max_length=20, choices=TypeTurbo.choices, blank=True, default="", verbose_name=_("Type de turbo"))
    nv_comp_inducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Compresseur – inducer (mm)"))
    nv_comp_exducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Compresseur – exducer (mm)"))
    nv_turb_inducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Turbine – inducer (mm)"))
    nv_turb_exducer_mm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Turbine – exducer (mm)"))
    nv_ar_turbine = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("A/R carter turbine"))
    nv_debit_max_lbmin = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name=_("Débit d'air maxi (lb/min)"))
    nv_pression_max_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Pression de suralimentation maxi (bar)"))
    nv_puissance_max_ch = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance maxi supportée (ch)"))
    nv_palier = models.CharField(max_length=10, choices=TypePalier.choices, blank=True, default="",
                                 verbose_name=_("Type de paliers"))
    nv_refroidissement = models.CharField(max_length=10, choices=RefroidissementTurbo.choices, blank=True, default="",
                                          verbose_name=_("Refroidissement"))
    nv_bride_turbine = models.CharField(max_length=12, choices=BrideTurbine.choices, blank=True, default="",
                                        verbose_name=_("Bride d'entrée turbine"))
    nv_regime_max_trmin = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Régime maxi de l'arbre (tr/min)"))
    nv_egt_max_c = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Température maxi des gaz admise (°C)"))

    # -------------------------
    # RÉGLAGES / LIMITES APPLIQUÉS
    # -------------------------
    reg_pression_cible_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                                 verbose_name=_("Pression de suralimentation cible (bar)"))
    reg_overboost_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                            verbose_name=_("Coupure overboost (bar)"))
    reg_egt_max_c = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Limite EGT réglée (°C)"))
    reg_lambda_pleine_charge = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                                   verbose_name=_("Lambda visé pleine charge"))
    reg_regime_max_moteur = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Rupteur moteur (tr/min)"))
    reg_preparateur = models.CharField(max_length=150, blank=True, verbose_name=_("Préparateur / cartographie"))

    # -------------------------
    # RÉSULTATS (banc / essais)
    # -------------------------
    res_puissance_avant_ch = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance avant (ch)"))
    res_puissance_apres_ch = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance après (ch)"))
    res_couple_avant_nm = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Couple avant (Nm)"))
    res_couple_apres_nm = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Couple après (Nm)"))
    res_pression_mesuree_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                                   verbose_name=_("Pression maxi mesurée (bar)"))
    res_egt_mesuree_c = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("EGT maxi mesurée (°C)"))
    res_lambda_mesure = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True,
                                            verbose_name=_("Lambda mesuré pleine charge"))


    # -------------------------
    # KIT DE MONTAGE
    # -------------------------
    # Turbo (nouveau, plus gros)
    turbo_neuf = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Turbo (nouveau, plus gros)"))
    turbo_neuf_fabricant = models.CharField(max_length=30, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    turbo_neuf_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    turbo_neuf_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Collecteur d'échappement / adaptateur
    collecteur_turbo = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Collecteur d'échappement / adaptateur"))
    collecteur_turbo_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    collecteur_turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    collecteur_turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Downpipe / descente de turbo
    downpipe = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Downpipe / descente de turbo"))
    downpipe_fabricant = models.CharField(max_length=30, choices=FabricantEchappement.choices, default=FabricantEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    downpipe_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    downpipe_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Wastegate externe
    wastegate_externe = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Wastegate externe"))
    wastegate_externe_fabricant = models.CharField(max_length=30, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    wastegate_externe_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    wastegate_externe_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Dump valve / blow-off
    dump_valve = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Dump valve / blow-off"))
    dump_valve_fabricant = models.CharField(max_length=30, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    dump_valve_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    dump_valve_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Intercooler
    intercooler_upgrade = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Intercooler"))
    intercooler_upgrade_fabricant = models.CharField(max_length=30, choices=FabricantIntercooler.choices, default=FabricantIntercooler.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    intercooler_upgrade_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    intercooler_upgrade_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Durites de suralimentation (silicone)
    durites_suralim = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Durites de suralimentation (silicone)"))
    durites_suralim_fabricant = models.CharField(max_length=30, choices=FabricantDurite.choices, default=FabricantDurite.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    durites_suralim_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    durites_suralim_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Lignes d'huile (arrivée / retour)
    lignes_huile_turbo = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Lignes d'huile (arrivée / retour)"))
    lignes_huile_turbo_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    lignes_huile_turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    lignes_huile_turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Lignes de refroidissement (eau)
    lignes_eau_turbo = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Lignes de refroidissement (eau)"))
    lignes_eau_turbo_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    lignes_eau_turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    lignes_eau_turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Joints, goujons et visserie
    joints_goujons = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Joints, goujons et visserie"))
    joints_goujons_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    joints_goujons_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    joints_goujons_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Injecteurs (plus gros débit)
    injecteurs_upgrade = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Injecteurs (plus gros débit)"))
    injecteurs_upgrade_fabricant = models.CharField(max_length=30, choices=FabricantInjecteur.choices, default=FabricantInjecteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    injecteurs_upgrade_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    injecteurs_upgrade_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Pompe à carburant renforcée
    pompe_carburant_upgrade = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Pompe à carburant renforcée"))
    pompe_carburant_upgrade_fabricant = models.CharField(max_length=30, choices=FabricantPompeCarburant.choices, default=FabricantPompeCarburant.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    pompe_carburant_upgrade_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pompe_carburant_upgrade_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Capteur de pression de suralimentation (MAP)
    capteur_map = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Capteur de pression de suralimentation (MAP)"))
    capteur_map_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteur_map_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_map_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Sonde de température d'échappement (EGT)
    sonde_egt = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Sonde de température d'échappement (EGT)"))
    sonde_egt_fabricant = models.CharField(max_length=30, choices=FabricantCapteurEchappement.choices, default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    sonde_egt_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_egt_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Sonde lambda large bande
    sonde_lambda_lb = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Sonde lambda large bande"))
    sonde_lambda_lb_fabricant = models.CharField(max_length=30, choices=FabricantCapteurEchappement.choices, default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    sonde_lambda_lb_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_lambda_lb_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Embrayage renforcé
    embrayage_renforce = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Embrayage renforcé"))
    embrayage_renforce_fabricant = models.CharField(max_length=30, choices=FabricantEmbrayage.choices, default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    embrayage_renforce_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    embrayage_renforce_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Huile moteur et filtre (après montage)
    huile_filtre_turbo = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Huile moteur et filtre (après montage)"))
    huile_filtre_turbo_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    huile_filtre_turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    huile_filtre_turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Reprogrammation / cartographie
    reprogrammation = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Reprogrammation / cartographie"))
    reprogrammation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    reprogrammation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Passage au banc de puissance
    passage_banc = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Passage au banc de puissance"))
    passage_banc_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    passage_banc_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



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
        related_name="montage_turbo"
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
        related_name="montage_turbo"
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
        related_name="montage_turbo",
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

        if self.voiture_exemplaire and self.kilometrage_montage_turbo is not None:
            if self.kilometrage_montage_turbo < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_montage_turbo": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Montage turbo plus gros")
        verbose_name_plural = _("Montage turbo plus gros")

    def __str__(self):
        return f"Montage turbo plus gros - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_MONTAGE_TURBO:
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
        # ANCIEN KM MONTAGE D'UN TURBO PLUS GROS
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_montage_turbo
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
        if self.kilometrage_montage_turbo is not None:

            self.kilometrage_variation = (
                    self.kilometrage_montage_turbo
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km montage_turbo
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_montage_turbo
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
                    _("Montage turbo plus gros")
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
                Maintenance.TypeMaintenance.MONTAGE_TURBO
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_montage_turbo is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_montage_turbo
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE MONTAGE D'UN TURBO PLUS GROS
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
                and self.kilometrage_montage_turbo is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_montage_turbo
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

        pieces = PIECES_MONTAGE_TURBO

        for prefix, label in pieces:
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
                EtatOKNotOK.AJOUTER,
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
                        self._meta.get_field(prefix).choices
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


    # ======================================================
    # FICHES TURBO, COMPARAISON ET LIMITES
    # ======================================================
    CHAMPS_FICHE = ("fabricant", "reference", "type", "comp_inducer_mm", "comp_exducer_mm", "turb_inducer_mm",
                    "turb_exducer_mm", "ar_turbine", "debit_max_lbmin", "pression_max_bar", "puissance_max_ch")

    @staticmethod
    def _trim(inducer, exducer):
        if inducer and exducer:
            return (Decimal(inducer) ** 2 / Decimal(exducer) ** 2 * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        return None

    @staticmethod
    def _ecart_pct(ancien, nouveau):
        if ancien and nouveau:
            return ((Decimal(nouveau) - Decimal(ancien)) / Decimal(ancien) * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return None

    @property
    def comparatif(self):
        """Lignes ancien / nouveau turbo avec l'écart en %."""
        lignes = []
        for nom in self.CHAMPS_FICHE:
            champ = self._meta.get_field(f"nv_{nom}")
            ancien = getattr(self, f"anc_{nom}")
            nouveau = getattr(self, f"nv_{nom}")
            if nom in ("fabricant", "type"):
                ancien = getattr(self, f"get_anc_{nom}_display")() if ancien and ancien != "CHOISIR" else ""
                nouveau = getattr(self, f"get_nv_{nom}_display")() if nouveau and nouveau != "CHOISIR" else ""
                ecart = None
            elif nom == "reference":
                ecart = None
            else:
                ecart = self._ecart_pct(ancien, nouveau)
            if ancien in (None, "") and nouveau in (None, ""):
                continue
            lignes.append({"label": champ.verbose_name, "ancien": ancien, "nouveau": nouveau, "ecart": ecart})
        trim_anc = self._trim(self.anc_comp_inducer_mm, self.anc_comp_exducer_mm)
        trim_nv = self._trim(self.nv_comp_inducer_mm, self.nv_comp_exducer_mm)
        if trim_anc or trim_nv:
            lignes.append({"label": _("Trim compresseur"), "ancien": trim_anc, "nouveau": trim_nv,
                           "ecart": self._ecart_pct(trim_anc, trim_nv)})
        return lignes

    @property
    def gain_puissance(self):
        if self.res_puissance_avant_ch and self.res_puissance_apres_ch:
            return self.res_puissance_apres_ch - self.res_puissance_avant_ch
        return None

    @property
    def gain_puissance_pct(self):
        return self._ecart_pct(self.res_puissance_avant_ch, self.res_puissance_apres_ch)

    @property
    def gain_couple(self):
        if self.res_couple_avant_nm and self.res_couple_apres_nm:
            return self.res_couple_apres_nm - self.res_couple_avant_nm
        return None

    @property
    def utilisation_capacite_pct(self):
        """Puissance obtenue (ou visée) par rapport à la puissance maxi supportée par le nouveau turbo."""
        if self.nv_puissance_max_ch and self.res_puissance_apres_ch:
            return (Decimal(self.res_puissance_apres_ch) / Decimal(self.nv_puissance_max_ch) * 100).quantize(
                Decimal("1"), rounding=ROUND_HALF_UP)
        return None

    @property
    def alertes_limites(self):
        """Dépassements des limites du turbo / des réglages."""
        a = []
        nv_p = self.nv_pression_max_bar
        if nv_p and self.reg_pression_cible_bar and self.reg_pression_cible_bar > nv_p:
            a.append(_("Pression cible (%(c)s bar) supérieure à la pression maxi du turbo (%(m)s bar).") % {"c": self.reg_pression_cible_bar, "m": nv_p})
        if nv_p and self.reg_overboost_bar and self.reg_overboost_bar > nv_p:
            a.append(_("Coupure overboost (%(c)s bar) au-delà de la pression maxi du turbo (%(m)s bar).") % {"c": self.reg_overboost_bar, "m": nv_p})
        if self.reg_pression_cible_bar and self.reg_overboost_bar and self.reg_overboost_bar <= self.reg_pression_cible_bar:
            a.append(_("La coupure overboost doit être supérieure à la pression cible."))
        if self.res_pression_mesuree_bar:
            if self.reg_overboost_bar and self.res_pression_mesuree_bar >= self.reg_overboost_bar:
                a.append(_("Pression mesurée (%(p)s bar) ≥ coupure overboost (%(o)s bar).") % {"p": self.res_pression_mesuree_bar, "o": self.reg_overboost_bar})
            elif nv_p and self.res_pression_mesuree_bar > nv_p:
                a.append(_("Pression mesurée (%(p)s bar) au-delà de la pression maxi du turbo (%(m)s bar).") % {"p": self.res_pression_mesuree_bar, "m": nv_p})
        if self.res_egt_mesuree_c:
            limite = min(x for x in (self.reg_egt_max_c, self.nv_egt_max_c) if x) if (self.reg_egt_max_c or self.nv_egt_max_c) else None
            if limite and self.res_egt_mesuree_c > limite:
                a.append(_("EGT mesurée (%(t)s °C) au-delà de la limite (%(l)s °C).") % {"t": self.res_egt_mesuree_c, "l": limite})
        u = self.utilisation_capacite_pct
        if u is not None:
            if u > 100:
                a.append(_("Puissance obtenue au-delà de la capacité du turbo (%(u)s %%).") % {"u": u})
            elif u > 90:
                a.append(_("Turbo utilisé à %(u)s %% de sa capacité : marge de sécurité faible.") % {"u": u})
        if self.reg_lambda_pleine_charge and self.reg_lambda_pleine_charge > Decimal("0.90"):
            a.append(_("Lambda pleine charge pauvre (> 0,90) : risque de surchauffe / détonation."))
        if self.res_lambda_mesure and self.res_lambda_mesure > Decimal("0.90"):
            a.append(_("Lambda mesuré pauvre (> 0,90) en pleine charge : enrichir la cartographie."))
        gp = self.gain_puissance_pct
        if gp is not None and gp > 30:
            manquants = [str(l) for p, l in PIECES_MONTAGE_TURBO
                         if p in ("injecteurs_upgrade", "pompe_carburant_upgrade", "embrayage_renforce")
                         and getattr(self, p) == EtatOptionnel.NON_PRESENT]
            if manquants:
                a.append(_("Gain > 30 %% : vérifier %(p)s.") % {"p": ", ".join(manquants)})
        return a

    @property
    def limites_respectees(self):
        return not self.alertes_limites




    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_montage_turbo is None:
            return

        km = Decimal(str(self.kilometrage_montage_turbo))

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
