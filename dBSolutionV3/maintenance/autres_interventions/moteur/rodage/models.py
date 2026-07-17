import uuid
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.check_up.models import PhareEtat
from maintenance.choices import RouesSerrageEtat
from utils.mixin import TechnicienMixin
from societe.models import Societe




def validate_step_0_1(value):
    if round(value * 10) != value * 10:
        raise ValidationError("La valeur doit être un multiple de 0.1")


class RodageEtat(models.TextChoices):
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

class LaveGlaceQualite(models.TextChoices):
    HIVER = 'HIVER', _("Hiver")
    ETE = 'ETE', _("Eté")


class NiveauxEtat(models.TextChoices):
    BON = "BON", _("Bon")
    AJOUTER = "AJOUTER", _("Ajouter")
    REMPLACER = "REMPLACER", _("Remplacer")

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
    PORSCHE_75W90 = "75W90", _("Porsche 75W90")
    SEPTANTE_CINQ140 = "75W140", _("75W140")



class Rodage(TechnicienMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    maintenance = models.ForeignKey(
        "maintenance.Maintenance",
        on_delete=models.CASCADE,
        related_name="rodage",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="rodage",
        null = True, blank = True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_rodage = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du rodage"),
    )

    societe = models.ForeignKey(
        Societe,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )




    moteur_rodage_vidange = models.CharField(max_length=25, choices=RodageEtat.choices, default=RodageEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))

    moteur_filtre_huile =  models.CharField(max_length=25, choices=RodageEtat.choices, default=RodageEtat.A_FAIRE, verbose_name=_("Remplacement du filtre à huile moteur"))
    moteur_filtre_huile_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    moteur_filtre_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    moteur_bouchon_vidange =  models.CharField(max_length=25, choices=RodageEtat.choices, default=RodageEtat.A_FAIRE, verbose_name=_("Remplacer le bouchon de vidange"))
    moteur_bouchon_vidange_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    moteur_bouchon_vidange_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))


    moteur_joint_vidange =  models.CharField(max_length=25, choices=RodageEtat.choices, default=RodageEtat.A_FAIRE, verbose_name=_("Remplacer le joint du bouchon de vidange"))
    moteur_joint_vidange_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    moteur_joint_vidange_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    moteur_ajout_huile =  models.CharField(max_length=25, choices=RodageEtat.choices, default=RodageEtat.A_FAIRE, verbose_name=_("Ajout de la nouvelle huile moteur"))
    moteur_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    moteur_ajout_huile_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    moteur_ajout_huile_quantite =  models.DecimalField(default=0.0, decimal_places=2,  max_digits=4,  verbose_name=_("Quantité d'huile moteur ajoutée en litres"), validators=[StepValueValidator(0.1)])



    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2, verbose_name=_("Quantité de liquide de lave glace ajoutée en litres"),validators=[StepValueValidator(0.1)])
    lave_glace_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    lave_glace_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité de liquide de lave glace"))

    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=2, verbose_name=_("Quantité de liquide de freins ajoutée en litres"), validators=[StepValueValidator(0.1)])
    frein_liquide_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité de liquide de freins"))

    refroidissement_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_liquide_quantite =  models.DecimalField(default=0.0, max_digits=4,  decimal_places=2, verbose_name=_("Quantité de liquide de refroidissement ajouté en litres"), validators=[StepValueValidator(0.1)])
    refroidissement_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2,verbose_name=_("Prix d'achat HTVA"))
    refroidissement_liquide_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))

    liquide_direction_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    liquide_direction_quantite =  models.DecimalField(default=0.0,  max_digits=4, decimal_places=2, verbose_name=_("Quantité de liquide de direction ajouté en litres"), validators=[StepValueValidator(0.1)])
    liquide_direction_prix = models.DecimalField(default=0.0, max_digits=4, decimal_places=2, verbose_name=_("Prix d'achat HTVA"))
    liquide_direction_qualite = models.CharField(max_length=25, choices=LiquideDirectionQualite.choices,default=LiquideDirectionQualite.UNIVERSAL_PSF,verbose_name=_("Qualité de liquide de direction"))

    # phares#

    phares_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de route"))
    phares_gros_phares = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Grand phares"))
    phares_clignotants = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Clignotants"))
    phares_recul = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de recul"))
    phares_anti_brouillard_avant = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Phares anti-brouillard avant"))
    phares_anti_brouillard_arriere = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Phares anti-brouillard arrière"))
    phares_feux_stops = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux stop"))
    phares_troisieme_feux_stop = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Troisième feux stop"))
    phares_feux_position_av = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de position avant"))
    phares_feux_position_ar = models.CharField(max_length=25, choices=PhareEtat.choices, default=PhareEtat.OK,verbose_name=_("Feux de position arrière"))


    pneu_pression_bar_avd = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant droit en bar"), validators=[StepValueValidator(0.1)])
    pneu_pression_bar_avg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant gauche en bar"), validators=[StepValueValidator(0.1)])
    pneu_pression_bar_ard = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière droit en bar"), validators=[StepValueValidator(0.1)])
    pneu_pression_bar_arg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière gauche en bar"), validators=[StepValueValidator(0.1)])

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE, verbose_name=_("Serrage des roues"))

    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rodage_piece"
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
        related_name="rodage"
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
        related_name="rodage_societe"
    )

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rodage",
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
        verbose_name = _("Rodage")
        verbose_name_plural = _("Rodages")

    def __str__(self):
        return _("rodage – Maintenance %(id)s") % {"id": self.rodage.id} % f"{self.utilisateur.prenom} {self.utilisateur.nom} - {self.cout_total} €"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometres_rodage is not None:
            if self.kilometres_rodage < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_rodage': _(
                        f"Le kilométrage du rodage ({self.kilometres_rodage}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        # Si checkup > km actuel, mettre à jour la voiture
        if self.voiture_exemplaire and self.kilometres_rodage:
            if self.kilometres_rodage > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometres_rodage
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


    @property
    def utilisateur_main_oeuvre(self):
        if self.main_oeuvre:
            return self.main_oeuvre.utilisateur
        return None

    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"

        temps_minutes = self.main_oeuvre.temps_minutes or 0

        heures = temps_minutes // 60
        minutes = temps_minutes % 60

        return f"{heures}h{minutes:02d}"

    @property
    def taux_horaire_main_oeuvre(self):
        if self.main_oeuvre:
            return self.main_oeuvre.taux_horaire
        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if self.main_oeuvre:
            return self.main_oeuvre.cout_total
        return Decimal("0.00")

    @property
    def nom_travailleur(self):
        if self.main_oeuvre:
            return str(self.main_oeuvre.utilisateur)
        return ""



    def calcul_piece(self, prefix):
        prix = getattr(self, f"{prefix}_prix", 0)
        quantite = getattr(self, f"{prefix}_quantite", 0)

        if not prix or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        prix_htva = prix  # pas de marge dans ton modèle

        prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        prix_ttc = prix_htva + tva

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)
        setattr(self, f"{prefix}_tva_vente", tva)
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        elements = [
            {
                "code": "moteur_filtre_huile",
                "label": _("Filtre à huile moteur"),
                "etat_field": "moteur_filtre_huile",
                "prix_field": "moteur_filtre_huile_prix",
                "quantite_field": "moteur_filtre_huile_quantite",
                "choices": RodageEtat.choices,
            },
            {
                "code": "moteur_bouchon_vidange",
                "label": _("Bouchon de vidange"),
                "etat_field": "moteur_bouchon_vidange",
                "prix_field": "moteur_bouchon_vidange_prix",
                "quantite_field": "moteur_bouchon_vidange_quantite",
                "choices": RodageEtat.choices,
            },
            {
                "code": "moteur_joint_vidange",
                "label": _("Joint du bouchon de vidange"),
                "etat_field": "moteur_joint_vidange",
                "prix_field": "moteur_joint_vidange_prix",
                "quantite_field": "moteur_joint_vidange_quantite",
                "choices": RodageEtat.choices,
            },
            {
                "code": "moteur_ajout_huile",
                "label": _("Huile moteur"),
                "etat_field": "moteur_ajout_huile",
                "prix_field": "moteur_ajout_huile_prix",
                "quantite_field": "moteur_ajout_huile_quantite",
                "choices": RodageEtat.choices,
            },
            {
                "code": "lave_glace",
                "label": _("Liquide de lave-glace"),
                "etat_field": "lave_glace_liquide_etat",
                "prix_field": "lave_glace_prix",
                "quantite_field": "lave_glace_quantite",
                "choices": NiveauxEtat.choices,
            },
            {
                "code": "frein_liquide",
                "label": _("Liquide de freins"),
                "etat_field": "frein_liquide_etat",
                "prix_field": "frein_liquide_prix",
                "quantite_field": "frein_liquide_quantite",
                "choices": NiveauxEtat.choices,
            },
            {
                "code": "refroidissement_liquide",
                "label": _("Liquide de refroidissement"),
                "etat_field": "refroidissement_liquide_etat",
                "prix_field": "refroidissement_prix",
                "quantite_field": "refroidissement_liquide_quantite",
                "choices": NiveauxEtat.choices,
            },
            {
                "code": "liquide_direction",
                "label": _("Liquide de direction"),
                "etat_field": "liquide_direction_etat",
                "prix_field": "liquide_direction_prix",
                "quantite_field": "liquide_direction_quantite",
                "choices": NiveauxEtat.choices,
            },
        ]

        for element in elements:
            etat = getattr(self, element["etat_field"], None)

            prix_brut = getattr(
                self,
                element["prix_field"],
                Decimal("0.00"),
            )

            quantite_brute = getattr(
                self,
                element["quantite_field"],
                Decimal("0.00"),
            )

            prix = Decimal(str(prix_brut or 0))
            quantite = Decimal(str(quantite_brute or 0))

            # Ne pas ajouter une ligne totalement vide
            if prix <= 0 and quantite <= 0:
                continue

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            rapport.append({
                "champ": element["label"],
                "code": element["code"],
                "etat": etat,
                "etat_label": dict(
                    element["choices"]
                ).get(etat, etat or "-"),
                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

        total_general = total_general.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        return {
            "lignes": rapport,
            "total_general": total_general,
        }