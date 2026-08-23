from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import RouesSerrageEtat, FabricantLubrifiant, FabricantPiece
from maintenance.entretien.models import LiquideFreinsQualite
from utils.mixin import TechnicienMixin
from maintenance.services import sync_maintenance
from maintenance.models import Maintenance





class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class Abs(TechnicienMixin, models.Model):
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
        related_name="abs",
        null=True,
        blank=True
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="abs",
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
    kilometrage_abs = models.PositiveIntegerField(
        verbose_name= _("Kilométrage au moment du controle ABS ")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    pays = models.CharField(
        max_length=5,
        choices=PAYS_CHOICES,
        default="BE"
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



    pompe_abs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Pompe d'ABS"))
    pompe_abs_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    pompe_abs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pompe_abs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva de la pompe ABS"))


    calculateur_abs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calculateur d'ABS"))
    calculateur_abs_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    calculateur_abs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    calculateur_abs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix d'achat htva du calculateur d'ABS"))


    capteur_abs_avd = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS avant droit"))
    capteur_abs_avd_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteur_abs_avd_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_abs_avd_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix capteur ABS avant droit"))


    capteur_abs_avg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS avant gauche"))
    capteur_abs_avg_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    capteur_abs_avg_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_abs_avg_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix capteur ABS avant gauche"))


    capteur_abs_ard = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS arrière droit"))
    capteur_abs_ard_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    capteur_abs_ard_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_abs_ard_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix capteur ABS arrière droit"))


    capteur_abs_arg = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur ABS arrière gauche"))
    capteur_abs_arg_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    capteur_abs_arg_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_abs_arg_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_("Prix capteur ABS arrière gauche"))




    liquide_frein_etat = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,
                                          verbose_name=_("État liquide de frein"))
    liquide_frein_fabricant = models.CharField(
        max_length=25,
        choices=FabricantLubrifiant.choices,
        default=FabricantLubrifiant.CASTROL,
        verbose_name=_("Fabricant du liquide de frein")
    )
    liquide_frein_specif = models.CharField(max_length=100, choices=LiquideFreinsQualite.choices,
                                            default=LiquideFreinsQualite.DOT4, blank=True,
                                            verbose_name=_("Spécification liquide de frein"))
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
        related_name="abs",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="abs"
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
        related_name="abs"
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
        verbose_name = _("Système ABS")
        verbose_name_plural = _("Systèmes ABS")

    def __str__(self):
        return f"Controle abs - {self.voiture_exemplaire} {self.date}"

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_abs is not None:
            if self.kilometrage_abs < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_système_abs': _(
                        f"Le kilométrage du système ABS ({self.kilometrage_abs}) "
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
        self.calcul_piece("pompe_abs")
        self.calcul_piece("calculateur_abs")
        self.calcul_piece("capteur_abs_avd")
        self.calcul_piece("capteur_abs_avg")
        self.calcul_piece("capteur_abs_ard")
        self.calcul_piece("capteur_abs_arg")


        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = (
                    _("Controle du système ABS")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(
                update_fields=["descriptif"]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.ABS
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                ]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # =========================
        if self.voiture_exemplaire_id:

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            ancien_kilometrage = (
                    voiture.kilometres_chassis or 0
            )

            # Snapshot du kilométrage avant intervention
            self.kilometres_chassis = ancien_kilometrage

            # =========================
            # CALCUL VARIATION
            # =========================
            if self.kilometrage_abs is not None:

                self.kilometrage_variation = (
                        self.kilometrage_abs
                        - ancien_kilometrage
                )

            else:
                self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE NETTOYAGE EXTÉRIEUR
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if (
                self.voiture_exemplaire_id
                and self.kilometrage_abs is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_abs
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_abs
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

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
    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        etats_acceptes = {
            EtatOKNotOK.NOT_OK,
            EtatOKNotOK.REMPLACE,
        }

        labels_etats = dict(EtatOKNotOK.choices)

        for field in self._meta.fields:
            field_name = field.name

            # Traiter uniquement les champs d'état EtatOKNotOK
            if not (
                    isinstance(field, models.CharField)
                    and field.choices == EtatOKNotOK.choices
            ):
                continue

            valeur = getattr(self, field_name, None)

            # Uniquement les éléments à remplacer ou remplacés
            if valeur not in etats_acceptes:
                continue

            # Exemple :
            # liquide_frein_etat -> liquide_frein
            champ_base = (
                field_name.removesuffix("_etat")
                if field_name.endswith("_etat")
                else field_name
            )

            # ============================
            # QUANTITÉ
            # ============================
            quantite = getattr(
                self,
                f"{champ_base}_quantite",
                Decimal("0.00"),
            )

            quantite = Decimal(str(quantite or "0.00"))

            # Ne prendre en compte que les quantités supérieures à zéro
            if quantite <= 0:
                continue

            # ============================
            # PRIX UNITAIRE
            # ============================
            prix = getattr(
                self,
                f"{champ_base}_prix",
                Decimal("0.00"),
            )

            prix = Decimal(str(prix or "0.00"))

            # ============================
            # FABRICANT
            # ============================
            nom_champ_fabricant = f"{champ_base}_fabricant"

            fabricant = getattr(
                self,
                nom_champ_fabricant,
                None,
            )

            methode_fabricant_display = getattr(
                self,
                f"get_{nom_champ_fabricant}_display",
                None,
            )

            if callable(methode_fabricant_display):
                fabricant = methode_fabricant_display()

            fabricant = fabricant or "-"

            # ============================
            # SPÉCIFICATION / QUALITÉ
            # ============================
            nom_champ_specification = f"{champ_base}_specif"

            specification = getattr(
                self,
                nom_champ_specification,
                None,
            )

            methode_specification_display = getattr(
                self,
                f"get_{nom_champ_specification}_display",
                None,
            )

            if callable(methode_specification_display):
                specification = methode_specification_display()

            # ============================
            # TOTAL
            # ============================
            total = prix * quantite
            total_general += total

            rapport.append({
                "champ": field.verbose_name,
                "code": champ_base,
                "etat": valeur,
                "etat_label": labels_etats.get(valeur, valeur),
                "fabricant": fabricant,
                "specification": specification or "-",
                "quantite": quantite,
                "prix": prix,
                "total": total,
            })

        return {
            "lignes": rapport,
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