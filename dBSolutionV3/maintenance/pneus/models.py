from decimal import Decimal, ROUND_HALF_UP

from django.core.validators import StepValueValidator

from django.core.exceptions import ValidationError
from maintenance.choices import RouesSerrageEtat, TAUX_HORAIRE_CHOICES, FabricantPneus
from maintenance.models import Maintenance
from django.conf import settings
from utils.mixin import TechnicienMixin
from django.db import models
from django.utils.translation import gettext_lazy as _





# ---------------------------
# TextChoices
# ---------------------------

class PneuEtat(models.TextChoices):
    OK = "OK", _("OK")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class ValveType(models.TextChoices):
    CAOUTCHOUC = "caoutchouc", _("Valve caoutchouc")
    METALLIQUE = "metallique", _("Valve métallique")
    TPMS_CAOUTCHOUC = "tpms_caoutchouc", _("Valve TPMS caoutchouc")
    TPMS_METALLIQUE = "tpms_metallique", _("Valve TPMS métallique")
    HAUTE_PRESSION = "haute_pression", _("Valve haute pression")
    MOTO = "moto", _("Valve moto")



class MasseEquilibrageType(models.TextChoices):
    # Masses à clipser
    CLIP_ACIER = "clip_acier", _("Masse à clipser en acier")
    CLIP_ZINC = "clip_zinc", _("Masse à clipser en zinc")
    CLIP_PLOMB = "clip_plomb", _("Masse à clipser en plomb")

    # Masses adhésives
    ADHESIVE_ACIER = "adhesive_acier", _("Masse adhésive en acier")
    ADHESIVE_ZINC = "adhesive_zinc", _("Masse adhésive en zinc")
    ADHESIVE_PLOMB = "adhesive_plomb", _("Masse adhésive en plomb")

    # Masses spécifiques
    MOTO = "moto", _("Masse d'équilibrage moto")
    CAMION = "camion", _("Masse d'équilibrage poids lourd")

    AUTRE = "autre", _("Autre")



# ---------------------------
# Modèle fusionné
# ---------------------------
class ControlePneus(TechnicienMixin, models.Model):
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
        related_name="controle_pneus",
        verbose_name=_("Maintenance"),
        null=True,  # autorisé vide à la création
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="controle_pneus",
        verbose_name="Kilomètres_checkup",
        null=True, blank=True
    )

    voiture_pneus = models.ForeignKey(
        "voiture_pneus.VoiturePneus",
        on_delete=models.CASCADE,
        related_name="controle_Pneus",
        verbose_name="Pneus",
        null=True, blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_pneus = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle des pneus"),
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # --- Pneus et Pression
    pneu_bande_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Bande de roulement du pneu avant droit"))
    pneu_bande_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu avant gauche"))
    pneu_bande_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu arrière droit"))
    pneu_bande_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("Bande de roulement du pneu arrière gauche"))

    pneu_epaisseur_avd = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant droit (mm)"))
    pneu_epaisseur_avg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu avant gauche (mm)"))
    pneu_epaisseur_ard = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière droit (mm)"))
    pneu_epaisseur_arg = models.FloatField(default=8.0, verbose_name=_("Épaisseur du pneu arrière gauche (mm)"))

    pneu_sidewall_avd = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK,verbose_name=_("flancs du pneu avant droit"))
    pneu_sidewall_avg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu avant gauche"))
    pneu_sidewall_ard = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu arrière droit"))
    pneu_sidewall_arg = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("flancs du pneu arrière gauche"))

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

    pneu_train_av =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Pneus avant à remplacer"))


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


    pneu_train_ar =  models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Pneus arrière à remplacer"))
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

    valve_pneu = models.CharField(max_length=25, choices=PneuEtat.choices, default=PneuEtat.OK, verbose_name=_("Valves de pneu"))
    valve_pneu_type = models.CharField(max_length=25, choices=ValveType.choices, default=ValveType.CAOUTCHOUC, verbose_name=_("type de valves de pneu"))
    valve_pneu_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA")
    )
    valve_pneu_quantite = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Quantité"))

    masse_equilibrage = models.CharField(max_length=25, choices=MasseEquilibrageType.choices, default=MasseEquilibrageType.CLIP_ZINC , verbose_name=_("Type de masses d'équilibrage"))


    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))


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

    remplacement_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Remplacement effectué"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pneus",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="controle_pneus_techs"
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
        related_name="controle_pneus_societe"
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
        verbose_name = _("Contrôle pneus")
        verbose_name_plural = _("Contrôles pneus")

    def __str__(self):
        return _("Contrôle pneus – Maintenance %(id)s") % {"id": self.maintenance.id}

    def clean(self):
        super().clean()

        if not self.voiture_exemplaire_id or self.kilometrage_pneus is None:
            return

        voiture = type(self.voiture_exemplaire).objects.get(
            pk=self.voiture_exemplaire_id
        )

        km_actuel = voiture.kilometres_chassis or 0

        if self.kilometrage_pneus < km_actuel:
            raise ValidationError({
                "kilometrage_pneus": _(
                    "Le kilométrage du contrôle pneus (%(km_controle)s) "
                    "ne peut pas être inférieur au kilométrage actuel de la voiture (%(km_voiture)s)."
                ) % {
                                         "km_controle": self.kilometrage_pneus,
                                         "km_voiture": km_actuel,
                                     }
            })

    def save(self, *args, **kwargs):

        ancien_kilometrage = 0

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
                    _("Controle des pneus")
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
                Maintenance.TypeMaintenance.PNEUS
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
            if self.kilometrage_pneus is not None:

                self.kilometrage_variation = (
                        self.kilometrage_pneus
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
                and self.kilometrage_pneus is not None
        ):

            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )

            if (
                    self.kilometrage_pneus
                    > (voiture.kilometres_chassis or 0)
            ):
                voiture.kilometres_chassis = (
                    self.kilometrage_pneus
                )

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        for field in self._meta.fields:
            field_name = field.name

            # Ne garder que les champs d'état des pneus
            if not (
                    isinstance(field, models.CharField)
                    and field.choices == PneuEtat.choices
            ):
                continue

            etat = getattr(self, field_name, None)

            # Pièces à remplacer ou déjà remplacées
            if etat not in (
                    PneuEtat.A_REMPLACER,
                    PneuEtat.REMPLACE,
            ):
                continue

            # =========================
            # FABRICANT
            # =========================
            fabricant = getattr(
                self,
                f"{field_name}_fabricant",
                None,
            )

            # Si fabricant est un objet (ForeignKey)
            if fabricant:
                fabricant = str(fabricant)
            else:
                fabricant = "-"

            # =========================
            # PRIX
            # =========================
            prix = Decimal(
                str(
                    getattr(
                        self,
                        f"{field_name}_prix",
                        Decimal("0.00"),
                    )
                    or Decimal("0.00")
                )
            )

            # =========================
            # QUANTITÉ
            # =========================
            quantite = Decimal(
                str(
                    getattr(
                        self,
                        f"{field_name}_quantite",
                        0,
                    )
                    or 0
                )
            )

            prix = prix.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            # =========================
            # LABEL ÉTAT
            # =========================
            methode_display = getattr(
                self,
                f"get_{field_name}_display",
                None,
            )

            etat_label = (
                methode_display()
                if callable(methode_display)
                else etat
            )

            # =========================
            # RAPPORT
            # =========================
            rapport.append({
                "champ": field.verbose_name,
                "nom": field.verbose_name,
                "code": field_name,
                "etat": etat,
                "etat_label": etat_label,
                "fabricant": fabricant,
                "prix": prix,
                "prix_unitaire": prix,
                "quantite": quantite,
                "total": total,
            })

        return {
            "lignes": rapport,
            "pieces": rapport,
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

