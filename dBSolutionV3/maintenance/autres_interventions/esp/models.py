from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantCapteur, RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
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


PIECES_ESP = [
    ("groupe_hydraulique_esp", _("Groupe hydraulique ESP (bloc et pompe)")),
    ("calculateur_esp", _("Calculateur ESP")),
    ("capteur_angle_volant", _("Capteur d'angle de volant")),
    ("capteur_lacet", _("Capteur de lacet et d'accélération transversale")),
    ("capteur_pression_freinage", _("Capteur de pression de freinage")),
    ("capteurs_vitesse_roue", _("Capteurs de vitesse de roue")),
    ("contacteur_feux_stop", _("Contacteur de feux stop")),
    ("bouton_esp", _("Bouton ESP (désactivation)")),
    ("faisceau_connecteurs_esp", _("Faisceau et connecteurs ESP")),
    ("liquide_frein_esp", _("Liquide de frein (purge du groupe ESP)")),
    ("calibrage_capteurs_esp", _("Calibrage des capteurs (angle de volant, lacet)")),
    ("diagnostic_codage_esp", _("Diagnostic et codage du calculateur ESP")),
]


class Esp(TechnicienMixin, models.Model):



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
        related_name="esp_esp",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="esp_esp",
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
    kilometrage_esp = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # COMPOSANTS ESP
    # -------------------------
    # Groupe hydraulique ESP (bloc et pompe)
    groupe_hydraulique_esp = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Groupe hydraulique ESP (bloc et pompe)"))
    groupe_hydraulique_esp_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    groupe_hydraulique_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    groupe_hydraulique_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Calculateur ESP
    calculateur_esp = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Calculateur ESP"))
    calculateur_esp_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    calculateur_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    calculateur_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Capteur d'angle de volant
    capteur_angle_volant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur d'angle de volant"))
    capteur_angle_volant_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteur_angle_volant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_angle_volant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Capteur de lacet et d'accélération transversale
    capteur_lacet = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de lacet et d'accélération transversale"))
    capteur_lacet_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteur_lacet_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_lacet_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Capteur de pression de freinage
    capteur_pression_freinage = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteur de pression de freinage"))
    capteur_pression_freinage_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteur_pression_freinage_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteur_pression_freinage_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Capteurs de vitesse de roue
    capteurs_vitesse_roue = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Capteurs de vitesse de roue"))
    capteurs_vitesse_roue_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    capteurs_vitesse_roue_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    capteurs_vitesse_roue_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Contacteur de feux stop
    contacteur_feux_stop = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Contacteur de feux stop"))
    contacteur_feux_stop_fabricant = models.CharField(max_length=30, choices=FabricantCapteur.choices, default=FabricantCapteur.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    contacteur_feux_stop_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    contacteur_feux_stop_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Bouton ESP (désactivation)
    bouton_esp = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bouton ESP (désactivation)"))
    bouton_esp_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    bouton_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    bouton_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Faisceau et connecteurs ESP
    faisceau_connecteurs_esp = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Faisceau et connecteurs ESP"))
    faisceau_connecteurs_esp_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    faisceau_connecteurs_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    faisceau_connecteurs_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Liquide de frein (purge du groupe ESP)
    liquide_frein_esp = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Liquide de frein (purge du groupe ESP)"))
    liquide_frein_esp_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    liquide_frein_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    liquide_frein_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Calibrage des capteurs (angle de volant, lacet)
    calibrage_capteurs_esp = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Calibrage des capteurs (angle de volant, lacet)"))
    calibrage_capteurs_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    calibrage_capteurs_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Diagnostic et codage du calculateur ESP
    diagnostic_codage_esp = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Diagnostic et codage du calculateur ESP"))
    diagnostic_codage_esp_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    diagnostic_codage_esp_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


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
        related_name="esp_esp"
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
        related_name="esp_esp"
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
        related_name="esp_esp",
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

        if self.voiture_exemplaire and self.kilometrage_esp is not None:
            if self.kilometrage_esp < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_esp": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("ESP (contrôle de stabilité)")
        verbose_name_plural = _("ESP (contrôle de stabilité)")

    def __str__(self):
        return f"ESP (contrôle de stabilité) - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_ESP:
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
        # ANCIEN KM ESP
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_esp
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
        if self.kilometrage_esp is not None:

            self.kilometrage_variation = (
                    self.kilometrage_esp
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km esp
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_esp
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
                    _("ESP (contrôle de stabilité)")
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
                Maintenance.TypeMaintenance.ESP
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_esp is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_esp
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE ESP
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
                and self.kilometrage_esp is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_esp
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

        pieces = PIECES_ESP

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

        if self.kilometrage_esp is None:
            return

        km = Decimal(str(self.kilometrage_esp))

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