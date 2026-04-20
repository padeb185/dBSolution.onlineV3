from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.models import Maintenance
from utilisateurs.models import Utilisateur
from django.conf import settings
from utils.mixin import TechnicienMixin


# ---------------------------
# TextChoices
# ---------------------------

class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("Non")
    NOT_OK = "NOT_OK", _("Oui")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class BatterieEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class PhareEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class NettoyageEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")
    PROPRE = "PROPRE", _("Propre")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("Bon")
    AJOUTER = "AJOUTER", _("Ajouter")


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
    QUATRE_20 = "80W", "80W"
    QUATRE_20_90 = "80W90", _("80W90")
    QUATRE_25_90 = "85W90", _("85W90")
    ATF3 = "ATF_III", _("ATF III")
    ATF_DSG = "ATF DSG", _("ATF DSG")


class HuilePontEtat(models.TextChoices):
    SEPTANTE_CINQ140 = "75W140", _("75W140")


class RefroidissementEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class PneuEtat(models.TextChoices):
    OK = "OK", _("OK")
    NON = "NON", _("Non")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")

class RefroidissementQualiteEtat(models.TextChoices):
    # Volkswagen Group
    G11 = "G11", _("G 11")
    G12 = "G12", _("G 12")
    G12_PLUS = "G12_PLUS", _("G 12+")
    G12_PLUS_PLUS = "G12_PLUS_PLUS", _("G 12++")
    G13 = "G13", _("G 13")

    # BMW
    G48 = "G48", _("G 48")

    # Mercedes-Benz
    MB_325_0 = "MB_325_0", _("MB 325.0")
    MB_325_3 = "MB_325_3", _("MB 325.3")
    MB_325_5 = "MB_325_5", _("MB 325.5")

    # Renault / Dacia
    TYPE_D = "TYPE_D", _("Type D")

    # PSA (Peugeot / Citroën)
    PSA_B71_5110 = "PSA_B71_5110", _("PSA B71 5110")

    # Ford
    WSS_M97B44_D = "WSS_M97B44_D", _("WSS-M97B44-D")
    WSS_M97B51_A1 = "WSS_M97B51_A1", _("WSS-M97B51-A1")

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

# ---------------------------
# Modèle fusionné
# ---------------------------
class ControleGeneral(TechnicienMixin, models.Model):
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="controle_general_checkup",
        verbose_name=_("Maintenance"),
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
        blank=True
    )

    kilometrage_checkup = models.PositiveIntegerField(
        _("Kilométrage au moment du Checkup"),
        null=True,
        blank=True
    )



    # --- Essuie-glaces & Pare-brise ---
    essuie_glace_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK, verbose_name=_("Essuie-glace AV fonctionnel"))
    essuie_glace_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NOT_OK, verbose_name=_("Essuie-glace AR fonctionnel"))
    balais_essuie_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Balais avant a remplacer"))
    balais_essuie_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Balai arrière à remplacer"))

    pare_brise_coups = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise avec coups"))
    pare_brise_remplacer = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Pare-brise à remplacer"))

    # --- Moteur & transmission ---
    moteur_fuite =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite moteur"))
    moteur_bruit =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruit moteur"))
    moteur_perte =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Perte de puissance"))
    moteur_casse =  models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Moteur à remplacer"))
    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON, verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))

    boite_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite boîte de vitesse"))
    boite_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits boîte de vitesse"))
    boite_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Problème d'embrayage"))
    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    boite_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileBoiteEtat.SEPTANTE_CINQ, verbose_name=_("Qualité d'huile"))

    # --- Pont ----

    pont_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite pont arrière"))
    pont_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bruits pont arrière"))
    pont_jeu = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu pont arrière"))
    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    pont_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ140,verbose_name=_("Qualité d'huile"))


    # --- Refroidissement ---

    refroidissement_radiateur = models.CharField(max_length=25, choices=RefroidissementEtat.choices, default=RefroidissementEtat.OK, verbose_name=_("Radiateur"))
    refroidissement_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"))
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13, verbose_name=_("Qualité de liquide de refroidissement"))


    # --- Freins ---

    freins_usure_plaquettes_av = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes avant (%)"))
    freins_plaquettes_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes avant à remplacer"))
    freins_epaisseur_disques_av = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    freins_fentes_disques_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques avant"))
    freins_disques_remplacer_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques avant à remplacer"))

    freins_usure_plaquettes_ar = models.IntegerField(default=0, verbose_name=_("Usure des plaquettes arrière (%)"))
    freins_plaquettes_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes arrière à remplacer"))
    freins_epaisseur_disques_ar = models.FloatField(default=0, verbose_name=_("Épaisseur des disques arrière (mm)"))
    freins_fentes_disques_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fentes sur les disques arrière"))
    freins_disques_remplacer_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques arrière à remplacer"))

    freins_fuites = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Présence de fuite"))


    # --- Liquide ---
    frein_liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État liquide de frein"))
    freins_remplacement_liquide_frein = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Remplacement liquide de frein"))
    freins_specif_liquide_frein = models.CharField(max_length=100, blank=True, verbose_name=_("Spécification liquide de frein"))
    freins_quantite_liquide_frein = models.FloatField(default=0, null=True, blank=True, verbose_name=_("Quantité liquide de frein (L)"))

    direction_fuite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fuite direction assistée / crémaillère"), null=True, blank=True)
    niveau_direction = models.FloatField(default=0.0, null=True, blank=True, verbose_name=_("Niveau liquide direction"))

    # --- Bruits ---
    bruit_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue avant droit"), blank=True, null=True)
    bruit_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("État roulement de roue avant gauche"),  blank=True, null=True)
    bruit_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière droit"), blank=True, null=True)
    bruit_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("État roulement de roue arrière gauche"),  blank=True, null=True)


    # --- Batterie ---
    batterie_etat =models.CharField(max_length=25, choices=BatterieEtat.choices, default=BatterieEtat.OK, verbose_name=_("État batterie"))

    # --- Jeux ---

    jeu_rotule_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction avant droite"))
    jeu_rotule_direction_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction avant gauche"))
    jeu_rotule_direction_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction arrière droite"))
    jeu_rotule_direction_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu rotule de direction arrière gauche"))

    jeu_rotule_suspension_inferieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant droite"))
    jeu_rotule_suspension_inferieure_avg= models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure avant gauche"))
    jeu_rotule_suspension_inferieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))
    jeu_rotule_suspension_inferieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeux rotule de suspension inférieure arrière droite"))

    jeu_rotule_suspension_superieure_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant droite"))
    jeu_rotule_suspension_superieure_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure avant gauche"))
    jeu_rotule_suspension_superieure_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))
    jeu_rotule_suspension_superieure_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeux rotule de suspension supérieure arrière droite"))

    jeu_Biellette_barre_stabilisatrice_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant droite"))
    jeu_Biellette_barre_stabilisatrice_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice avant gauche"))
    jeu_Biellette_barre_stabilisatrice_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière droite"))
    jeu_Biellette_barre_stabilisatrice_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de barre stabilisatrice arrière gauche"))

    jeu_barre_stabilisatrice_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu barre stabilisatrice avant"))
    jeu_barre_stabilisatrice_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu barre stabilisatrice arrière"))

    jeu_biellette_direction_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu biellette de direction droite"))
    jeu_biellette_direction_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu biellette de direction gauche"))

    jeu_cardan_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu du cardan avant droit"))
    jeu_cardan_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu du cardan avant droit"))
    jeu_cardan_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu du cardan avant droit"))
    jeu_cardan_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu du cardan avant droit"))

    jeu_arbre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu dans l'arbre de transmission"))


    jeu_amortisseur_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices,default=EtatOKNotOK.OK, verbose_name=_("Jeu amortisseur avant droit"))
    jeu_amortisseur_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur avant gauche"))
    jeu_amortisseur_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière droit"))
    jeu_amortisseur_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu amortisseur arrière gauche"))

    jeu_roulement_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant droit"))
    jeu_roulement_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement avant gauche"))
    jeu_roulement_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement arrière droit"))
    jeu_roulement_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu roulement arrière gauche"))

    jeu_triangle_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant droit"))
    jeu_triangle_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle avant gauche"))
    jeu_triangle_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière droit"))
    jeu_triangle_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu triangle arrière gauche"))

    jeu_multi_bras_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant droit"))
    jeu_multi_bras_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras avant gauche"))
    jeu_multi_bras_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière droit"))
    jeu_multi_bras_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Jeu suspension multi-bras arrière gauche"))

    # --- Pneus et Pression

    pneu_epaisseur_avd = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu avant droit (mm)"))
    pneu_epaisseur_avg = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu avant gauche (mm)"))
    pneu_epaisseur_ard = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu arrière droit (mm)"))
    pneu_epaisseur_arg = models.FloatField(default=0.0, verbose_name=_("Épaisseur du pneu arrière gauche (mm)"))

    pneu_sidewall_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("flanc du pneu avant droit"))
    pneu_sidewall_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu avant gauche"))
    pneu_sidewall_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu arrière droit"))
    pneu_sidewall_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flanc du pneu arrière gauche"))

    pneu_pression_bar_avd = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant droit en bar"))
    pneu_pression_bar_avg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant gauche en bar"))
    pneu_pression_bar_ard = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière droit en bar"))
    pneu_pression_bar_arg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière gauche en bar"))


    pneu_train_av =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.NON, verbose_name=_("Train avant à remplacer"))
    pneu_train_ar =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.NON, verbose_name=_("Train arrière à remplacer"))



    # --- Réglage phares ---
    phares_reglages = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Réglage phares"))
    phares_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de route"))
    phares_gros_phares = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Grand phares"))
    phares_clignotants = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Clignotants"))
    phares_recul = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de recul"))
    phares_anti_brouillard_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Phares anti-brouillard avant"))
    phares_anti_brouillard_arriere = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK, verbose_name=_("Phares anti-brouillard arrière"))


    # --- Nettoyage extérieur ---
    nettoyage_exterieur_traces_gomme = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Traces de gomme"))
    nettoyage_exterieur_carrosserie = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carrosserie"))
    nettoyage_exterieur_jantes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Jantes"))
    nettoyage_exterieur_sechage = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Séchage"))

    # --- Nettoyage intérieur ---
    nettoyage_interieur_vitres = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Vitres"))
    nettoyage_interieur_pare_brise = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Pare-brise"))
    nettoyage_interieur_aspirateur = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Aspirateur"))
    nettoyage_interieur_portes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Intérieurs de porte"))
    nettoyage_interieur_sieges = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Sièges"))
    nettoyage_interieur_carpettes = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Carpettes"))
    nettoyage_interieur_tableau_de_bord = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Tableau de bord"))
    nettoyage_interieur_plastiques = models.CharField(max_length=25, choices=NettoyageEtat.choices, default=NettoyageEtat.A_FAIRE, verbose_name=_("Plastiques"))

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

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_checkup:
            if self.kilometrage_checkup > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_checkup
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)
