from decimal import Decimal, ROUND_HALF_UP

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import TAUX_HORAIRE_CHOICES, FabricantPiece, FabricantCapteurEchappement, FabricantTurbo, \
    FabricantIntercooler, FabricantVanneEGR, FabricantDurite, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")





# ---------------------------
# Modèle fusionné
# ---------------------------
class Admission(TechnicienMixin, models.Model):


    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="admission",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="admission",
        verbose_name="Kilomètres_admission",
        null=True,
        blank=True
    )

    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_admission = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du controle"),

    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # -------------------------
    # PIECES
    # -------------------------
    def piece_fields(prefix):
        return {
            f"{prefix}": models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK),
            f"{prefix}_prix": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_tva_achat": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_marge": models.IntegerField(null=True, blank=True),
            f"{prefix}_prix_vente_htva": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_tva_vente": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_prix_ttc": models.DecimalField(max_digits=10, decimal_places=2, default=0),
            f"{prefix}_quantite": models.IntegerField(default=0),
        }

    # -------------------------
    # FILTRATION
    filtre_air_pc = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Filtre à air"))
    filtre_air_pc_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    filtre_air_pc_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    filtre_air_pc_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    boitier_filtre_air = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Boîtier filtre à air"))
    boitier_filtre_air_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    boitier_filtre_air_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    boitier_filtre_air_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # MESURE AIR
    debitmetre = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Débitmètre d'air"))
    debitmetre_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    debitmetre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    debitmetre_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_map = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur MAP"))
    capteur_map_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    capteur_map_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    capteur_map_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    capteur_temperature_air = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Capteur température air"))
    capteur_temperature_air_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    capteur_temperature_air_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    capteur_temperature_air_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # ADMISSION PRINCIPALE
    corps_papillon = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Corps de papillon"))
    corps_papillon_fabricant = models.CharField(max_length=25, choices=FabricantCapteurEchappement.choices,default=FabricantCapteurEchappement.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    corps_papillon_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    corps_papillon_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    collecteur_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Collecteur d'admission"))
    collecteur_admission_fabricant = models.CharField(max_length=25, choices=FabricantPiece.choices,default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    collecteur_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    collecteur_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # SURALIMENTATION
    turbo = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Turbo"))
    turbo_fabricant = models.CharField(max_length=25, choices=FabricantTurbo.choices, default=FabricantTurbo.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    turbo_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    turbo_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    intercooler = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Intercooler"))
    intercooler_fabricant = models.CharField(max_length=25, choices=FabricantIntercooler.choices, default=FabricantIntercooler.CHOISIR,verbose_name=_("Fabricant"), blank=True)
    intercooler_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    intercooler_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # EGR
    vanne_egr = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT,verbose_name=_("Vanne EGR"))
    vanne_egr_fabricant = models.CharField(max_length=25, choices=FabricantVanneEGR.choices, default=FabricantVanneEGR.CHOISIR,verbose_name=_("Fabricant"), blank=True)
    vanne_egr_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    vanne_egr_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # DIVERS
    durites_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Durites d'admission"))
    durites_admission_fabricant = models.CharField(max_length=25, choices=FabricantDurite.choices, default=FabricantDurite.CHOISIR,verbose_name=_("Fabricant"), blank=True)
    durites_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    durites_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    joints_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Joints admission"))
    joints_admission_fabricant = models.CharField(max_length=25, choices=FabricantDurite.choices,default=FabricantDurite.CHOISIR, verbose_name=_("Fabricant"),blank=True)
    joints_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat htva"))
    joints_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))



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

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admission",
        verbose_name=_("Main d'oeuvre")
    )

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="admission"
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
        related_name="admission"
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
        verbose_name = _("Admission")
        verbose_name_plural = _("Admissions")

    def __str__(self):
        voiture = getattr(self, "voiture_exemplaire", None)
        return f"Admission moteur - {voiture or 'Sans véhicule'}"

    def clean(self):
        super().clean()

        voiture = getattr(self, "voiture_exemplaire", None)

        if voiture and self.kilometrage_admission is not None:
            if self.kilometrage_admission < voiture.kilometres_chassis:
                raise ValidationError({
                    'kilometrage_admission': _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage actuel."
                    )
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if (
                not self.tech_technicien_id
                and hasattr(self, "_user")
        ):
            self.assign_technicien(
                self._user
            )

        # =========================
        # VEHICULE
        # =========================
        voiture = None

        if self.voiture_exemplaire_id:
            voiture = type(
                self.voiture_exemplaire
            ).objects.get(
                pk=self.voiture_exemplaire_id
            )

        # =========================
        # ANCIEN KM ADMISSION
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_admission
                        or ancien_objet.kilometres_chassis
                        or 0
                )

        elif voiture:

            ancien_kilometrage = (
                    voiture.kilometres_chassis
                    or 0
            )

        # =========================
        # VARIATION
        # =========================
        if self.kilometrage_admission is not None:

            self.kilometrage_variation = (
                    self.kilometrage_admission
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_admission
            )

        else:

            self.kilometrage_variation = 0

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if (
                self.main_oeuvre_id
                and self.voiture_exemplaire_id
        ):
            self.main_oeuvre.descriptif = (
                    _("Admission")
                    + " "
                    + str(self.voiture_exemplaire)
            )

            self.main_oeuvre.save(
                update_fields=[
                    "descriptif"
                ]
            )

        # =========================
        # MAINTENANCE
        # =========================
        if (
                self.maintenance_id
                and self.voiture_exemplaire_id
        ):

            self.maintenance.type_maintenance = (
                Maintenance.TypeMaintenance.ADMISSION
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_admission is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_admission
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE ADMISSION
        # =========================
        super().save(
            *args,
            **kwargs
        )

        # =========================
        # UPDATE VEHICULE
        # =========================
        if (
                voiture is not None
                and self.kilometrage_admission is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_admission
            )

            kilometrage_vehicule = int(
                voiture.kilometres_chassis
                or 0
            )

            # Ne jamais faire redescendre
            # le kilométrage général du véhicule
            if nouveau_kilometrage >= kilometrage_vehicule:
                voiture.kilometres_chassis = (
                    nouveau_kilometrage
                )

                voiture.save(
                    update_fields=[
                        "kilometres_chassis"
                    ]
                )



        # -------------------------
        # RAPPORT
        # -------------------------

    def calcul_piece(self, prefix):
        prix_achat = getattr(self, f"{prefix}_prix_achat")
        marge = getattr(self, f"{prefix}_marge")
        quantite = getattr(self, f"{prefix}_quantite")

        if not prix_achat or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        # TVA achat
        setattr(self, f"{prefix}_tva_achat",
                (prix_achat * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

        # HTVA
        if marge:
            prix_htva = prix_achat * (1 + Decimal(marge) / 100)
        else:
            prix_htva = prix_achat

        prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)

        # TVA vente
        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        setattr(self, f"{prefix}_tva_vente", tva)

        # TTC
        prix_ttc = prix_htva + tva
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    def generer_rapport_remplacement(self):
        lignes = []
        total_general = Decimal("0.00")
        etats_labels = dict(EtatOKNotOK.choices)

        for field in self._meta.fields:
            field_name = field.name

            if not (
                    isinstance(field, models.CharField)
                    and field.choices == EtatOKNotOK.choices
            ):
                continue

            valeur = getattr(self, field_name, None)

            if valeur not in (
                    EtatOKNotOK.NOT_OK,
                    EtatOKNotOK.REMPLACE,
            ):
                continue

            # -------------------------
            # Prix
            # -------------------------

            prix = getattr(
                self,
                f"{field_name}_prix",
                None,
            )

            if prix is None:
                prix = getattr(
                    self,
                    f"{field_name}_prix_achat",
                    Decimal("0.00"),
                )

            prix = Decimal(str(prix or "0.00"))

            # -------------------------
            # Quantité
            # -------------------------

            quantite = getattr(
                self,
                f"{field_name}_quantite",
                1,
            )

            quantite = Decimal(
                str(
                    quantite
                    if quantite not in (None, 0)
                    else 1
                )
            )

            # -------------------------
            # Fabricant
            # -------------------------

            fabricant_field_name = f"{field_name}_fabricant"

            fabricant = getattr(
                self,
                fabricant_field_name,
                None,
            )

            fabricant_label = "-"

            if fabricant not in (
                    None,
                    "",
                    "CHOISIR",
            ):
                get_fabricant_display = getattr(
                    self,
                    f"get_{fabricant_field_name}_display",
                    None,
                )

                if callable(get_fabricant_display):
                    fabricant_label = get_fabricant_display()
                else:
                    fabricant_label = fabricant

            # -------------------------
            # Total
            # -------------------------

            total = (prix * quantite).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            total_general += total

            lignes.append({
                "champ": field.verbose_name,
                "code": field_name,

                "etat": valeur,
                "etat_label": etats_labels.get(
                    valeur,
                    valeur,
                ),

                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "prix": prix.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),

                "quantite": quantite,
                "total": total,
            })

        return {
            "lignes": lignes,

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

