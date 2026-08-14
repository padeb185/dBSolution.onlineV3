from decimal import ROUND_HALF_UP, Decimal
from django.conf import settings
from django.core.validators import StepValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantLubrifiant, RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantEmbrayage, \
    FabricantJointSpi
from maintenance.entretien.models import LiquideFreinsQualite
from maintenance.models import Maintenance
from maintenance.services import sync_maintenance
from utils.mixin import TechnicienMixin





class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")




class Embrayage(TechnicienMixin, models.Model):
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

    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="embrayage",
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="embrayage",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name= _("Kilomètres chassis")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_embrayage = models.PositiveIntegerField(
        verbose_name= _("Kilométrage au moment du remplacement de l'embrayage ")
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE",
        verbose_name=_("Pays"),

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





    disque_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Disque d'embrayage"))
    disque_embrayage_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    disque_embrayage_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    disque_embrayage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    mecanisme_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Plateau de pression"))
    mecanisme_embrayage_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    mecanisme_embrayage_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    mecanisme_embrayage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    butee_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Butée d'embrayage"))
    butee_embrayage_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    butee_embrayage_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    butee_embrayage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    fourchette_embrayage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Fourchette d'embrayage"))
    fourchette_embrayage_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    fourchette_embrayage_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    fourchette_embrayage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    guide_butee = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Guide de la butée"))
    guide_butee_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    guide_butee_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    guide_butee_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    volant_moteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Volant moteur"))
    volant_moteur_fabricant = models.CharField(max_length=25, choices=FabricantEmbrayage.choices,default=FabricantEmbrayage.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    volant_moteur_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    volant_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    joint_spi_vilebrequin = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint spi vilebrequin"))
    joint_spi_vilebrequin_fabricant = models.CharField(max_length=25, choices=FabricantJointSpi.choices,default=FabricantJointSpi.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    joint_spi_vilebrequin_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    joint_spi_vilebrequin_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



    joint_spi_boite = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joint spi vilebrequin"))
    joint_spi_boite_fabricant = models.CharField(max_length=25, choices=FabricantJointSpi.choices, default=FabricantJointSpi.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    joint_spi_boite_quantite = models.PositiveIntegerField(default=0, verbose_name=_("Quantité"))
    joint_spi_boite_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat HTVA"))



    liquide_frein = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("État liquide de frein"))
    liquide_frein_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CASTROL,
        verbose_name=_("Fabricant du liquide de frein")
    )
    liquide_frein_specif = models.CharField(
        max_length=100, choices=LiquideFreinsQualite.choices,
        default=LiquideFreinsQualite.DOT4, blank=True,
        verbose_name=_("Spécification liquide de frein")
    )
    liquide_frein_quantite = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        null=True,
        blank=True,
        verbose_name=_("Quantité liquide de frein (L)"),
        validators=[StepValueValidator(0.1)],
    )

    liquide_frein_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat du liquide HTVA")
    )




    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,verbose_name=_("Serrage des roues"))

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

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="embrayage",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="embrayage"
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
        related_name="embrayage"
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
        verbose_name = _("Embrayage")
        verbose_name_plural = _("Embrayages")

    def __str__(self):
        return f"Remplacement embrayage - {self.voiture_exemplaire} {self.date}"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_embrayage is not None:
            if self.kilometrage_embrayage < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_embrayage': _(
                        f"Le kilométrage de l'embrayage ({self.kilometrage_embrayage}) "
                        f"ne peut pas être inférieur au kilométrage actuel de la voiture ({self.voiture_exemplaire.kilometres_chassis})."
                    )
                })

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

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # ----------------------------
        # CALCUL DES PIÈCES
        # ----------------------------
        self.calcul_piece("disque_embrayage")
        self.calcul_piece("mecanisme_embrayage")
        self.calcul_piece("butee_embrayage")
        self.calcul_piece("fourchette_embrayage")
        self.calcul_piece("guide_butee")
        self.calcul_piece("volant_moteur")
        self.calcul_piece("joint_spi_vilebrequin")
        self.calcul_piece("joint_spi_boite")
        self.calcul_piece("liquide_frein")



        # ----------------------------
        # TECHNICIEN AUTO
        # ----------------------------
        if not self.tech_technicien and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # ----------------------------
        # MAIN D'OEUVRE AUTO DESCRIPTIF
        # ----------------------------

        # ----------------------------
        # MAJ KILOMÉTRAGE
        # ----------------------------
        if self.voiture_exemplaire and self.kilometrage_abs:
            if self.kilometrage_embrayage > self.voiture_exemplaire.kilometres_chassis:
                self.voiture_exemplaire.kilometres_chassis = self.kilometrage_embrayage
                self.voiture_exemplaire.save(update_fields=["kilometres_chassis"])

        # copie locale
        if self.voiture_exemplaire:
            self.kilometres_chassis = self.voiture_exemplaire.kilometres_chassis

        # ----------------------------
        # SAVE ABS
        # ----------------------------
        super().save(*args, **kwargs)


        if self.main_oeuvre_id and self.voiture_exemplaire_id:

            task_name = f"{_('ABS')} {self.voiture_exemplaire} "

            if self.main_oeuvre.descriptif != task_name:
                self.main_oeuvre.descriptif = task_name
                self.main_oeuvre.save(update_fields=["descriptif"])

        # ----------------------------
        # SYNC MAINTENANCE
        # ----------------------------
        sync_maintenance(
            self,
            Maintenance.TypeMaintenance.ABS
        )
    # -------------------------
    # RAPPORT
    # -------------------------
    from decimal import Decimal

    def generer_rapport_remplacement(self):
        rapport = []
        total_pieces = Decimal("0.00")

        pieces = [
            "disque_embrayage",
            "mecanisme_embrayage",
            "butee_embrayage",
            "fourchette_embrayage",
            "guide_butee",
            "volant_moteur",
            "joint_spi_vilebrequin",
            "joint_spi_boite",
            "liquide_frein",
        ]

        for field_name in pieces:
            valeur = getattr(
                self,
                field_name,
                None,
            )

            # Pièces à remplacer ou déjà remplacées
            if valeur not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
            ]:
                continue

            # -------------------------
            # PRIX
            # -------------------------
            prix = getattr(
                self,
                f"{field_name}_prix",
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
                f"{field_name}_quantite",
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # -------------------------
            # FABRICANT
            # -------------------------
            fabricant = getattr(
                self,
                f"{field_name}_fabricant",
                None,
            )

            if fabricant:
                display_method = getattr(
                    self,
                    f"get_{field_name}_fabricant_display",
                    None,
                )

                if callable(display_method):
                    fabricant_label = display_method()
                else:
                    fabricant_label = fabricant
            else:
                fabricant_label = "-"

            # -------------------------
            # ÉTAT AFFICHÉ
            # -------------------------
            etat_display_method = getattr(
                self,
                f"get_{field_name}_display",
                None,
            )

            if callable(etat_display_method):
                etat_label = etat_display_method()
            else:
                etat_label = valeur

            # -------------------------
            # TOTAL
            # -------------------------
            total = prix * quantite
            total_pieces += total

            rapport.append({
                "champ": self._meta.get_field(
                    field_name
                ).verbose_name,

                "code": field_name,

                "etat": valeur,

                "etat_label": etat_label,

                "fabricant": fabricant_label,

                "prix": prix,

                "quantite": quantite,

                "total": total,
            })

        return {
            "lignes": rapport,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
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