from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantCourse, FabricantCapteur, RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
    RouesSerrageEtat, RefroidissementQualiteEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class EtatOptionnel(models.TextChoices):
    """Opération optionnelle (calibrage, diagnostic…)."""
    NON_PRESENT = "NON_PRESENT", _("Non présent")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")




class EtatDemontage(models.TextChoices):
    """Démontage / allègement."""
    NON_CONCERNE = "NON_CONCERNE", _("Non concerné")
    DEMONTE = "DEMONTE", _("Démonté")
    REMONTE = "REMONTE", _("Remonté")
    SUPPRIME = "SUPPRIME", _("Supprimé définitivement")


class TypeLubrification(models.TextChoices):
    HUMIDE_ORIGINE = "HUMIDE_ORIGINE", _("Carter humide d'origine")
    HUMIDE_CLOISONNE = "HUMIDE_CLOISONNE", _("Carter humide cloisonné (bâche à huile)")
    CARTER_SEC = "CARTER_SEC", _("Carter sec")


PIECES = [
    ("carter_sec_reservoir", _("Carter sec : réservoir d'huile")),
    ("carter_sec_pompe", _("Carter sec : pompe multi-étages")),
    ("carter_sec_durites", _("Carter sec : durites et raccords")),
    ("bache_huile", _("Bâche à huile / carter cloisonné")),
    ("radiateur_huile", _("Radiateur d'huile")),
    ("pistons_forges", _("Pistons forgés")),
    ("bielles_forgees", _("Bielles forgées")),
    ("arbres_cames", _("Arbres à cames")),
    ("soupapes_ressorts", _("Soupapes et ressorts renforcés")),
    ("joint_culasse_renforce", _("Joint de culasse renforcé")),
    ("admission_course", _("Admission (filtre / boîte à air)")),
    ("injecteurs_course", _("Injecteurs")),
    ("pompe_carburant_course", _("Pompe à carburant")),
    ("volant_moteur_allege", _("Volant moteur allégé")),
    ("rodage_moteur", _("Rodage du moteur")),
]


class PreparationMoteur(TechnicienMixin, models.Model):



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
        related_name="pc_moteur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="pc_moteur",
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
    kilometrage_pc_moteur = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # CARACTÉRISTIQUES
    # -------------------------
    type_lubrification = models.CharField(max_length=40, choices=TypeLubrification.choices, default=TypeLubrification.HUMIDE_ORIGINE, verbose_name=_("Lubrification"))
    puissance_origine = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance d'origine (ch)"))
    puissance_apres = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Puissance après préparation (ch)"))
    couple_origine = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Couple d'origine (Nm)"))
    couple_apres = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Couple après préparation (Nm)"))
    regime_maxi = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Régime maximum (tr/min)"))

    # -------------------------
    # COMPOSANTS
    # -------------------------
    # Carter sec : réservoir d'huile
    carter_sec_reservoir = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Carter sec : réservoir d'huile"))
    carter_sec_reservoir_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    carter_sec_reservoir_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    carter_sec_reservoir_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Carter sec : pompe multi-étages
    carter_sec_pompe = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Carter sec : pompe multi-étages"))
    carter_sec_pompe_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    carter_sec_pompe_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    carter_sec_pompe_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Carter sec : durites et raccords
    carter_sec_durites = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Carter sec : durites et raccords"))
    carter_sec_durites_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    carter_sec_durites_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    carter_sec_durites_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Bâche à huile / carter cloisonné
    bache_huile = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Bâche à huile / carter cloisonné"))
    bache_huile_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    bache_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    bache_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Radiateur d'huile
    radiateur_huile = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Radiateur d'huile"))
    radiateur_huile_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    radiateur_huile_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    radiateur_huile_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Pistons forgés
    pistons_forges = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Pistons forgés"))
    pistons_forges_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    pistons_forges_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pistons_forges_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Bielles forgées
    bielles_forgees = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Bielles forgées"))
    bielles_forgees_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    bielles_forgees_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    bielles_forgees_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Arbres à cames
    arbres_cames = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Arbres à cames"))
    arbres_cames_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    arbres_cames_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    arbres_cames_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Soupapes et ressorts renforcés
    soupapes_ressorts = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Soupapes et ressorts renforcés"))
    soupapes_ressorts_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    soupapes_ressorts_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    soupapes_ressorts_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Joint de culasse renforcé
    joint_culasse_renforce = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Joint de culasse renforcé"))
    joint_culasse_renforce_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    joint_culasse_renforce_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    joint_culasse_renforce_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Admission (filtre / boîte à air)
    admission_course = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Admission (filtre / boîte à air)"))
    admission_course_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    admission_course_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    admission_course_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Injecteurs
    injecteurs_course = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Injecteurs"))
    injecteurs_course_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    injecteurs_course_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    injecteurs_course_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Pompe à carburant
    pompe_carburant_course = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Pompe à carburant"))
    pompe_carburant_course_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    pompe_carburant_course_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pompe_carburant_course_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Volant moteur allégé
    volant_moteur_allege = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Volant moteur allégé"))
    volant_moteur_allege_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    volant_moteur_allege_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    volant_moteur_allege_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Rodage du moteur
    rodage_moteur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Rodage du moteur"))
    rodage_moteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    rodage_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


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
        related_name="pc_moteur"
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
        related_name="pc_moteur"
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
        related_name="pc_moteur",
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

        if self.voiture_exemplaire and self.kilometrage_pc_moteur is not None:
            if self.kilometrage_pc_moteur < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_pc_moteur": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Préparation moteur")
        verbose_name_plural = _("Préparation moteur")

    def __str__(self):
        return f"Préparation moteur - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES:
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
        # ANCIEN KM PRÉPARATION MOTEUR
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_pc_moteur
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
        if self.kilometrage_pc_moteur is not None:

            self.kilometrage_variation = (
                    self.kilometrage_pc_moteur
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km pc_moteur
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_pc_moteur
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
                    _("Préparation moteur")
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
                Maintenance.TypeMaintenance.PC_MOTEUR
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_pc_moteur is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_pc_moteur
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE PRÉPARATION MOTEUR
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
                and self.kilometrage_pc_moteur is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_pc_moteur
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

        pieces = PIECES

        for prefix, label in pieces:
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
                EtatDemontage.DEMONTE,
                EtatDemontage.REMONTE,
                EtatDemontage.SUPPRIME,
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

        if self.kilometrage_pc_moteur is None:
            return

        km = Decimal(str(self.kilometrage_pc_moteur))

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