import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.mixin import TechnicienMixin


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
    ATF_DSG = "ATF DSG", _("ATF DSG")

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




class Entretien(TechnicienMixin, models.Model):
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
        blank=True
    )

    kilometrage_entretien = models.PositiveIntegerField(
        _("Kilométrage au moment de l'entretien"),
        null=True,
        blank=True
    )






    moteur_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Vidange de l'huile moteur"))
    filtre_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacement du filtre à huile moteur"))
    moteur_bouchon_vidange =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le bouchon de vidange"))
    moteur_joint_vidange =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le joint du bouchon de vidange"))
    moteur_ajout_huile =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Ajout de la nouvelle huile moteur"))
    moteur_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    moteur_ajout_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))
    moteur_bougies =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer les bougies"))



    filtre_a_air =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre à air"))
    filtre_a_carburant =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre à carburant"))
    filtre_habitacle =  models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE, verbose_name=_("Remplacer le filtre d'habitacle"))

    boite_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de boite de vitesses"))
    filtre_huile_bte = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacement du filtre à huile de boite de vitesses"))
    boite_bouchon_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le bouchon de vidange"))
    boite_joint_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le joint du bouchon de vidange"))
    boite_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile moteur"))
    boite_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices, default=HuileEtat.ZERO_30,verbose_name=_("Qualité d'huile"))
    boite_ajout_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))

    pont_entretien_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile de boite de vitesses"))
    pont_bouchon_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices,default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le bouchon de vidange"))
    pont_joint_vidange = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Remplacer le joint du bouchon de vidange"))
    pont_ajout_huile = models.CharField(max_length=25, choices=EntretienEtat.choices, default=EntretienEtat.A_FAIRE,verbose_name=_("Vidange de l'huile moteur"))
    pont_ajout_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices,default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))
    pont_ajout_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"))

    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_quantite = models.FloatField(default=0,verbose_name=_("Quantité de liquide de lave glace ajoutée en litres"))
    lave_glace_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité de liquide de lave glace"))

    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_quantite = models.FloatField(default=0,verbose_name=_("Quantité de liquide de freins ajoutée en litres"))
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité de liquide de freins"))

    refroidissement_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_liquide_quantite = models.FloatField(default=0,verbose_name=_("Quantité de liquide de refroidissement ajouté en litres"))
    refroidissement_liquide_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))

    liquide_direction_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de direction"))
    liquide_direction_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de direction ajouté en litres"))
    liquide_direction_qualite = models.CharField(max_length=25, choices=LiquideDirectionQualite.choices,default=LiquideDirectionQualite.UNIVERSAL_PSF,verbose_name=_("Qualité de liquide de direction"))

    pneu_pression_bar_avd = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant droit en bar"))
    pneu_pression_bar_avg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu avant gauche en bar"))
    pneu_pression_bar_ard = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière droit en bar"))
    pneu_pression_bar_arg = models.FloatField(default=2.4, verbose_name=_("Pression du pneu arrière gauche en bar"))


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

    # --- Date d'enregistrement ---
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))


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
        return _("Entretien – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_entretien is not None:
            if self.kilometrage_entretien < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_checkup': _(
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

        super().save(*args, **kwargs)

