from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantLubrifiant,  TAUX_HORAIRE_CHOICES
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin
from django.core.exceptions import ValidationError




class NiveauxEtat(models.TextChoices):
    BON = "BON", _("OK")
    AJOUTER = "AJOUTER", _("Ajouté")

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


class HuileBoiteNiveauxEtat(models.TextChoices):
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

class LiquideFreinsQualite(models.TextChoices):
        DOT3 = 'DOT 3', _("DOT 3")
        DOT4 = 'DOT 4', _("DOT 4")
        DOT5 = 'DOT 5', _("DOT 5")
        DOT51 = 'DOT 5.1', _("DOT 5.1")



class LaveGlaceQualite(models.TextChoices):
    HIVER = 'HIVER', _("Hiver")
    ETE = 'ETE', _("Eté")


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

class Niveau(TechnicienMixin, models.Model):
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


    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="Niveaux",
        verbose_name=_("Niveaux"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="niveau_exemplaire",
        verbose_name="Kilomètres_niveaux",
        null=True, blank=True
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_niveaux = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment des niveaux"),

    )




    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile moteur"))
    moteur_niveau_huile_fabricant = models.CharField(max_length=30,choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR,verbose_name=_("Fabricant"))
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))
    moteur_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    moteur_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile de boite"))
    boite_niveau_huile_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteNiveauxEtat.choices,default=HuileBoiteNiveauxEtat.SEPTANTE_CINQ,verbose_name=_("Qualité d'huile"))
    boite_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    boite_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile de pont"))
    pont_niveau_huile_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ80,verbose_name=_("Qualité d'huile"))
    pont_niveau_huile_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité ajoutée en litres"),validators=[StepValueValidator(0.1)])
    pont_niveau_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))
    refroidissement_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1,  verbose_name=_("Quantité de liquide ajoutée en litres"),validators=[StepValueValidator(0.1)])
    refroidissement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité de liquide de freins"))
    frein_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,  verbose_name=_("Quantité de liquide ajoutée en litres"), validators=[StepValueValidator(0.1)])
    frein_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    lave_glace_liquide_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité de liquide de lave glace"))
    lave_glace_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    lave_glace_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))


    direction_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    direction_liquide_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices,default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    direction_liquide_qualite = models.CharField(max_length=25, choices=LiquideDirectionQualite.choices,default= LiquideDirectionQualite.CHF_7_1 ,verbose_name=_("Qualité de liquide de direction"))
    direction_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    direction_liquide_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))




    remarques = models.TextField(
        blank=True,
        verbose_name=_("Commentaire niveaux")
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

    date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="niveaux",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="niveaux_techs"
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
        related_name="niveaux_tech_societe"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )


    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe


    class Meta:
        verbose_name = _("Niveau")
        verbose_name_plural = _("Niveaux")


    def __str__(self):
        return f"Niveaux – {self.voiture_exemplaire} ({self.date:%Y-%m-%d})"

    def clean(self):
        super().clean()

        if not self.voiture_exemplaire_id or self.kilometrage_niveaux is None:
            return

        voiture = type(self.voiture_exemplaire).objects.get(
            pk=self.voiture_exemplaire_id
        )

        km_actuel = voiture.kilometres_chassis or 0

        if self.kilometrage_niveaux < km_actuel:
            raise ValidationError({
                "kilometrage_niveaux": _(
                    "Le kilométrage du contrôle niveaux (%(km_controle)s) "
                    "ne peut pas être inférieur au kilométrage actuel de la voiture (%(km_voiture)s)."
                ) % {
                                           "km_controle": self.kilometrage_niveaux,
                                           "km_voiture": km_actuel,
                                       }
            })

    def save(self, *args, **kwargs):
        # Validation AVANT modification du kilométrage voiture
        self.full_clean()

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = _("Niveaux") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # Sauvegarde du contrôle
        super().save(*args, **kwargs)

        # Mise à jour voiture APRÈS validation
        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if self.kilometrage_niveaux is not None:
                if self.kilometrage_niveaux > (voiture.kilometres_chassis or 0):
                    voiture.kilometres_chassis = self.kilometrage_niveaux
                    voiture.save(update_fields=["kilometres_chassis"])

            if self.kilometres_chassis != voiture.kilometres_chassis:
                self.kilometres_chassis = voiture.kilometres_chassis
                super().save(update_fields=["kilometres_chassis"])

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

    # -------------------------
        # CALCUL GENERIQUE
        # -------------------------

    def calcul_piece(self, prefix):

        prix = getattr(self, f"{prefix}_prix", Decimal("0"))
        quantite = getattr(self, f"{prefix}_quantite", 0)

        total = prix * quantite

        return {
            "prix": prix,
            "quantite": quantite,
            "total": total,
        }

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        produits = [
            {
                "prefix": "moteur_niveau_huile",
                "label": _("Huile moteur"),
            },
            {
                "prefix": "boite_niveau_huile",
                "label": _("Huile de boîte de vitesses"),
            },
            {
                "prefix": "pont_niveau_huile",
                "label": _("Huile de pont"),
            },
            {
                "prefix": "refroidissement",
                "label": _("Liquide de refroidissement"),
            },
            {
                "prefix": "frein_liquide",
                "label": _("Liquide de freins"),
            },
            {
                "prefix": "lave_glace_liquide",
                "label": _("Liquide de lave-glace"),
            },
            {
                "prefix": "direction_liquide",
                "label": _("Liquide de direction assistée"),
            },
        ]

        for produit in produits:
            prefix = produit["prefix"]

            etat_field = f"{prefix}_etat"
            quantite_field = f"{prefix}_quantite"
            qualite_field = f"{prefix}_qualite"
            fabricant_field = f"{prefix}_fabricant"
            prix_field = f"{prefix}_prix"

            etat = getattr(self, etat_field, None)

            # Ajouter au rapport lorsqu'un produit doit être
            # ajouté ou remplacé
            if etat not in [
                NiveauxEtat.AJOUTER,

            ]:
                continue

            prix = getattr(
                self,
                prix_field,
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            quantite = getattr(
                self,
                quantite_field,
                Decimal("0.00"),
            )

            if quantite is None:
                quantite = Decimal("0.00")

            quantite = Decimal(str(quantite))

            qualite = getattr(
                self,
                qualite_field,
                "",
            )

            fabricant = getattr(
                self,
                fabricant_field,
                "",
            )

            # Libellé traduit de l'état
            try:
                etat_label = getattr(
                    self,
                    f"get_{etat_field}_display",
                )()
            except (AttributeError, TypeError):
                etat_label = etat

            # Libellé traduit de la qualité
            try:
                qualite_label = getattr(
                    self,
                    f"get_{qualite_field}_display",
                )()
            except (AttributeError, TypeError):
                qualite_label = qualite

            # Libellé traduit du fabricant
            try:
                fabricant_label = getattr(
                    self,
                    f"get_{fabricant_field}_display",
                )()
            except (AttributeError, TypeError):
                fabricant_label = fabricant

            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": produit["label"],
                "code": prefix,

                # Valeur technique : AJOUTER, REMPLACE, FAIT...
                "etat": etat,

                # Libellé traduit affiché dans le PDF
                "etat_label": etat_label,

                # Valeur technique de la qualité
                "qualite": qualite,
                "qualite_label": qualite_label,

                # Valeur technique du fabricant
                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "prix": prix,
                "prix_unitaire": prix,
                "quantite": quantite,
                "total": total,
            })

        return {
            "lignes": rapport,
            "total_general": total_general,
        }