from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantSuspension, FabricantRoulement, FabricantSilentBloc, RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
    RouesSerrageEtat, RefroidissementQualiteEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class EtatOptionnel(models.TextChoices):
    """Pièce optionnelle : absente sur certains montages."""
    NON_PRESENT = "NON_PRESENT", _("Non présent")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


PIECES_SUSPENSION = [
    ("combines_filetes_av", _("Combinés filetés avant")),
    ("combines_filetes_ar", _("Combinés filetés arrière")),
    ("amortisseurs_sport_av", _("Amortisseurs sport avant")),
    ("amortisseurs_sport_ar", _("Amortisseurs sport arrière")),
    ("ressorts_sport_av", _("Ressorts sport avant")),
    ("ressorts_sport_ar", _("Ressorts sport arrière")),
    ("ressorts_rappel", _("Ressorts de rappel (helper)")),
    ("coupelles_reglables", _("Coupelles réglables (carrossage)")),
    ("roulements_suspension", _("Roulements de suspension")),
    ("butees_suspension", _("Butées de suspension")),
    ("soufflets", _("Soufflets / kits de protection")),
    ("ecrous", _("Écrous de tige d'amortisseur")),
    ("biellettes_reglables", _("Biellettes de barre stabilisatrice réglables")),
    ("huile_amortisseur", _("Huile d'amortisseur")),
    ("prereglage", _("Préréglage du combiné fileté")),
]


class SuspensionSport(TechnicienMixin, models.Model):



    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )
    # -------------------------
    # RELATIONS
    # -------------------------
    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="susp_suspension_sport",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="susp_suspension_sport",
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometres_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Kilomètres rollback")
    )


    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_boite_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback boite")
    )

    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_moteur_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback moteur")
    )

    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)

    kilometres_embrayage_rollback = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres rollback embrayage")
    )

    # -------------------------
    # INFOS
    # -------------------------
    kilometrage_suspension_sport = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # PIÈCES DE SUSPENSION
    # -------------------------
    # Combinés filetés avant
    combines_filetes_av = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Combinés filetés avant"))
    combines_filetes_av_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    combines_filetes_av_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    combines_filetes_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Combinés filetés arrière
    combines_filetes_ar = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Combinés filetés arrière"))
    combines_filetes_ar_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    combines_filetes_ar_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    combines_filetes_ar_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Amortisseurs sport avant
    amortisseurs_sport_av = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Amortisseurs sport avant"))
    amortisseurs_sport_av_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    amortisseurs_sport_av_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    amortisseurs_sport_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Amortisseurs sport arrière
    amortisseurs_sport_ar = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Amortisseurs sport arrière"))
    amortisseurs_sport_ar_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    amortisseurs_sport_ar_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    amortisseurs_sport_ar_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Ressorts sport avant
    ressorts_sport_av = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Ressorts sport avant"))
    ressorts_sport_av_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    ressorts_sport_av_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    ressorts_sport_av_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Ressorts sport arrière
    ressorts_sport_ar = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Ressorts sport arrière"))
    ressorts_sport_ar_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    ressorts_sport_ar_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    ressorts_sport_ar_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Ressorts de rappel (helper)
    ressorts_rappel = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Ressorts de rappel (helper)"))
    ressorts_rappel_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    ressorts_rappel_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    ressorts_rappel_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Coupelles réglables (carrossage)
    coupelles_reglables = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Coupelles réglables (carrossage)"))
    coupelles_reglables_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    coupelles_reglables_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    coupelles_reglables_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Roulements de suspension
    roulements_suspension = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Roulements de suspension"))
    roulements_suspension_fabricant = models.CharField(max_length=30, choices=FabricantRoulement.choices, default=FabricantRoulement.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    roulements_suspension_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    roulements_suspension_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Butées de suspension
    butees_suspension = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Butées de suspension"))
    butees_suspension_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    butees_suspension_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    butees_suspension_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Soufflets / kits de protection
    soufflets = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Soufflets / kits de protection"))
    soufflets_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    soufflets_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    soufflets_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Écrous de tige d'amortisseur
    ecrous = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Écrous de tige d'amortisseur"))
    ecrous_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    ecrous_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    ecrous_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Biellettes de barre stabilisatrice réglables
    biellettes_reglables = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Biellettes de barre stabilisatrice réglables"))
    biellettes_reglables_fabricant = models.CharField(max_length=30, choices=FabricantSuspension.choices, default=FabricantSuspension.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    biellettes_reglables_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    biellettes_reglables_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Huile d'amortisseur
    huile_amortisseur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Huile d'amortisseur"))
    huile_amortisseur_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    huile_amortisseur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    huile_amortisseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Préréglage du combiné fileté
    prereglage = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Préréglage du combiné fileté"))
    prereglage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    prereglage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # -------------------------
    # PRÉRÉGLAGE DU COMBINÉ FILETÉ (valeurs de réglage)
    # -------------------------
    prereglage_hauteur_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur de caisse avant (mm)"))
    prereglage_hauteur_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Hauteur de caisse arrière (mm)"))
    prereglage_precharge_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Précharge ressort avant (mm)"))
    prereglage_precharge_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Précharge ressort arrière (mm)"))
    prereglage_detente_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Détente avant (clics)"))
    prereglage_detente_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Détente arrière (clics)"))
    prereglage_compression_av = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Compression avant (clics)"))
    prereglage_compression_ar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Compression arrière (clics)"))


    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

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

    # Technicien qui fait le checkup (toujours l'utilisateur courant)
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="susp_suspension_sport"
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
        related_name="susp_suspension_sport"
    )

    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="susp_suspension_sport",
        verbose_name=_("Main d'oeuvre")
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

    def clean(self):
        super().clean()

        if self.voiture_exemplaire and self.kilometrage_suspension_sport is not None:
            if self.kilometrage_suspension_sport < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_suspension_sport": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Suspension sport")
        verbose_name_plural = _("Suspension sport")

    def __str__(self):
        return f"Suspension sport - {self.voiture_exemplaire}"



    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):
        prix = getattr(
            self,
            f"{prefix}_prix",
            Decimal("0.00"),
        )

        quantite = getattr(
            self,
            f"{prefix}_quantite",
            0,
        )

        if not prix or not self.pays:
            return

        # -------------------------
        # TVA
        # -------------------------
        taux_tva = Decimal(
            str(TVAConfig.get_tva(self.pays))
        )

        tva_rate = taux_tva / Decimal("100")

        # -------------------------
        # PRIX HTVA
        # -------------------------
        prix_htva = Decimal(str(prix))

        prix_htva = prix_htva.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # TVA
        # -------------------------
        tva = (
                prix_htva * tva_rate
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # PRIX TTC
        # -------------------------
        prix_ttc = (
                prix_htva + tva
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        # -------------------------
        # SAUVEGARDE DES CALCULS
        # -------------------------
        setattr(
            self,
            f"{prefix}_prix_vente_htva",
            prix_htva,
        )

        setattr(
            self,
            f"{prefix}_tva_vente",
            tva,
        )

        setattr(
            self,
            f"{prefix}_prix_ttc",
            prix_ttc,
        )

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):

        # 🔥 synchro kilométrage AVANT save
        if hasattr(self, "sync_kilometrage"):
            self.sync_kilometrage()

        # Calculs
        for prefix, _label in PIECES_SUSPENSION:
            self.calcul_piece(prefix)

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
        # ANCIEN KM SUSPENSION_SPORT
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_suspension_sport
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
        if self.kilometrage_suspension_sport is not None:

            self.kilometrage_variation = (
                    self.kilometrage_suspension_sport
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km suspension_sport
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_suspension_sport
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
                    _("Suspension sport")
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
                Maintenance.TypeMaintenance.SUSPENSION_SPORT
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_suspension_sport is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_suspension_sport
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE SUSPENSION_SPORT
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
                and self.kilometrage_suspension_sport is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_suspension_sport
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

        # ========================================================
        # SAUVEGARDE
        # ========================================================

        super().save(*args, **kwargs)


    def generer_rapport_remplacement(self):
        rapport = []
        total_general = Decimal("0.00")

        pieces = PIECES_SUSPENSION

        for prefix, label in pieces:
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
            ]:
                continue

            # -------------------------
            # FABRICANT
            # -------------------------
            fabricant = getattr(
                self,
                f"{prefix}_fabricant",
                None,
            )

            fabricant_label = fabricant

            try:
                fabricant_field = self._meta.get_field(
                    f"{prefix}_fabricant"
                )

                if fabricant_field.choices:
                    fabricant_label = dict(
                        fabricant_field.choices
                    ).get(
                        fabricant,
                        fabricant,
                    )

            except FieldDoesNotExist:
                fabricant = None
                fabricant_label = None

            # -------------------------
            # PRIX
            # -------------------------
            prix = getattr(
                self,
                f"{prefix}_prix",
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
                f"{prefix}_quantite",
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # Quantité 0 = ne pas ajouter au rapport
            if quantite <= 0:
                continue

            # -------------------------
            # TOTAL
            # -------------------------
            total = prix * quantite
            total_general += total

            # -------------------------
            # RAPPORT
            # -------------------------
            rapport.append(
                {
                    "champ": label,
                    "code": prefix,

                    "etat": etat,
                    "etat_label": dict(
                        self._meta.get_field(prefix).choices
                    ).get(
                        etat,
                        etat,
                    ),

                    "fabricant": fabricant,
                    "fabricant_label": fabricant_label,

                    "prix": prix,
                    "quantite": quantite,
                    "total": total,
                }
            )

        return {
            "lignes": rapport,
            "total_general": total_general,
        }


    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        return self.main_oeuvre.temps_display




    def sync_kilometrage(self):
        if not self.voiture_exemplaire:
            return

        if self.kilometrage_suspension_sport is None:
            return

        km = Decimal(str(self.kilometrage_suspension_sport))

        voiture = self.voiture_exemplaire
        voiture.refresh_from_db(fields=["kilometres_chassis"])

        if km < voiture.kilometres_chassis:
            raise ValidationError("Kilométrage invalide")

        # 🔥 SOURCE UNIQUE
        voiture.kilometres_chassis = km
        voiture.save(update_fields=["kilometres_chassis"])

        # 🔁 copie locale
        self.kilometres_chassis = km

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