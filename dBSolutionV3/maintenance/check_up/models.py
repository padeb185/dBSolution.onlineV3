from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator, MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantLubrifiant, RefroidissementFabricant, \
    FabricantFrein, TypeHuileDirection, FabricantPiece, FabricantSuspension, AmpouleAutomobile, FabricantPneus, \
    FabricantBatterie, FabricantAmpoule, TVAConfig, HuileEtat, HuileBoiteEtat, HuilePontEtat, RefroidissementQualiteEtat
from django.conf import settings
from utils.mixin import TechnicienMixin


# ---------------------------
# TextChoices
# ---------------------------


class EtatAjouter(models.TextChoices):
    SANS = "SANS", _("Sans")
    AJOUTER = "AJOUTER", _("Ajouté")


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class PhareEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class PhareReglageEtat(models.TextChoices):
    OK = "OK", _("OK")
    FAIT = "FAIT", _("Fait")
    A_FAIRE = "A_FAIRE", _("A faire")

class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("OK")
    AJOUTER = "AJOUTER", _("Ajouter")


class RefroidissementEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    AJOUTER = "AJOUTER", _("Ajouter")
    REMPLACE = "REMPLACE", _("Remplacé")


class PneuEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class QualiteLiquideFrein(models.TextChoices):
    DOT3 = "DOT3", _("DOT 3")
    DOT4 = "DOT4", _("DOT 4")
    DOT5 = "DOT5", _("DOT 5")
    DOT51 = "DOT51", _("DOT 5.1")

# ---------------------------
# Modèle fusionné
# ---------------------------
class Checkup(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="checkup",
        verbose_name=_("Checkup"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_general_checkup_exemplaire_km",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_checkup = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du Checkup"),

    )
    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # --- Essuie-glaces & Pare-brise ---
    essuie_glace = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                    verbose_name=_("Etat des balais avant"))
    essuie_glace_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,
                                                     default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"))
    essuie_glace_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    essuie_glace_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    balais_essuie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Etat des balais arrières"))
    balais_essuie_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,
                                              default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"))
    balais_essuie_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    balais_essuie_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                             verbose_name=_("Prix d'achat HTVA"))



    pare_brise_av_coups = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                           verbose_name=_("Pare-brise sans coups"))
    pare_brise_av_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                               verbose_name=_("Pare-brise à remplacer"))
    pare_brise_av_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    pare_brise_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                             verbose_name=_("Prix d'achat HTVA"))

    # --- Moteur & transmission ---
    moteur_fuite =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite moteur"))
    moteur_bruit =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruit moteur"))
    moteur_perte =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Perte de puissance"))
    moteur_casse =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Moteur à remplacer"))
    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON, verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))
    moteur_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    boite_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite boîte de vitesse"))
    boite_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits boîte de vitesse"))
    boite_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Problème d'embrayage"))
    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    boite_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité d'huile"))
    boite_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))
    # --- Pont ----

    pont_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite pont arrière"))
    pont_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits pont arrière"))
    pont_jeu = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu pont arrière"))
    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    pont_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ80,verbose_name=_("Qualité d'huile"))
    pont_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    pont_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))

    # --- Refroidissement ---

    refroidissement_radiateur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Radiateur"))
    refroidissement_radiateur_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR,verbose_name=_("Fabricant"))
    refroidissement_radiateur_quantite = models.PositiveIntegerField(default=0,verbose_name=_("Quantité"))
    refroidissement_radiateur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    refroidissement_liquide = models.CharField(max_length=25, choices=RefroidissementEtat.choices, default=RefroidissementEtat.OK, verbose_name=_("Liquide de refroidissement "))
    refroidissement_liquide_fabricant = models.CharField(max_length=25, choices=RefroidissementFabricant.choices,default=RefroidissementFabricant.CHOISIR,verbose_name=_("Fabricant"))
    refroidissement_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    refroidissement_liquide_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13, verbose_name=_("Qualité de liquide"))
    refroidissement_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))

    # --- Freins ---

    freins_plaquettes_av_usure = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avant (%)"))
    freins_plaquettes_av_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes avant"))
    freins_plaquettes_av_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant"))
    freins_plaquettes_av_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    freins_plaquettes_av_prix = models.DecimalField(max_digits=10,
                                               decimal_places=2,
                                               default=0,
                                               verbose_name=_("Prix d'achat HTVA")
                                               )

    freins_disques_av_epaisseur = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    freins_disques_av_fentes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques avant"))
    freins_disques_av_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques avant"))
    freins_disques_av_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant")
    )
    freins_disques_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    freins_disques_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    freins_plaquettes_ar_usure = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrière (%)"))
    freins_plaquettes_ar_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes arrière à remplacer"))
    freins_plaquettes_ar_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant"))
    freins_plaquettes_ar_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    freins_plaquettes_ar_prix = models.DecimalField(max_digits=10,
                                                    decimal_places=2,
                                                    default=0,
                                                    verbose_name=_("Prix d'achat HTVA")
                                                    )

    freins_disques_ar_epaisseur = models.FloatField(default=0, verbose_name=_("Épaisseur des disques arrière (mm)"))
    freins_disques_ar_fentes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques arrière"))
    freins_disques_ar_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques arrière"))
    freins_disques_ar_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFrein.choices,
        default=FabricantFrein.CHOISIR,
        verbose_name=_("Fabricant")
    )
    freins_disques_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité")
    )
    freins_disques_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    freins_liquide_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fuite"))


    # --- Liquide ---
    freins_liquide_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État liquide de frein"))
    freins_liquide_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CHOISIR,
        verbose_name=_("Fabricant")
    )
    freins_liquide_specif = models.CharField(max_length=100, choices=QualiteLiquideFrein.choices, default=QualiteLiquideFrein.DOT4, blank=True, verbose_name=_("Spécification liquide de frein"))
    freins_liquide_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
        verbose_name=_("Quantité ajoutée en litres"),
        validators=[StepValueValidator(0.1)],
    )

    freins_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )


    direction_liquide_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite direction assistée / crémaillère"), null=True, blank=True)
    direction_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    direction_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    direction_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    direction_liquide_qualite = models.CharField(max_length=25, choices=TypeHuileDirection.choices,default=TypeHuileDirection.CHOISIR,verbose_name=_("Qualité"))
    direction_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    # --- Bruits ---
    bruit_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue avant droit"), blank=True, null=True)
    bruit_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État roulement de roue avant gauche"),  blank=True, null=True)
    bruit_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière droit"), blank=True, null=True)
    bruit_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière gauche"),  blank=True, null=True)


    # --- Batterie ---
    batterie_etat = models.CharField(max_length=25, choices=BatterieEtat.choices, default=BatterieEtat.OK, verbose_name=_("État batterie"))
    batterie_fabricant = models.CharField(
        max_length=25,
        choices=FabricantBatterie.choices,
        default=FabricantBatterie.CHOISIR,
        verbose_name=_("Fabricant de la batterie"),
    )
    batterie_tension = models.PositiveIntegerField(default= 12, verbose_name=_("Tension de batterie"))
    batterie_ampere_heure = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        verbose_name=_("Ampère heure"),
    )
    batterie_ampere_max = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1500)],
        verbose_name=_("Courant maximum de démarrage"),
    )

    batterie_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name= _("Quantité")
    )
    batterie_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))





    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction avant droite"),
    )
    jeu_rotule_direction_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_direction_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_direction_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_direction_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction avant gauche"),
    )
    jeu_rotule_direction_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_direction_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_direction_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_direction_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction arrière droite"),
    )
    jeu_rotule_direction_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_direction_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_direction_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_direction_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de direction arrière gauche"),
    )
    jeu_rotule_direction_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_direction_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_direction_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_inferieure_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure avant droite"),
    )
    jeu_rotule_suspension_inferieure_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_inferieure_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_inferieure_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_inferieure_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure avant gauche"),
    )
    jeu_rotule_suspension_inferieure_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_inferieure_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_inferieure_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_inferieure_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure arrière droite"),
    )
    jeu_rotule_suspension_inferieure_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_inferieure_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_inferieure_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_inferieure_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension inférieure arrière gauche"),
    )
    jeu_rotule_suspension_inferieure_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_inferieure_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_inferieure_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_superieure_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure avant droite"),
    )
    jeu_rotule_suspension_superieure_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_superieure_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_superieure_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_superieure_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure avant gauche"),
    )
    jeu_rotule_suspension_superieure_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_superieure_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_superieure_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_superieure_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure arrière droite"),
    )
    jeu_rotule_suspension_superieure_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_superieure_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_superieure_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_rotule_suspension_superieure_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu rotule de suspension supérieure arrière gauche"),
    )
    jeu_rotule_suspension_superieure_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_rotule_suspension_superieure_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_rotule_suspension_superieure_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_Biellette_barre_stabilisatrice_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice avant droite"),
    )
    jeu_Biellette_barre_stabilisatrice_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_Biellette_barre_stabilisatrice_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_Biellette_barre_stabilisatrice_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_Biellette_barre_stabilisatrice_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice avant gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_Biellette_barre_stabilisatrice_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_Biellette_barre_stabilisatrice_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_Biellette_barre_stabilisatrice_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice arrière droite"),
    )
    jeu_Biellette_barre_stabilisatrice_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_Biellette_barre_stabilisatrice_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_Biellette_barre_stabilisatrice_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_Biellette_barre_stabilisatrice_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de barre stabilisatrice arrière gauche"),
    )
    jeu_Biellette_barre_stabilisatrice_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_Biellette_barre_stabilisatrice_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_Biellette_barre_stabilisatrice_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_barre_stabilisatrice_av = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu barre stabilisatrice avant"),
    )
    jeu_barre_stabilisatrice_av_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_barre_stabilisatrice_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_barre_stabilisatrice_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_barre_stabilisatrice_ar = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu barre stabilisatrice arrière"),
    )
    jeu_barre_stabilisatrice_ar_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_barre_stabilisatrice_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_barre_stabilisatrice_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_biellette_direction_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de direction droite"),
    )
    jeu_biellette_direction_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_biellette_direction_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_biellette_direction_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_biellette_direction_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu biellette de direction gauche"),
    )
    jeu_biellette_direction_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_biellette_direction_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_biellette_direction_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_cardan_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu du cardan avant droit"),
    )
    jeu_cardan_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_cardan_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_cardan_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_cardan_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu du cardan avant gauche"),
    )
    jeu_cardan_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_cardan_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_cardan_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_cardan_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu du cardan arrière droit"),
    )
    jeu_cardan_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_cardan_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_cardan_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_cardan_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu du cardan arrière gauche"),
    )
    jeu_cardan_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_cardan_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_cardan_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_arbre = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu dans l'arbre de transmission"),
    )
    jeu_arbre_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_arbre_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_arbre_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_amortisseur_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur avant droit"),
    )
    jeu_amortisseur_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantSuspension.choices,
        default=FabricantSuspension.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_amortisseur_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_amortisseur_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_amortisseur_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur avant gauche"),
    )
    jeu_amortisseur_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantSuspension.choices,
        default=FabricantSuspension.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_amortisseur_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_amortisseur_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_amortisseur_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur arrière droit"),
    )
    jeu_amortisseur_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantSuspension.choices,
        default=FabricantSuspension.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_amortisseur_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_amortisseur_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_amortisseur_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu amortisseur arrière gauche"),
    )
    jeu_amortisseur_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantSuspension.choices,
        default=FabricantSuspension.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_amortisseur_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_amortisseur_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_roulement_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement avant droit"),
    )
    jeu_roulement_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_roulement_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_roulement_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_roulement_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement avant gauche"),
    )
    jeu_roulement_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_roulement_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_roulement_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_roulement_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement arrière droit"),
    )
    jeu_roulement_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_roulement_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_roulement_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_roulement_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu roulement arrière gauche"),
    )
    jeu_roulement_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_roulement_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_roulement_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_triangle_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle avant droit"),
    )
    jeu_triangle_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_triangle_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_triangle_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_triangle_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle avant gauche"),
    )
    jeu_triangle_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_triangle_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_triangle_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_triangle_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle arrière droit"),
    )
    jeu_triangle_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_triangle_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_triangle_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_triangle_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu triangle arrière gauche"),
    )
    jeu_triangle_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_triangle_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_triangle_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_multi_bras_avd = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras avant droit"),
    )
    jeu_multi_bras_avd_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_multi_bras_avd_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_multi_bras_avd_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_multi_bras_avg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras avant gauche"),
    )
    jeu_multi_bras_avg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_multi_bras_avg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_multi_bras_avg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_multi_bras_ard = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras arrière droit"),
    )
    jeu_multi_bras_ard_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_multi_bras_ard_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_multi_bras_ard_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    jeu_multi_bras_arg = models.CharField(
        max_length=25,
        choices=EtatOKNotOK.choices,
        default=EtatOKNotOK.OK,
        verbose_name=_("Jeu suspension multi-bras arrière gauche"),
    )
    jeu_multi_bras_arg_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_multi_bras_arg_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    jeu_multi_bras_arg_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    # --- Pneus et Pression

    pneu_bande_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,
                                      verbose_name=_("Pneu avant droit"))
    pneu_bande_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,
                                      verbose_name=_("Pneu avant gauche"))
    pneu_bande_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,
                                      verbose_name=_("Pneu arrière droit"))
    pneu_bande_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,
                                      verbose_name=_("Pneu arrière gauche"))


    pneu_epaisseur_avd = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant droit (mm)"))
    pneu_epaisseur_avg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant gauche (mm)"))
    pneu_epaisseur_ard = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière droit (mm)"))
    pneu_epaisseur_arg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière gauche (mm)"))

    pneu_sidewall_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("flanc du pneu avant droit"))
    pneu_sidewall_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu avant gauche"))
    pneu_sidewall_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu arrière droit"))
    pneu_sidewall_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu arrière gauche"))

    pneu_pression_bar_avd = models.FloatField(
        default=2.4,
        validators=[StepValueValidator(0.1)],
        verbose_name=_("Pression du pneu avant droit en bar"),
    )

    pneu_pression_bar_avg = models.FloatField(
        default=2.4,
        validators=[StepValueValidator(0.1)],
        verbose_name=_("Pression du pneu avant gauche en bar"),
    )

    pneu_pression_bar_ard = models.FloatField(
        default=2.4,
        validators=[StepValueValidator(0.1)],
        verbose_name=_("Pression du pneu arrière droit en bar"),
    )

    pneu_pression_bar_arg = models.FloatField(
        default=2.4,
        validators=[StepValueValidator(0.1)],
        verbose_name=_("Pression du pneu arrière gauche en bar"),
    )

    pneu_train_av = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Pneus avant à remplacer"))
    pneu_train_av_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPneus.choices,
        default=FabricantPneus.CHOISIR,
        verbose_name=_("Manufacturier")
    )

    pneu_train_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pneu_train_av_quantite = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Quantité"))

    pneu_train_ar = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Pneus arrière à remplacer"))
    pneu_train_ar_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPneus.choices,
        default=FabricantPneus.CHOISIR,
        verbose_name=_("Manufacturier")
    )
    pneu_train_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pneu_train_ar_quantite = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Quantité"))



    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE, verbose_name=_("Serrage des roues"))

    # --- Réglage phares ---
    phares_reglages = models.CharField(max_length=25, choices=PhareReglageEtat.choices, default=PhareReglageEtat.OK,verbose_name=_("Réglage des phares"))

    phares_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de route"),
    )
    phares_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    phares_gros_phares = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Grands phares"),
    )
    phares_gros_phares_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_gros_phares_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_gros_phares_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_gros_phares_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )




    phares_clignotants = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Clignotants"),
    )
    phares_clignotants_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_clignotants_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_clignotants_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_clignotants_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    phares_recul = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de recul"),
    )
    phares_recul_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_recul_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_recul_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_recul_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    phares_anti_brouillard_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard avant"),
    )
    phares_anti_brouillard_avant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_anti_brouillard_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_anti_brouillard_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    phares_anti_brouillard_arriere = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard arrière"),
    )
    phares_anti_brouillard_arriere_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_anti_brouillard_arriere_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_anti_brouillard_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    phares_feux_stops = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux stop"),
    )
    phares_feux_stops_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_stops_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_stops_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_feux_stops_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    phares_troisieme_feux_stop = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Troisième feu stop"),
    )
    phares_troisieme_feux_stop_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_troisieme_feux_stop_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_troisieme_feux_stop_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_troisieme_feux_stop_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    phares_feux_position_av = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position avant"),
    )
    phares_feux_position_av_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_position_av_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    phares_feux_position_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    phares_feux_position_ar = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position arrière"),
    )
    phares_feux_position_ar_fabricant = models.CharField(
        max_length=25,
        choices=FabricantAmpoule.choices,
        default=FabricantAmpoule.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    phares_feux_position_ar_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_feux_position_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )




    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Traces de gomme"))
    nettoyage_exterieur_carrosserie = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carrosserie"))
    nettoyage_exterieur_jantes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Jantes"))
    nettoyage_exterieur_sechage = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Séchage"))
    nettoyage_exterieur_produits = models.CharField(
        max_length=25,
        choices=EtatAjouter.choices,
        default=EtatAjouter.SANS,
        verbose_name=_("Produits")
    )

    nettoyage_exterieur_produits_prix = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Prix d'achat HTVA"))

    nettoyage_exterieur_produits_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"))

    # --- Nettoyage intérieur ---
    nettoyage_interieur_vitres = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Vitres"))
    nettoyage_interieur_pare_brise = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Pare-brise"))
    nettoyage_interieur_aspirateur = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Aspirateur"))
    nettoyage_interieur_portes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Intérieurs de porte"))
    nettoyage_interieur_sieges = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Sièges"))
    nettoyage_interieur_carpettes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carpettes"))
    nettoyage_interieur_tableau_de_bord = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Tableau de bord"))
    nettoyage_interieur_plastiques = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Plastiques"))
    nettoyage_interieur_produits = models.CharField(
        max_length=25,
        choices=EtatAjouter.choices,
        default=EtatAjouter.SANS,
        verbose_name=_("Produits")
    )

    nettoyage_interieur_produits_prix = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name=_("Prix d'achat HTVA"))

    nettoyage_interieur_produits_quantite = models.IntegerField(
        default=0,
        verbose_name=_("Quantité"))




    remarques = models.TextField(
        verbose_name=_("Remarques"), blank=True, null=True)

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

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checkup",
        verbose_name=_("Main d'oeuvre")
    )

    tech_last_maintained_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="checkup",
        verbose_name=_("Dernière maintenance effectuée par")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_techs"
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
        related_name="controle_tech_societe"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
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

    class Meta:
        verbose_name = _("Contrôle général")
        verbose_name_plural = _("Contrôles généraux")

    def __str__(self):
        # Si l'objet a une maintenance liée, on affiche son id
        if self.maintenance:
            return f"Check-up {self.maintenance.id}"
        # Sinon on affiche un texte par défaut
        return "Check-up (sans maintenance)"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_checkup is not None:
            if self.kilometrage_checkup < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
                        f"Le kilométrage du check-up ({self.kilometrage_checkup}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })


            if self.serrage_roues == RouesSerrageEtat.A_FAIRE:
                raise ValidationError({
                    "serrage_roues": _(
                        "Vous devez indiquer si le serrage des roues a été effectué avant d'enregistrer ce contrôle."
                    )
                })

    def save(self, *args, **kwargs):

        # =========================
        # 1. SYNC KM VOITURE
        # =========================
        if self.voiture_exemplaire and self.kilometrage_checkup:

            if self.kilometrage_checkup < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError("Le kilométrage ne peut pas diminuer.")

            if self.kilometrage_checkup > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_checkup
                self.voiture_exemplaire.kilometres_dernier_entretien = self.kilometrage_checkup
                self.voiture_exemplaire.date_derniere_intervention = timezone.now().date()

                self.voiture_exemplaire.update_kilometres()
                self.voiture_exemplaire.save()

        # =========================
        # 2. COPIE SNAPSHOT
        # =========================
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if (
                self.kilometrage_checkup is not None
                and self.kilometres_chassis is not None
        ):
            self.kilometrage_variation = (
                    self.kilometrage_checkup - self.kilometres_chassis
            )

        # =========================
        # 3. TECHNICIEN
        # =========================
        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        # =========================
        # 4. MAIN D'OEUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Checkup complet") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])


        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
            rapport = []
            total_general = Decimal("0.00")

            # États autorisant l'ajout dans le rapport
            etats_a_facturer = {
                EtatOKNotOK.A_REMPLACER,
                EtatOKNotOK.REMPLACE,

                BatterieEtat.A_REMPLACER,
                BatterieEtat.REMPLACE,

                PhareEtat.A_REMPLACER,
                PhareEtat.REMPLACE,

                RefroidissementEtat.A_REMPLACER,
                RefroidissementEtat.REMPLACE,

                PneuEtat.A_REMPLACER,
                PneuEtat.REMPLACE,

                NiveauxEtat.AJOUTER,

                EtatAjouter.AJOUTER,
            }

            # Correspondances particulières entre le champ d'état
            # et la base des champs prix/quantité/fabricant/qualité/type.
            correspondances = {
                # Huiles et liquides
                "moteur_niveau_huile_etat": "moteur_niveau_huile",
                "boite_niveau_huile_etat": "boite_niveau_huile",
                "pont_niveau_huile_etat": "pont_niveau_huile",
                "direction_liquide_etat": "direction_liquide",

                # Liquide de frein
                "frein_liquide_frein_etat": "frein_liquide",

                # Refroidissement
                "refroidissement_radiateur": "refroidissement",

                # Freins
                "freins_plaquettes_av_remplacer": "freins_plaquettes_av",
                "freins_disques_av_remplacer": "freins_disques_av",
                "freins_plaquettes_ar_remplacer": "freins_plaquettes_ar",
                "freins_disques_ar_remplacer": "freins_disques_ar",

                # Pneus
                "pneu_train_av": "pneu_train_av",
                "pneu_train_ar": "pneu_train_ar",

                # Éclairage
                "phares_avant": "phares_avant",
                "phares_gros_phares": "phares_gros_phares",
                "phares_clignotants": "phares_clignotants",
                "phares_recul": "phares_recul",
                "phares_anti_brouillard_avant": "phares_anti_brouillard_avant",
                "phares_anti_brouillard_arriere": "phares_anti_brouillard_arriere",
                "phares_feux_stops": "phares_feux_stops",
                "phares_troisieme_feux_stop": "phares_troisieme_feux_stop",
                "phares_feux_position_av": "phares_feux_position_av",
                "phares_feux_position_ar": "phares_feux_position_ar",

                # Produits de nettoyage
                "nettoyage_exterieur_produits": "nettoyage_exterieur_produits",
                "nettoyage_interieur_produits": "nettoyage_interieur_produits",
            }

            for field in self._meta.fields:
                if not isinstance(field, models.CharField):
                    continue

                if not field.choices:
                    continue

                field_name = field.name
                etat = getattr(self, field_name, None)

                if etat not in etats_a_facturer:
                    continue

                # Déterminer la base utilisée pour les champs associés
                champ_base = correspondances.get(field_name)

                if not champ_base:
                    if field_name.endswith("_etat"):
                        champ_base = field_name.removesuffix("_etat")

                    elif field_name.endswith("_remplacer"):
                        champ_base = field_name.removesuffix("_remplacer")

                    else:
                        champ_base = field_name

                champ_prix = f"{champ_base}_prix"
                champ_quantite = f"{champ_base}_quantite"
                champ_fabricant = f"{champ_base}_fabricant"
                champ_qualite = f"{champ_base}_qualite"
                champ_type = f"{champ_base}_type"

                # Ne pas ajouter un contrôle sans prix ou quantité associés
                if not hasattr(self, champ_prix):
                    continue

                if not hasattr(self, champ_quantite):
                    continue

                prix = getattr(
                    self,
                    champ_prix,
                    Decimal("0.00"),
                )

                quantite = getattr(
                    self,
                    champ_quantite,
                    Decimal("0.00"),
                )

                if prix is None:
                    prix = Decimal("0.00")

                if quantite is None:
                    quantite = Decimal("0.00")

                prix = Decimal(str(prix))
                quantite = Decimal(str(quantite))

                # N'afficher que les lignes réellement facturables
                if prix <= Decimal("0.00"):
                    continue

                if quantite <= Decimal("0.00"):
                    continue

                total = (
                        prix * quantite
                ).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )

                total_general += total

                # Libellé de l'état
                get_etat_display = getattr(
                    self,
                    f"get_{field_name}_display",
                    None,
                )

                if callable(get_etat_display):
                    etat_label = get_etat_display()
                else:
                    etat_label = dict(field.choices).get(etat, etat)

                # Fabricant
                fabricant = None
                fabricant_label = None

                if hasattr(self, champ_fabricant):
                    fabricant = getattr(
                        self,
                        champ_fabricant,
                        None,
                    )

                    get_fabricant_display = getattr(
                        self,
                        f"get_{champ_fabricant}_display",
                        None,
                    )

                    if callable(get_fabricant_display):
                        fabricant_label = get_fabricant_display()
                    else:
                        fabricant_label = fabricant

                # Qualité
                qualite = None
                qualite_label = None

                if hasattr(self, champ_qualite):
                    qualite = getattr(
                        self,
                        champ_qualite,
                        None,
                    )

                    get_qualite_display = getattr(
                        self,
                        f"get_{champ_qualite}_display",
                        None,
                    )

                    if callable(get_qualite_display):
                        qualite_label = get_qualite_display()
                    else:
                        qualite_label = qualite

                # Type
                type_produit = None
                type_label = None

                if hasattr(self, champ_type):
                    type_produit = getattr(
                        self,
                        champ_type,
                        None,
                    )

                    get_type_display = getattr(
                        self,
                        f"get_{champ_type}_display",
                        None,
                    )

                    if callable(get_type_display):
                        type_label = get_type_display()
                    else:
                        type_label = type_produit

                # Unité
                unite = ""

                if any(
                        texte in champ_base
                        for texte in [
                            "huile",
                            "liquide",
                            "refroidissement",
                        ]
                ):
                    unite = "L"

                rapport.append({
                    "champ": field.verbose_name,
                    "designation": field.verbose_name,
                    "code": field_name,

                    "etat": etat,
                    "etat_label": etat_label,

                    "fabricant": fabricant,
                    "fabricant_label": fabricant_label,

                    "qualite": qualite,
                    "qualite_label": qualite_label,

                    "type": type_produit,
                    "type_label": type_label,

                    "quantite": quantite,
                    "unite": unite,

                    "prix": prix,
                    "prix_unitaire": prix,

                    "total": total,
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

        temps_minutes = Decimal(
            str(self.main_oeuvre.temps_minutes or 0)
        )

        taux_horaire = Decimal(
            str(self.taux_horaire or Decimal("50.00"))
        )

        cout = (
                temps_minutes
                / Decimal("60")
                * taux_horaire
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


