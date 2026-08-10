from datetime import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantLubrifiant, TypeHuileDirection, \
    AmpouleAutomobile, FabricantFrein, MatierePlaquetteFrein, MatiereFrein, TypeDisqueFrein, RefroidissementFabricant
from maintenance.models import Maintenance
from maintenance.nettoyage_exterieur.models import EtatAjouter
from django.conf import settings
from utils.mixin import TechnicienMixin





# ---------------------------
# TextChoices
# ---------------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class CrochetPresent(models.TextChoices):
    OK = "OK", _("Monté")
    NOT_OK = "NOT_OK", _("Démonté")

class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class PhareEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")

class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")


class NiveauxEtat(models.TextChoices):
    OK = "OK", _("OK")
    AJOUTER = "AJOUTER", _("Ajouté")
    REMPLACER = "REMPLACER", _("A remplacer")


class HuileEtat(models.TextChoices):
    ZERO_16 = "0W16", _("0W16")
    ZERO_20 = "0W20", _("0W20")
    ZERO_30 = "0W30", _("0W30")
    ZERO_40 = "0W40", _("0W40")
    CINQ_20 = "5W20", _("5W20")
    CINQ_30 = "5W30", _("5W30")
    CINQ_40 = "5W40", _("5W40")
    DIX_40 = "10W40", _("10W40")
    DIX_50 = "10W50", _("10W50")
    DIX_60 = "10W60", _("10W60")
    QUINZE_40 = "15W40", _("15W40")
    QUINZE_50 = "15W50", _("15W50")
    VINGT_50 = "20W50", _("20W50")


class HuileBoiteEtat(models.TextChoices):
    SEPTANTE_CINQ = "75W", _("75W")
    SEPTANTE_5_80 = "75W80", _("75W80")
    SEPTANTE_CINQ90  = "75W90", _("75W90")
    QUATRE_20 = "80W", _("80W")
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF_DSG", _("ATF DSG")
    ATF_DCT = "ATF_DCT", _("ATF DCT")
    ATF_CVT = "ATF_CVT", _("ATF CVT")
    ATF_DEXRON_II = "ATF_DEXRON_II", _("ATF Dexron II")
    ATF_DEXRON_III = "ATF_DEXRON_III", _("ATF Dexron III")
    ATF_DEXRON_VI = "ATF_DEXRON_VI", _("ATF Dexron VI")
    ATF_MERCON = "ATF_MERCON", _("ATF Mercon")
    ATF_MERCON_V = "ATF_MERCON_V", _("ATF Mercon V")
    ATF_MERCON_LV = "ATF_MERCON_LV", _("ATF Mercon LV")
    ATF_MULTI = "ATF_MULTI", _("ATF Multi Vehicle")
    ATF_WS = "ATF_WS", _("ATF Toyota WS")
    ATF_ZF_LIFEGUARD = "ATF_ZF_LIFEGUARD", _("ZF Lifeguard")
    ATF_MOPAR = "ATF_MOPAR", _("Mopar ATF+4")
    ATF_AISIN = "ATF_AISIN", _("Aisin ATF")
    ATF_MBV236 = "ATF_MBV236", _("Mercedes MB 236.x")
    ATF_VOLVO = "ATF_VOLVO", _("Volvo ATF")
    ATF_HONDA = "ATF_HONDA", _("Honda ATF DW-1")
    ATF_NISSAN = "ATF_NISSAN", _("Nissan Matic")
    Huile_PDK_FFL_3 = "PDK_FFL-3", _("PDK FFL 3")
    AUTRE = "AUTRE", _("Autre")

class HuilePontEtat(models.TextChoices):
    SEPTANTE_CINQ140 = "75W140", _("75W140")
    SEPTANTE_CINQ90 = "75W90", _("Porsche 75W90")
    AUTRE = "AUTRE", _("Autre")


class RefroidissementEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class PneuEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class RefroidissementQualiteEtat(models.TextChoices):
    # Volkswagen Group
    G11 = "G11", _("G 11")
    G12 = "G12", _("G 12")
    G12_PLUS = "G12_PLUS", _("G 12+")
    G12_PLUS_PLUS = "G12_PLUS_PLUS", _("G 12++")
    G13 = "G13", _("G 13")

    # BMW
    G48 = "G48", _("G 48 BMW")

    # Mercedes-Benz
    MB_325_0 = "MB_325_0", _("MB 325.0")
    MB_325_3 = "MB_325_3", _("MB 325.3")
    MB_325_5 = "MB_325_5", _("MB 325.5")

    # Renault / Dacia
    TYPE_D = "TYPE_D", _("Type D")

    # PSA (Peugeot / Citroën)
    PSA_B71_5110 = "PSA_B71_5110", _("PSA B71 5110")

    # Ford
    WSS_M97B44_D = "WSS_M97B44_D", _("Ford WSS-M97B44-D")
    WSS_M97B51_A1 = "WSS_M97B51_A1", _("Ford WSS-M97B51-A1")

    # General Motors
    DEX_COOL = "DEX_COOL", _("Dex-Cool")

    # Toyota / Lexus
    TOYOTA_SLLC = "TOYOTA_SLLC", _("Toyota SLLC")

    # Honda
    HONDA_TYPE_2 = "HONDA_TYPE_2", _("Honda Type 2")

    # Nissan
    NISSAN_L248 = "NISSAN_L248", _("Nissan L248")
    NISSAN_L250 = "NISSAN_L250", _("Nissan L250")

    # Hyundai / Kia
    HYUNDAI_KIA_LLC = "HYUNDAI_KIA_LLC", _("Hyundai/Kia Long Life Coolant")
    AUTRE = "AUTRE", _("Autre")

class ReadyForOK(models.TextChoices):
    VIDE = "", "---------"
    SPA200 = "SPA200", _("Spa-Francorchamps 200 km")
    SPA300 = "SPA300", _("Spa-Francorchamps 300 km")
    SPA400 = "SPA400", _("Spa-Francorchamps 400 km")
    NURBURG2 = "NURBURG2", _("Nürburgring 2 tours")
    NURBURG5 = "NURBURG5", _("Nürburgring 5 tours")
    NURBURG7 = "NURBURG7", _("Nürburgring 7 tours")
    NURBURG10 = "NURBURG10", _("Nürburgring 10 tours")
    NURBURG12 = "NURBURG12", _("Nürburgring 12 tours")
    NURBURG15 = "NURBURG15", _("Nürburgring 15 tours")
    AUTRE200 = "AUTRE200", _("Autre circuit 200 km")
    AUTRE300 = "AUTRE300", _("Autre circuit 300 km")
    AUTRE400 = "AUTRE400", _("Autre circuit 400 km")

class QualiteLiquideFrein(models.TextChoices):
    DOT3 = "DOT3", _("DOT 3")
    DOT4 = "DOT4", _("DOT 4")
    DOT5 = "DOT5", _("DOT 5")
    DOT51 = "DOT51", _("DOT 5.1")

class LiquideFreinEtat(models.TextChoices):
    OK = "OK", _("OK")
    AJOUTER = "AJOUTER", _("Ajouté")
    A_REMPLACER = "A_REMPLACER", _("A remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
# ---------------------------
# Modèle fusionné
# ---------------------------
class CheckupTrack(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="checkup_track",
        verbose_name=_("Checkup Track"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="checkup_track",
        verbose_name="Kilomètres checkup piste",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_checkup_track = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du checkup piste"),
    )



    # --- Essuie-glaces & Pare-brise ---
    essuie_glace = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Etat des balais avant"))
    essuie_glace_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    essuie_glace_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))


    balais_essuie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Etat des balais arrières"))
    balais_essuie_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    balais_essuie_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))


    pare_brise_av_coups = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise sans coups"))
    pare_brise_av_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise à remplacer"))
    pare_brise_av_quantite = models.PositiveIntegerField(
        verbose_name=_("Quantité"),
        default=0,
        null=True,
    )
    pare_brise_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))


    # --- Moteur & transmission ---
    moteur_etat =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État du moteur"))
    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.OK, verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.MOBIL, verbose_name=_("Fabricant de l'huile moteur"))
    moteur_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité d'huile ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))
    moteur_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva de l'huile moteur"))


    boite_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État de la boîte de vitesse"))
    boite_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État de l'embrayage"))
    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.OK,verbose_name=_("Niveau d'huile"))
    boite_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant de l'huile de boite de vitesse"))
    boite_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité d'huile ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité d'huile"))
    boite_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva de l'huile de boite"))

    # --- Pont ----

    pont_niveau_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite pont arrière"))
    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.OK,verbose_name=_("Niveau d'huile"))
    pont_niveau_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant de l'huile de pont"))
    pont_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité d'huile ajoutée en litres"), validators=[StepValueValidator(0.1)])
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ140,verbose_name=_("Qualité d'huile"))
    pont_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva de l'huile de pont"))

    # --- Refroidissement ---
    refroidissement_radiateur = models.CharField(max_length=25, choices=RefroidissementEtat.choices,default=RefroidissementEtat.OK, verbose_name=_("Radiateur"))
    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.OK,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_fabricant = models.CharField(max_length=25, choices=RefroidissementFabricant.choices,default=RefroidissementFabricant.CHOISIR,verbose_name=_("Fabricant du liquide de refroidissement"))
    refroidissement_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"), validators=[StepValueValidator(0.1)])
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13, verbose_name=_("Qualité de liquide de refroidissement"))
    refroidissement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du liquide de refroidissement"))

    # --- Freins ---

    freins_plaquettes_remplacer_av_usure = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avant (%)"))
    freins_plaquettes_remplacer_av_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes avant à remplacer"))
    freins_plaquettes_remplacer_av_quantite = models.PositiveIntegerField(default=0,  verbose_name=_("Quantité"))
    freins_plaquettes_remplacer_av_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant des plaquettes"))
    freins_plaquettes_remplacer_av_qualite = models.CharField(max_length=25, choices=MatierePlaquetteFrein.choices, default=MatierePlaquetteFrein.CHOISIR,verbose_name=_("Matière des plaquettes"))
    freins_plaquettes_remplacer_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))






    freins_epaisseur_disques_av_usure = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    freins_epaisseur_disques_av_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Disques avant à remplacer"))
    freins_epaisseur_disques_av_fentes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques arrière"))
    freins_epaisseur_disques_av_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    freins_epaisseur_disques_av_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant des disques"))
    freins_epaisseur_disques_av_qualite = models.CharField(max_length=25, choices=MatiereFrein.choices,default=MatiereFrein.CHOISIR,verbose_name=_("Matière des disques"))
    freins_epaisseur_disques_av_type = models.CharField(max_length=25, choices=TypeDisqueFrein.choices,default=TypeDisqueFrein.CHOISIR,verbose_name=_("Type de disques"))
    freins_epaisseur_disques_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    freins_plaquettes_remplacer_ar_usure = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrière (%)"))
    freins_plaquettes_remplacer_ar_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Plaquettes arrière à remplacer"))
    freins_plaquettes_remplacer_ar_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant des plaquettes"))
    freins_plaquettes_remplacer_ar_qualite = models.CharField(max_length=25, choices=MatierePlaquetteFrein.choices,default=MatierePlaquetteFrein.CHOISIR,verbose_name=_("Matière des plaquettes"))
    freins_plaquettes_remplacer_ar_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    freins_plaquettes_remplacer_ar_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))



    freins_epaisseur_disques_ar_usure = models.FloatField(default=0.0,verbose_name=_("Épaisseur des disques arrière (mm)"))
    freins_epaisseur_disques_ar_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,verbose_name=_("Disques arrière à remplacer"))
    freins_epaisseur_disques_ar_fentes= models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes sur les disques"))
    freins_epaisseur_disques_ar_fabricant = models.CharField(max_length=25, choices=FabricantFrein.choices,default=FabricantFrein.CHOISIR,verbose_name=_("Fabricant des plaquettes"))
    freins_epaisseur_disques_ar_qualite = models.CharField(max_length=25, choices=MatiereFrein.choices,default=MatiereFrein.CHOISIR,verbose_name=_("Matière des disques"))
    freins_epaisseur_disques_ar_type = models.CharField(max_length=25, choices=TypeDisqueFrein.choices,default=TypeDisqueFrein.CHOISIR,verbose_name=_("Type des disques"))
    freins_epaisseur_disques_ar_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    freins_epaisseur_disques_ar_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva"))





    freins_liquide_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fuite"))
    # --- Liquide ---
    freins_liquide_etat = models.CharField(max_length=25, choices=LiquideFreinEtat.choices, default=LiquideFreinEtat.OK, verbose_name=_("État liquide de frein"))
    freins_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CASTROL, verbose_name=_("Fabricant du liquide de frein"))
    freins_liquide_qualite = models.CharField(max_length=100,choices=QualiteLiquideFrein.choices, default=QualiteLiquideFrein.DOT4, blank=True, verbose_name=_("Spécification liquide de frein"))
    freins_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité liquide de frein (L)"), validators=[StepValueValidator(0.1)])
    freins_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du liquide de frein"))


    direction_liquide = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Etat direction assistée / crémaillère"), null=True, blank=True)
    direction_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.OK, verbose_name=_("Niveau du liquide de direction"), null=True, blank=True)
    direction_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CASTROL, verbose_name=_("Fabricant"))
    direction_liquide_qualite = models.CharField(max_length=25, choices=TypeHuileDirection.choices, default=TypeHuileDirection.CHOISIR, verbose_name=_("Qualité du liquide de direction"), null=True, blank=True)
    direction_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4, decimal_places=1,verbose_name=_("Quantité liquide de direction (L)"), validators=[StepValueValidator(0.1)])
    direction_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du liquide de direction"))

    # --- Bruits ---
    bruit_roulement_roue= models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruit de roulement de roue"), blank=True, null=True)

    jeu_roulement_roue = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu roulement de roue"))

    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeux rotules de direction"))


    jeu_rotule_suspension = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotules de suspension"))


    jeu_biellette_bar_stab = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK,    blank=True,
    null=True ,verbose_name=_("Jeu biellettes de barre stabilisatrice"))

    jeu_barre_stabilisatrice = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu barre stabilisatrice"))


    jeu_biellette_direction = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de direction"))

    jeu_cardan = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu des cardan"))

    jeu_arbre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu dans l'arbre de transmission"))


    jeu_amortisseur = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu amortisseur"))


    jeu_triangle = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle"))

    jeu_multi_bras = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras"))


    # phares#

    phares_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de route"),
    )
    phares_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_gros_phares = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Grands phares"),
    )
    phares_gros_phares_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_gros_phares_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_gros_phares_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_clignotants = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Clignotants"),
    )
    phares_clignotants_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_clignotants_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_clignotants_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_recul = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de recul"),
    )
    phares_recul_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_recul_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_recul_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_anti_brouillard_avant = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard avant"),
    )
    phares_anti_brouillard_avant_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_avant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_anti_brouillard_avant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_anti_brouillard_arriere = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Phares anti-brouillard arrière"),
    )
    phares_anti_brouillard_arriere_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_anti_brouillard_arriere_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_anti_brouillard_arriere_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_feux_stops = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux stop"),
    )
    phares_feux_stops_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_stops_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_feux_stops_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_troisieme_feux_stop = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Troisième feu stop"),
    )
    phares_troisieme_feux_stop_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_troisieme_feux_stop_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_troisieme_feux_stop_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_feux_position_av = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position avant"),
    )
    phares_feux_position_av_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_feux_position_av_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    phares_feux_position_ar = models.CharField(
        max_length=25,
        choices=PhareEtat.choices,
        default=PhareEtat.OK,
        verbose_name=_("Feux de position arrière"),
    )
    phares_feux_position_ar_type = models.CharField(
        max_length=25,
        choices=AmpouleAutomobile.choices,
        default=AmpouleAutomobile.CHOISIR,
        verbose_name=_("Type d'ampoule"),
    )
    phares_feux_position_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    phares_feux_position_ar_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    # --- Pneus et Pression


    pneu_epaisseur_avd = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant droit (mm)"))
    pneu_epaisseur_avg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant gauche (mm)"))
    pneu_epaisseur_ard = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière droit (mm)"))
    pneu_epaisseur_arg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière gauche (mm)"))

    pneu_sidewall = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Flanc des pneus"))


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


    pneu_train_av = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Etat du train avant"))
    pneu_train_av_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pneu_train_av_quantite = models.PositiveIntegerField(default=1, null=True, blank=True, verbose_name=_("Quantité"))

    pneu_train_ar = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Etat du train arrière"))
    pneu_train_ar_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    pneu_train_ar_quantite = models.PositiveIntegerField(default=1, null=True, blank=True, verbose_name=_("Quantité"))


    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE, verbose_name=_("Serrage des roues"))

    crochet_de_remorquage = models.CharField(max_length=25, choices=CrochetPresent.choices, default=CrochetPresent.NOT_OK,verbose_name=_("Crochet de remorquage"))

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
    nettoyage_interieur_plastiques = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Plastiques"), null=True,blank=True)
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

    ready_for = models.CharField(max_length=25, choices=ReadyForOK.choices, verbose_name=_("Prête pour :"), blank=True, default="")

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checkup_track",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="checkup_track"
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
        related_name="checkup_track"
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
        if self.voiture_exemplaire and self.kilometrage_checkup_track is not None:
            if (
                    self.kilometrage_checkup_track is not None
                    and self.voiture_exemplaire
                    and self.kilometrage_checkup_track < self.voiture_exemplaire.kilometres_chassis
            ):
                raise ValidationError({
                    'kilometrage_checkup_track': _(
                        f"Le kilométrage du check-up ({self.kilometrage_checkup_track}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture "
                        f"({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })


        if self.serrage_roues == RouesSerrageEtat.A_FAIRE:
            raise ValidationError({
                "serrage_roues": _(
                    "Vous devez indiquer si le serrage des roues a été effectué avant d'enregistrer ce contrôle."
                )
            })

    def save(self, *args, **kwargs):

        # ----------------------------
        # TECHNICIEN
        # ----------------------------
        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # ----------------------------
        # KILOMÉTRAGE CHECKUP
        # ----------------------------
        if self.kilometrage_checkup_track > self.voiture_exemplaire.kilometres_chassis:
            self.voiture_exemplaire.kilometres_chassis = self.kilometrage_checkup_track
            self.voiture_exemplaire.kilometres_dernier_entretien = self.kilometrage_checkup_track
            self.voiture_exemplaire.date_derniere_intervention = timezone.now().date()

            self.voiture_exemplaire.update_kilometres()
            self.voiture_exemplaire.save()

        # ----------------------------
        # MAIN D'OEUVRE (FIX UNIQUE SAVE)
        # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Checkup piste") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # ----------------------------
        # MAINTENANCE UPDATE (SAFE)
        # ----------------------------
        if self.maintenance:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.CHECKUP_TRACK
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            self.maintenance.save(update_fields=[
                "type_maintenance",
                "voiture_exemplaire"
            ])

        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        # Correspondances particulières du modèle CheckupTrack.
        configuration = {
            "moteur_niveau_huile": {
                "etat": "moteur_niveau_huile_etat",
                "qualite": "moteur_niveau_huile_qualite",
                "quantite": "moteur_niveau_huile_quantite",
                "libelle": _("Huile moteur"),
                "unite": _("L"),
            },
            "boite_niveau_huile": {
                "etat": "boite_niveau_huile_etat",
                "qualite": "boite_niveau_huile_qualite",
                "quantite": "boite_niveau_huile_quantite",
                "libelle": _("Huile de boîte de vitesses"),
                "unite": _("L"),
            },
            "pont_niveau_huile": {
                "etat": "pont_niveau_huile_etat",
                "qualite": "pont_niveau_huile_qualite",
                "quantite": "pont_niveau_huile_quantite",
                "libelle": _("Huile de pont"),
                "unite": _("L"),
            },
            "refroidissement": {
                "etat": "refroidissement_etat",
                "fabricant": "refroidissement_fabricant",
                "qualite": "refroidissement_qualite",
                "quantite": "refroidissement_quantite",
                "libelle": _("Liquide de refroidissement"),
                "unite": _("L"),
            },
            "freins_plaquettes_remplacer_av": {
                "etat": "freins_plaquettes_remplacer_av_etat",
                "qualite": "freins_plaquettes_remplacer_av_qualite",
                "quantite": "freins_plaquettes_remplacer_av_quantite",
                "unite": _("Set"),
            },

            "freins_plaquettes_remplacer_ar": {
                "etat": "freins_plaquettes_remplacer_ar_etat",
                "qualite": "freins_plaquettes_remplacer_ar_qualite",
                "quantite": "frein_splaquettes_remplacer_ar_quantite",
                "unite": _("Set"),
            },
            "freins_epaisseur_disques_av": {
                "etat": "freins_epaisseur_disques_av_etat",
                "qualite": "freins_epaisseur_disques_av_qualite",
                "quantite": "freins_epaisseur_disques_av_quantite",
                "unite": _("Set"),
            },
            "freins_epaisseur_disques_ar": {
                "etat": "freins_epaisseur_disques_ar_etat",
                "qualite": "freins_epaisseur_disques_ar_qualite",
                "quantite": "freins_epaisseur_disques_ar_quantite",
                "unite": _("Set"),
            },

            "frein_liquide": {
                "etat": "frein_liquide_frein_etat",
                "fabricant": "frein_liquide_fabricant",
                "qualite": "freins_liquide_qualite",
                "quantite": "freins_liquide_quantite",
                "libelle": _("Liquide de frein"),
                "unite": _("L"),
            },
            "direction_liquide": {
                "etat": "direction_liquide_etat",
                "niveau": "direction_liquide_niveau",
                "qualite": "direction_liquide_qualite",
                "quantite": "direction_liquide_quantite",
                "libelle": _("Liquide de direction assistée"),
                "unite": _("L"),
            },
            "pneu_train_av": {
                "etat": "pneu_train_av",
                "quantite": "pneu_train_av_quantite",
                "libelle": _("Pneus du train avant"),
                "unite": _("pneu"),
            },
            "pneu_train_ar": {
                "etat": "pneu_train_ar",
                "quantite": "pneu_train_ar_quantite",
                "libelle": _("Pneus du train arrière"),
                "unite": _("pneu"),
            },
            "nettoyage_exterieur_produits": {
                "etat": "nettoyage_exterieur_produits",
                "quantite": "nettoyage_exterieur_produits_quantite",
                "libelle": _("Produits de nettoyage extérieur"),
                "unite": _("unité"),
            },
            "nettoyage_interieur_produits": {
                "etat": "nettoyage_interieur_produits",
                "quantite": "nettoyage_interieur_produits_quantite",
                "libelle": _("Produits de nettoyage intérieur"),
                "unite": _("unité"),
            },
            "pare_brise_av": {
                "etat": "pare_brise_av_remplacer",
                "quantite": "pare_brise_av_quantite",
                "libelle": _("Pare-brise"),
                "unite": _("unité"),
            },


        }

        def convertir_decimal(valeur):
            if valeur in (None, ""):
                return Decimal("0.00")

            try:
                return Decimal(str(valeur))
            except (TypeError, ValueError, ArithmeticError):
                return Decimal("0.00")

        def obtenir_display(nom_champ, valeur):
            if not nom_champ:
                return valeur or "-"

            methode_display = getattr(
                self,
                f"get_{nom_champ}_display",
                None,
            )

            if callable(methode_display):
                return methode_display()

            return valeur or "-"

        for field in self._meta.fields:
            field_name = field.name

            # Seulement les champs contenant un prix.
            if not field_name.endswith("_prix"):
                continue

            champ_base = field_name.removesuffix("_prix")
            config = configuration.get(champ_base, {})

            # Quantité personnalisée ou convention standard.
            champ_quantite = config.get(
                "quantite",
                f"{champ_base}_quantite",
            )

            if not hasattr(self, champ_quantite):
                continue

            prix = convertir_decimal(
                getattr(self, field_name, None)
            )

            quantite = convertir_decimal(
                getattr(self, champ_quantite, None)
            )

            # Une ligne n'est ajoutée que si prix et quantité existent.
            if prix <= 0 or quantite <= 0:
                continue

            prix = prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            quantite = quantite.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total = (
                    prix * quantite
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            # =====================================================
            # ÉTAT
            # =====================================================

            champ_etat = config.get("etat")

            if not champ_etat:
                if hasattr(self, champ_base):
                    champ_etat = champ_base
                elif hasattr(self, f"{champ_base}_etat"):
                    champ_etat = f"{champ_base}_etat"

            etat = (
                getattr(self, champ_etat, "")
                if champ_etat
                else ""
            )

            etat_label = obtenir_display(
                champ_etat,
                etat,
            )

            # =====================================================
            # NIVEAU
            # =====================================================

            champ_niveau = config.get(
                "niveau",
                f"{champ_base}_niveau",
            )

            niveau = (
                getattr(self, champ_niveau, "")
                if hasattr(self, champ_niveau)
                else ""
            )

            niveau_label = obtenir_display(
                champ_niveau,
                niveau,
            )

            # =====================================================
            # FABRICANT
            # =====================================================

            champ_fabricant = config.get(
                "fabricant",
                f"{champ_base}_fabricant",
            )

            fabricant = (
                getattr(self, champ_fabricant, "")
                if hasattr(self, champ_fabricant)
                else ""
            )

            fabricant_label = obtenir_display(
                champ_fabricant,
                fabricant,
            )

            # =====================================================
            # QUALITÉ
            # =====================================================

            champ_qualite = config.get(
                "qualite",
                f"{champ_base}_qualite",
            )

            qualite = (
                getattr(self, champ_qualite, "")
                if hasattr(self, champ_qualite)
                else ""
            )

            qualite_label = obtenir_display(
                champ_qualite,
                qualite,
            )

            # =====================================================
            # TYPE, PRINCIPALEMENT POUR LES AMPOULES
            # =====================================================

            champ_type = config.get(
                "type",
                f"{champ_base}_type",
            )

            type_piece = (
                getattr(self, champ_type, "")
                if hasattr(self, champ_type)
                else ""
            )

            type_label = obtenir_display(
                champ_type,
                type_piece,
            )

            # =====================================================
            # LIBELLÉ
            # =====================================================

            libelle = config.get("libelle")

            if not libelle:
                try:
                    champ_principal = self._meta.get_field(champ_base)
                    libelle = champ_principal.verbose_name
                except Exception:
                    libelle = (
                        champ_base
                        .replace("_", " ")
                        .capitalize()
                    )

            # Pour les ampoules, le type est ajouté au libellé.
            if (
                    champ_base.startswith("phares_")
                    and type_label not in ("", "-", None)
            ):
                libelle = _("%(piece)s — %(type)s") % {
                    "piece": libelle,
                    "type": type_label,
                }

            # Unité par défaut.
            if champ_base.startswith("phares_"):
                unite = _("ampoule")
            else:
                unite = config.get("unite", _("pièce"))

            rapport.append({
                "champ": libelle,
                "nom": libelle,
                "designation": libelle,
                "piece": libelle,
                "code": champ_base,

                "etat": etat,
                "etat_label": etat_label,
                "etat_display": etat_label,

                "niveau": niveau,
                "niveau_label": niveau_label,

                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "qualite": qualite,
                "qualite_label": qualite_label,

                "type": type_piece,
                "type_label": type_label,

                "quantite": quantite,
                "unite": unite,

                "prix": prix,
                "prix_unitaire": prix,
                "total": total,
            })

            total_general += total

        total_general = total_general.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": rapport,
            "pieces": rapport,
            "rapport": rapport,
            "nombre_elements": len(rapport),
            "total_general": total_general,
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

