from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from piece.piece_fluides.models import InventaireFluide
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin
from django.core.exceptions import ValidationError

def validate_step_0_1(value):
    if round(value * 10) != value * 10:
        raise ValidationError("La valeur doit être un multiple de 0.1")

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



class Niveau(TechnicienMixin, models.Model):
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
        blank=True
    )

    kilometrage_niveaux = models.PositiveIntegerField(
        _("Kilométrage au moment des niveaux"),
        null=True,
        blank=True
    )


    moteur_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    moteur_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"), validators=[validate_step_0_1])
    moteur_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.ZERO_30, verbose_name=_("Qualité d'huile"))

    boite_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    boite_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"), validators=[validate_step_0_1])
    boite_niveau_huile_qualite = models.CharField(max_length=25, choices=HuileBoiteEtat.choices,default=HuileBoiteEtat.SEPTANTE_CINQ,verbose_name=_("Qualité d'huile"))

    pont_niveau_huile_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau d'huile"))
    pont_niveau_huile_quantite = models.FloatField(default=0, verbose_name=_("Quantité d'huile ajoutée en litres"),validators=[validate_step_0_1])
    pont_niveau_huile_qualite = models.CharField(max_length=25, choices=HuilePontEtat.choices,default=HuilePontEtat.SEPTANTE_CINQ140,verbose_name=_("Qualité d'huile"))

    refroidissement_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de refroidissement"))
    refroidissement_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de refroidissement ajoutée en litres"),validators=[validate_step_0_1])
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices,default=RefroidissementQualiteEtat.G13,verbose_name=_("Qualité de liquide de refroidissement"))

    frein_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de freins"))
    frein_liquide_quantite = models.FloatField(default=0, verbose_name=_("Quantité de liquide de freins ajoutée en litres"), validators=[validate_step_0_1] )
    frein_liquide_qualite = models.CharField(max_length=25, choices=LiquideFreinsQualite.choices,default=LiquideFreinsQualite.DOT4,verbose_name=_("Qualité de liquide de freins"))

    lave_glace_liquide_etat = models.CharField(max_length=25, choices=NiveauxEtat.choices, default=NiveauxEtat.BON,verbose_name=_("Niveau de liquide de lave-glace"))
    lave_glace_quantite = models.FloatField(default=0,verbose_name=_("Quantité de liquide de lave glace ajoutée en litres"), validators=[validate_step_0_1])
    lave_glace_qualite = models.CharField(max_length=25, choices=LaveGlaceQualite.choices,default=LaveGlaceQualite.HIVER,verbose_name=_("Qualité de liquide de lave glace"))

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

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)



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
        # Vérification que le kilométrage du check-up n'est pas inférieur au kilométrage actuel de la voiture
        if self.voiture_exemplaire and self.kilometrage_niveaux is not None:
            if self.kilometrage_niveaux < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_niveaux': _(
                        f"Le kilométrage du check-up ({self.kilometrage_niveaux}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()  # valide les km avant sauvegarde

        if self.voiture_exemplaire:
            if self.kilometrage_niveaux is not None:
                # Si l'utilisateur a saisi un km
                if self.kilometrage_niveaux > self.voiture_exemplaire.kilometres_chassis:
                    self.voiture_exemplaire.kilometres_chassis = self.kilometrage_niveaux
                    self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])
                # Toujours copier dans le Niveau
                self.kilometres_chassis = max(self.kilometrage_niveaux, self.voiture_exemplaire.kilometres_chassis)
            else:
                # Si non saisi, prendre le km actuel de la voiture
                self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        super().save(*args, **kwargs)

