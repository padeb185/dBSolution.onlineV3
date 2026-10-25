from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantCapteur, FabricantClim, FabricantFiltre, RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
    RouesSerrageEtat, RefroidissementQualiteEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")


class EtatOptionnel(models.TextChoices):
    """Opération optionnelle (calibrage, diagnostic…)."""
    NON_PRESENT = "NON_PRESENT", _("Non présent")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")


PIECES_VENTILATION = [
    ("soufflerie", _("Soufflerie (pulseur d'air habitacle)")),
    ("moteur_ventilation", _("Moteur de ventilation")),
    ("resistance_vitesse", _("Résistance de vitesse du moteur de ventilation")),
    ("module_commande_pulseur", _("Module de commande électronique du pulseur")),
    ("filtre_habitacle", _("Filtre d'habitacle (pollen / charbon actif)")),
    ("resistance_chauffage", _("Résistance de chauffage additionnel (PTC)")),
    ("commande_ventilation", _("Commande / tableau de ventilation-chauffage")),
    ("volets_repartition", _("Volets de répartition et de mixage d'air")),
    ("moteurs_volets", _("Moteurs (actionneurs) de volets")),
    ("volet_recyclage", _("Volet de recyclage d'air")),
    ("sonde_temperature_habitacle", _("Sonde de température habitacle")),
    ("aerateurs", _("Aérateurs et grilles de ventilation")),
    ("conduits_ventilation", _("Conduits et gaines d'air")),
    ("faisceau_ventilation", _("Faisceau et connecteurs")),
    ("desinfection_ventilation", _("Désinfection / traitement antibactérien du circuit")),
    ("diagnostic_ventilation", _("Diagnostic et codage")),
]


class Ventilation(TechnicienMixin, models.Model):



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
        related_name="ventilation",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="ventilation",
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
    kilometrage_ventilation = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # COMPOSANTS VENTILATION
    # -------------------------
    # Soufflerie (pulseur d'air habitacle)
    soufflerie = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Soufflerie (pulseur d'air habitacle)"))
    soufflerie_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    soufflerie_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    soufflerie_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Moteur de ventilation
    moteur_ventilation = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Moteur de ventilation"))
    moteur_ventilation_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    moteur_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    moteur_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Résistance de vitesse du moteur de ventilation
    resistance_vitesse = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Résistance de vitesse du moteur de ventilation"))
    resistance_vitesse_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    resistance_vitesse_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    resistance_vitesse_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Module de commande électronique du pulseur
    module_commande_pulseur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Module de commande électronique du pulseur"))
    module_commande_pulseur_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    module_commande_pulseur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    module_commande_pulseur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Filtre d'habitacle (pollen / charbon actif)
    filtre_habitacle = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Filtre d'habitacle (pollen / charbon actif)"))
    filtre_habitacle_fabricant = models.CharField(max_length=30, choices=FabricantFiltre.choices, default=FabricantFiltre.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    filtre_habitacle_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    filtre_habitacle_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Résistance de chauffage additionnel (PTC)
    resistance_chauffage = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Résistance de chauffage additionnel (PTC)"))
    resistance_chauffage_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    resistance_chauffage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    resistance_chauffage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Commande / tableau de ventilation-chauffage
    commande_ventilation = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Commande / tableau de ventilation-chauffage"))
    commande_ventilation_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    commande_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    commande_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Volets de répartition et de mixage d'air
    volets_repartition = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Volets de répartition et de mixage d'air"))
    volets_repartition_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    volets_repartition_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    volets_repartition_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Moteurs (actionneurs) de volets
    moteurs_volets = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Moteurs (actionneurs) de volets"))
    moteurs_volets_fabricant = models.CharField(max_length=30, choices=FabricantClim.choices, default=FabricantClim.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    moteurs_volets_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    moteurs_volets_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Volet de recyclage d'air
    volet_recyclage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Volet de recyclage d'air"))
    volet_recyclage_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    volet_recyclage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    volet_recyclage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Sonde de température habitacle
    sonde_temperature_habitacle = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Sonde de température habitacle"))
    sonde_temperature_habitacle_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    sonde_temperature_habitacle_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    sonde_temperature_habitacle_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Aérateurs et grilles de ventilation
    aerateurs = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Aérateurs et grilles de ventilation"))
    aerateurs_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    aerateurs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    aerateurs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Conduits et gaines d'air
    conduits_ventilation = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Conduits et gaines d'air"))
    conduits_ventilation_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    conduits_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    conduits_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Faisceau et connecteurs
    faisceau_ventilation = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Faisceau et connecteurs"))
    faisceau_ventilation_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    faisceau_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    faisceau_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Désinfection / traitement antibactérien du circuit
    desinfection_ventilation = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Désinfection / traitement antibactérien du circuit"))
    desinfection_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    desinfection_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Diagnostic et codage
    diagnostic_ventilation = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Diagnostic et codage"))
    diagnostic_ventilation_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    diagnostic_ventilation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))



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
        related_name="ventilation"
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
        related_name="ventilation"
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
        related_name="ventilation",
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

        if self.voiture_exemplaire and self.kilometrage_ventilation is not None:
            if self.kilometrage_ventilation < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_ventilation": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Ventilation")
        verbose_name_plural = _("Ventilation")

    def __str__(self):
        return f"Ventilation - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_VENTILATION:
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
        # ANCIEN KM VENTILATION
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_ventilation
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
        if self.kilometrage_ventilation is not None:

            self.kilometrage_variation = (
                    self.kilometrage_ventilation
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km ventilation
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_ventilation
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
                    _("Ventilation")
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
                Maintenance.TypeMaintenance.VENTILATION
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_ventilation is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_ventilation
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE VENTILATION
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
                and self.kilometrage_ventilation is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_ventilation
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

        pieces = PIECES_VENTILATION

        for prefix, label in pieces:
            etat = getattr(self, prefix, None)

            if etat not in [
                EtatOKNotOK.NOT_OK,
                EtatOKNotOK.REMPLACE,
                EtatOKNotOK.AJOUTER,
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

        if self.kilometrage_ventilation is None:
            return

        km = Decimal(str(self.kilometrage_ventilation))

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