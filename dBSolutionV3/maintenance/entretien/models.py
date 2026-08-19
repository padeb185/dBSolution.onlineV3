import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.check_up.models import PhareEtat
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantLubrifiant, FabricantFiltre, \
    AmpouleAutomobile, FabricantPiece, TypeHuileDirection, FabricantBougies
from utils.mixin import TechnicienMixin
from societe.models import Societe




def validate_step_0_1(value):
    if round(value * 10) != value * 10:
        raise ValidationError("La valeur doit être un multiple de 0.1")


class EntretienEtat(models.TextChoices):
    A_FAIRE = "A_FAIRE", _("A faire")
    FAIT = "FAIT", _("Fait")
    REPORTER = "REPORTER", _("Reporter")



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

class LaveGlaceQualite(models.TextChoices):
    HIVER = 'HIVER', _("Hiver")
    ETE = 'ETE', _("Eté")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("Bon")
    AJOUTER = "AJOUTER", _("Ajouter")
    REMPLACER = "REMPLACER", _("Remplacé")

class LiquideFreinsQualite(models.TextChoices):
    DOT3 = 'DOT 3', _("DOT 3")
    DOT4 = 'DOT 4', _("DOT 4")
    DOT5 = 'DOT 5', _("DOT 5")
    DOT51 = 'DOT 5.1', _("DOT 5.1")


class LiquideDirectionQualite(models.TextChoices):

    # Hydraulique direction assistée (Pentosin / CHF)
    CHF_7_1 = "CHF_7_1", _("CHF 7.1")
    CHF_11S = "CHF_11S", _("CHF 11S")
    CHF_202 = "CHF_202", _("CHF 202")
    CHF_1_PLUS = "CHF_1_PLUS", _("CHF 1+")
    CHF_LIFEGUARD = "CHF_LIFEGUARD", _("CHF Lifeguard Fluid")

    # --- Porsche spécifiques (très important : base CHF) ---
    PORSCHE_CHF_11S = "PORSCHE_CHF_11S", _("Porsche / Pentosin CHF 11S (direction assistée)")
    PORSCHE_CHF_202 = "PORSCHE_CHF_202", _("Porsche / Pentosin CHF 202 (hydraulique moderne)")
    PORSCHE_ATF_D3 = "PORSCHE_ATF_D3", _("Porsche ATF Dexron III (anciens modèles)")

    # --- BMW spécifiques (très important) ---
    BMW_CHF_11S = "BMW_CHF_11S", _("BMW / Pentosin CHF 11S (direction assistée)")
    BMW_CHF_202 = "BMW_CHF_202", _("BMW / Pentosin CHF 202 (direction assistée moderne)")
    BMW_CHF_7_1 = "BMW_CHF_7_1", _("BMW CHF 7.1 (anciens systèmes hydrauliques)")
    BMW_ATF_D3 = "BMW_ATF_D3", _("BMW ATF Dexron III (anciens modèles direction assistée)")

    # Fluides spécifiques Renault / ELF
    RENAULT_MATIC_D2 = "RENAULT_MATIC_D2", _("Renaultmatic D2 (ELF)")
    RENAULT_MATIC_D3_SYN = "RENAULT_MATIC_D3_SYN", _("Renaultmatic D3 SYN (ELF)")
    ELF_MATIC_G3 = "ELF_MATIC_G3", _("ELF Matic G3")

    # --- Renault spécifiques (atelier / OEM) ---
    RENAULT_PSF_D3 = "RENAULT_PSF_D3", _("Renault PSF Dexron III (direction assistée hydraulique)")
    RENAULT_ELF_PSF = "RENAULT_ELF_PSF", _("Renault / ELF liquide direction assistée")

    # Autres constructeurs
    PSF_HYUNDAI_KIA = "PSF_HYUNDAI_KIA", _("PSF Hyundai / Kia")
    PSF_TOYOTA = "PSF_TOYOTA", _("PSF Toyota")
    PSF_HONDA = "PSF_HONDA", _("PSF Honda")

    # Universel
    UNIVERSAL_PSF = "UNIVERSAL_PSF", _("Liquide direction assistée universel")


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


class HuilePontEtat(models.TextChoices):
    SEPTANTE_CINQ80 = "75W80", _("75W80")
    SEPTANTE_CINQ85 = "75W85", _("75W85")
    SEPTANTE_CINQ90 = "75W90", _("75W90")
    SEPTANTE_CINQ110 = "75W110", _("75W110")
    SEPTANTE_CINQ140 = "75W140", _("75W140")

    QUATRE_VINGT90 = "80W90", _("80W90")
    QUATRE_VINGT140 = "80W140", _("80W140")

    QUATRE_VINGT_CINQ90 = "85W90", _("85W90")
    QUATRE_VINGT_CINQ140 = "85W140", _("85W140")

    SAE90 = "SAE90", _("SAE 90")
    SAE140 = "SAE140", _("SAE 140")

    PORSCHE_75W90 = "PORSCHE_75W90", _("Porsche 75W90")
    PORSCHE_75W140 = "PORSCHE_75W140", _("Porsche 75W140")

    AUTRE = "AUTRE", _("Autre")
    INCONNUE = "INCONNUE", _("Huile inconnue")




class Entretien(TechnicienMixin, models.Model):
    # -------------------------
    # CONFIG TVA
    # -------------------------
    PAYS_CHOICES = [
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DE', _("Allemagne")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('ES', _("Espagne")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('GR', _("Grèce")),
        ('HR', _("Croatie")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('LV', _("Lettonie")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SE', _("Suède")),
        ('SI', _("Slovénie")),
        ('SK', _("Slovaquie")),
    ]

    TVA_PIECES = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'CY': 19,
        'CZ': 21,
        'DE': 19,
        'DK': 25,
        'EE': 24,
        'ES': 21,
        'FI': 25.5,
        'FR': 20,
        'GR': 24,
        'HR': 25,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LT': 21,
        'LU': 17,
        'LV': 21,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SE': 25,
        'SI': 22,
        'SK': 23,
    }
    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="entretien",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="entretiens",
        null = True, blank = True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_entretien = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment de l'entretien"),
    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )




    moteur_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))
    moteur_bouchon_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le bouchon de vidange"),
    )
    moteur_bouchon_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.AUTRE,
        verbose_name=_("Fabricant"),
    )
    moteur_bouchon_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    moteur_bouchon_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    moteur_joint_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le joint du bouchon de vidange"),
    )
    moteur_joint_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    moteur_joint_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    moteur_joint_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    moteur_ajout_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Ajout de la nouvelle huile moteur"))
    moteur_ajout_huile_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    moteur_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    moteur_ajout_huile_quantite =  models.DecimalField(default=0.0, decimal_places=2,  max_digits=4,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_ajout_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    filtre_huile = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacement du filtre à huile moteur"),
    )
    filtre_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_huile_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_a_air = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à air"),
    )
    filtre_a_air_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_a_air_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_a_air_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_a_carburant = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à carburant"),
    )
    filtre_a_carburant_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_a_carburant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),

    )
    filtre_a_carburant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    filtre_habitacle = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre d'habitacle"),
    )
    filtre_habitacle_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    filtre_habitacle_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    filtre_habitacle_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    filtre_huile_boite = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le filtre à huile de boîte de vitesses"),
    )

    filtre_huile_boite_fabricant = models.CharField(
        max_length=25,
        choices=FabricantFiltre.choices,
        default=FabricantFiltre.CHOISIR,
        verbose_name=_("Fabricant"),
    )

    filtre_huile_boite_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )

    filtre_huile_boite_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    bougies = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer les bougies"),
    )
    bougies_fabricant = models.CharField(
        max_length=25,
        choices=FabricantBougies.choices,
        default=FabricantBougies.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    bougies_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    bougies_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA des bougies"),
    )


    boite_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de boite de vitesses"))
    boite_bouchon_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le bouchon de vidange"),
    )
    boite_bouchon_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    boite_bouchon_vidange_quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité"),
    )
    boite_bouchon_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    boite_joint_vidange = models.CharField(
        max_length=25,
        choices=EntretienEtat.choices,
        default=EntretienEtat.A_FAIRE,
        verbose_name=_("Remplacer le joint du bouchon de vidange"),
    )
    boite_joint_vidange_fabricant = models.CharField(
        max_length=25,
        choices=FabricantPiece.choices,
        default=FabricantPiece.AUTRE,
        verbose_name=_("Fabricant"),
    )
    boite_joint_vidange_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    boite_joint_vidange_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
    boite_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile moteur"))
    boite_ajout_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.MOBIL,
        verbose_name=_("Fabricant"),
    )
    boite_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    boite_ajout_huile_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_ajout_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    pont_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de pont"))
    pont_bouchon_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le bouchon de vidange"))
    pont_joint_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le joint du bouchon de vidange"))
    pont_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Ajout de la nouvelle huile de pont"))
    pont_ajout_huile_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    pont_ajout_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ80, verbose_name=_("Qualité d'huile de pont"))
    pont_ajout_huile_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    pont_ajout_huile_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    lave_glace_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    lave_glace_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité"))
    lave_glace_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Fabricant"))
    frein_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité"))
    frein_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )



    refroidissement_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_liquide_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.MOBIL,verbose_name=_("Nom du fabricant"))
    refroidissement_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    refroidissement_liquide_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité"))
    refroidissement_liquide_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )


    liquide_direction_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    liquide_direction_fabricant = models.CharField(max_length=25, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.MOBIL,verbose_name=_("Nom du fabricant"))
    liquide_direction_quantite =  models.DecimalField(default=0.0,  max_digits=4, decimal_places=2,  validators=[StepValueValidator(0.1)], verbose_name=_("Quantité ajoutée en litres"))
    liquide_direction_qualite = models.CharField(max_length=25, choices=TypeHuileDirection.choices,default=TypeHuileDirection.CHOISIR,verbose_name=_("Qualité"))
    liquide_direction_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )
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

    pneu_pression_bar_avd = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu avant droit en bar"),
    )

    pneu_pression_bar_avg = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu avant gauche en bar"),
    )

    pneu_pression_bar_ard = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu arrière droit en bar"),
    )

    pneu_pression_bar_arg = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.4,
        validators=[StepValueValidator(Decimal("0.1"))],
        verbose_name=_("Pression du pneu arrière gauche en bar"),

    )
    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE, verbose_name=_("Serrage des roues"))

    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretien_piece"
    )

    quantite = models.FloatField(null=True, blank=True)



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
        related_name="controle_techs_entretien"
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
        related_name="controle_tech_societe_entretien"
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

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entretiens",
        verbose_name=_("Main d'oeuvre")
    )


    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)



    def doit_alerter(self, km_actuel):
        return (
                not self.termine
                and km_actuel >= self.kilometrage_prevu - self.alerte_avant_km
        )


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    class Meta:
        verbose_name = _("Entretien")
        verbose_name_plural = _("entretiens")

    def __str__(self):
        return _("Entretien – Maintenance %(id)s") % {"id": self.entretien.id} % f"{self.utilisateur.prenom} {self.utilisateur.nom} - {self.cout_total} €"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_entretien is not None:
            if self.kilometrage_entretien < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_entretien': _(
                        f"Le kilométrage de l'entretien ({self.kilometrage_entretien}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometrage_entretien:
            if self.kilometrage_entretien > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_entretien
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # Toujours garder une copie dans le contrôle
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, '_user'):
            self.assign_technicien(self._user)

            # ----------------------------
            # MAIN D'OEUVRE AUTO DESCRIPTIF
            # ----------------------------
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Entretien") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        super().save(*args, **kwargs)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # --------------------------------------------------
            # On traite uniquement les champs terminant par _prix
            # --------------------------------------------------
            if not field_name.endswith("_prix"):
                continue

            # Exemple :
            # liquide_direction_prix
            # -> liquide_direction
            champ_base = field_name.removesuffix("_prix")

            champ_quantite = f"{champ_base}_quantite"

            # Le champ quantité doit exister
            if not hasattr(self, champ_quantite):
                continue

            # --------------------------------------------------
            # Prix / quantité
            # --------------------------------------------------
            prix = getattr(self, field_name, None)
            quantite = getattr(self, champ_quantite, None)

            prix = Decimal(str(prix or 0))
            quantite = Decimal(str(quantite or 0))

            # Ne pas afficher les lignes sans prix ou quantité
            if prix <= 0 or quantite <= 0:
                continue

            prix = prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            # --------------------------------------------------
            # ÉTAT
            # --------------------------------------------------

            # Priorité à :
            # liquide_direction_etat
            champ_etat = f"{champ_base}_etat"

            if hasattr(self, champ_etat):
                etat = getattr(self, champ_etat, "")

                methode_etat_display = getattr(
                    self,
                    f"get_{champ_etat}_display",
                    None,
                )

            # Sinon ancien fonctionnement :
            # ex. balais_essuie_avant
            elif hasattr(self, champ_base):
                etat = getattr(self, champ_base, "")

                methode_etat_display = getattr(
                    self,
                    f"get_{champ_base}_display",
                    None,
                )

            else:
                etat = ""
                methode_etat_display = None

            if callable(methode_etat_display):
                etat_label = methode_etat_display()
            else:
                etat_label = etat or "-"

            # --------------------------------------------------
            # FABRICANT
            # --------------------------------------------------
            champ_fabricant = f"{champ_base}_fabricant"

            fabricant = getattr(
                self,
                champ_fabricant,
                "",
            )

            methode_fabricant_display = getattr(
                self,
                f"get_{champ_fabricant}_display",
                None,
            )

            if callable(methode_fabricant_display):
                fabricant_label = methode_fabricant_display()
            else:
                fabricant_label = fabricant or "-"

            # --------------------------------------------------
            # QUALITÉ
            # --------------------------------------------------
            champ_qualite = f"{champ_base}_qualite"

            qualite = getattr(
                self,
                champ_qualite,
                "",
            )

            methode_qualite_display = getattr(
                self,
                f"get_{champ_qualite}_display",
                None,
            )

            if callable(methode_qualite_display):
                qualite_label = methode_qualite_display()
            else:
                qualite_label = qualite or "-"

            # --------------------------------------------------
            # TYPE
            # --------------------------------------------------
            champ_type = f"{champ_base}_type"

            type_piece = getattr(
                self,
                champ_type,
                "",
            )

            methode_type_display = getattr(
                self,
                f"get_{champ_type}_display",
                None,
            )

            if callable(methode_type_display):
                type_label = methode_type_display()
            else:
                type_label = type_piece or "-"

            # --------------------------------------------------
            # LIBELLÉ
            # --------------------------------------------------

            # On essaie d'abord le champ d'état
            try:
                if hasattr(self, champ_etat):
                    champ_model = self._meta.get_field(champ_etat)
                    libelle = champ_model.verbose_name

                else:
                    champ_model = self._meta.get_field(champ_base)
                    libelle = champ_model.verbose_name

            except Exception:
                libelle = champ_base.replace("_", " ").capitalize()

            # --------------------------------------------------
            # RAPPORT
            # --------------------------------------------------
            rapport.append({
                "champ": libelle,
                "nom": libelle,
                "code": champ_base,

                "etat": etat,
                "etat_label": etat_label,

                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "qualite": qualite,
                "qualite_label": qualite_label,

                "type": type_piece,
                "type_label": type_label,

                "quantite": quantite,
                "prix": prix,
                "prix_unitaire": prix,
                "total": total,
            })

            total_general += total

        return {
            "lignes": rapport,
            "pieces": rapport,
            "total_general": total_general.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            ),
        }

    @property
    def utilisateur_main_oeuvre(self):
        if self.main_oeuvre:
            return self.main_oeuvre.utilisateur
        return None

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
            return Decimal(str(self.main_oeuvre.taux_horaire))

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


    @property
    def nom_travailleur(self):
        if self.main_oeuvre:
            return str(self.main_oeuvre.utilisateur)
        return ""