from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import TAUX_HORAIRE_CHOICES, FabricantPompeCarburant, FabricantPompeHautePression, \
    FabricantRampeInjection, FabricantCapteurPressionRampe, FabricantTuyauxHautePression, FabricantInjecteur, \
    FabricantConnecteurInjecteur, TVAConfig
from maintenance.models import Maintenance





class TypeCarburantInjection(models.TextChoices):
    ESSENCE = "ESSENCE", _("Essence")
    ETHANOL = "ETHANOL", _("Éthanol / E85")
    DIESEL = "DIESEL", _("Diesel")
    CNG = "CNG", _("CNG / Gaz naturel")
    LPG = "LPG", _("LPG / GPL")
    HYDROGENE = "HYDROGENE", _("Hydrogène")
    AUTRE = "AUTRE", _("Autre")


class EtatInjection(models.TextChoices):
    OK = "OK", _("OK")
    A_CONTROLER = "A_CONTROLER", _("À contrôler")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    NETTOYE = "NETTOYE", _("Nettoyé")
    NON_APPLICABLE = "NON_APPLICABLE", _("Non applicable")


class Injection(models.Model):


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
        related_name="injection",
        null=True,
        blank=True
    )

    id = models.AutoField(primary_key=True)



    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="injections",
        verbose_name=_("Véhicule"),
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_injection = models.PositiveIntegerField(
        verbose_name= _("Kilométrage du contrôle de l'injection")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    type_carburant = models.CharField(
        max_length=20,
        choices=TypeCarburantInjection.choices,
        default=TypeCarburantInjection.ESSENCE,
        verbose_name=_("Type de carburant"),
    )

    # ==========================================================
    # POMPE À CARBURANT
    # ==========================================================

    pompe_carburant_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("État de la pompe à carburant"),
    )
    pompe_carburant_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPompeCarburant.choices,
        default=FabricantPompeCarburant.CHOISIR,
        verbose_name=_("Fabricant de la pompe à carburant"),
    )

    pompe_carburant_pression_bar = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name=_("Pression de la pompe à carburant en bar"),
    )

    pompe_carburant_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix de la pompe à carburant"),
    )

    pompe_carburant_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de pompes à carburant"),
    )

    # ==========================================================
    # DIESEL / INJECTION HAUTE PRESSION
    # ==========================================================

    pompe_haute_pression_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.NON_APPLICABLE,
        verbose_name=_("État de la pompe haute pression"),
    )


    pompe_haute_pression_fabricant = models.CharField(
        max_length=50,
        choices=FabricantPompeHautePression.choices,
        default=FabricantPompeHautePression.CHOISIR,
        verbose_name=_("Fabricant de la pompe haute pression"),
    )

    pompe_haute_pression_pression_bar = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name=_("Pression de la pompe haute pression en bar"),
    )


    pompe_haute_pression_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix de la pompe haute pression"),
    )

    pompe_haute_pression_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de pompes haute pression"),
    )

    # ==========================================================
    # RAMPE D'INJECTION
    # ==========================================================

    rampe_injection_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("État de la rampe d'injection"),
    )


    rampe_injection_fabricant = models.CharField(
        max_length=50,
        choices=FabricantRampeInjection.choices,
        default=FabricantRampeInjection.CHOISIR,
        verbose_name=_("Fabricant de la rampe d'injection"),
    )

    rampe_injection_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix de la rampe d'injection"),
    )

    rampe_injection_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de rampes d'injection"),
    )

    # ==========================================================
    # CAPTEUR DE PRESSION DE RAMPE
    # ==========================================================

    capteur_pression_rampe_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("État du capteur de pression de rampe"),
    )
    capteur_pression_rampe_fabricant = models.CharField(
        max_length=50,
        choices=FabricantCapteurPressionRampe.choices,
        default=FabricantCapteurPressionRampe.CHOISIR,
        verbose_name=_("Fabricant du capteur de pression de rampe"),
    )

    pression_rampe_bar = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name=_("Pression de rampe mesurée en bar"),
    )

    capteur_pression_rampe_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix du capteur de pression de rampe"),
    )

    capteur_pression_rampe_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de capteurs de pression de rampe"),
    )

    # ==========================================================
    # TUYAUX HAUTE PRESSION
    # ==========================================================

    tuyaux_haute_pression_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.NON_APPLICABLE,
        verbose_name=_("État des tuyaux haute pression"),
    )
    tuyaux_haute_pression_fabricant = models.CharField(
        max_length=50,
        choices=FabricantTuyauxHautePression.choices,
        default=FabricantTuyauxHautePression.CHOISIR,
        verbose_name=_("Fabricant des tuyaux haute pression"),
    )

    tuyaux_haute_pression_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix des tuyaux haute pression"),
    )

    tuyaux_haute_pression_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de tuyaux haute pression"),
    )

    # ==========================================================
    # INJECTEURS
    # ==========================================================

    injecteurs_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("État des injecteurs"),
    )

    nombre_injecteurs = models.PositiveSmallIntegerField(
        default=4,
        verbose_name=_("Nombre d'injecteurs"),
    )
    injecteurs_fabricant = models.CharField(
        max_length=50,
        choices=FabricantInjecteur.choices,
        default=FabricantInjecteur.CHOISIR,
        verbose_name=_("Fabricant des injecteurs"),
    )

    injecteurs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix unitaire d'un injecteur"),
    )

    injecteurs_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité d'injecteurs remplacés"),
    )

    # ==========================================================
    # RÉSISTANCE INJECTEURS
    # ==========================================================

    injecteur_1_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 1 en ohms"),
    )

    injecteur_2_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 2 en ohms"),
    )

    injecteur_3_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 3 en ohms"),
    )

    injecteur_4_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 4 en ohms"),
    )

    injecteur_5_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 5 en ohms"),
    )

    injecteur_6_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 6 en ohms"),
    )

    injecteur_7_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 7 en ohms"),
    )

    injecteur_8_resistance_ohm = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.000"))],
        verbose_name=_("Résistance injecteur 8 en ohms"),
    )

    # ==========================================================
    # NETTOYAGE INJECTEURS
    # ==========================================================

    nettoyage_injecteurs_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("Nettoyage des injecteurs effectué"),
    )

    nettoyage_injecteurs_quantite = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Nombre d'injecteurs nettoyés"),
    )

    nettoyage_injecteurs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix du nettoyage des injecteurs"),
    )

    # ==========================================================
    # CONNECTEURS
    # ==========================================================

    connecteurs_injecteurs_etat = models.CharField(
        max_length=20,
        choices=EtatInjection.choices,
        default=EtatInjection.OK,
        verbose_name=_("État des connecteurs d'injecteurs"),
    )
    connecteurs_injecteurs_fabricant = models.CharField(
        max_length=50,
        choices=FabricantConnecteurInjecteur.choices,
        default=FabricantConnecteurInjecteur.CHOISIR,
        verbose_name=_("Fabricant des connecteurs d'injecteurs"),
    )

    connecteurs_injecteurs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name=_("Prix des connecteurs d'injecteurs"),
    )

    connecteurs_injecteurs_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité de connecteurs d'injecteurs remplacés"),
    )



    # ==========================================================
    # DIAGNOSTIC
    # ==========================================================

    diagnostic_effectue = models.BooleanField(
        default=False,
        verbose_name=_("Diagnostic du système d'injection effectué"),
    )

    code_defaut = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Codes défaut"),
    )

    resultat_diagnostic = models.TextField(
        blank=True,
        verbose_name=_("Résultat du diagnostic"),
    )

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
        related_name="injection"
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
        related_name="injection"
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
        related_name="injection",
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

        if self.voiture_exemplaire and self.kilometrage_injection is not None:
            if self.kilometrage_injection < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_injection": _(
                        "Le kilométrage du controle injection ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })


    class Meta:
        verbose_name = _("Injection")
        verbose_name_plural = _("Injections")
        ordering = ["-id"]

    def __str__(self):
        if self.voiture_exemplaire:
            return f"{_('Injection')} - {self.voiture_exemplaire}"
        return str(_("Injection"))

    # -------------------------
    # CALCUL GENERIQUE
    # -------------------------
    def calcul_piece(self, prefix):
        prix = getattr(self, f"{prefix}_prix", 0)
        quantite = getattr(self, f"{prefix}_quantite", 0)

        if not prix or not self.pays:
            return

        tva_rate = Decimal(self.TVA_PIECES.get(self.pays, 0)) / 100

        prix_htva = prix  # pas de marge dans ton modèle

        prix_htva = prix_htva.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        tva = (prix_htva * tva_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        prix_ttc = prix_htva + tva

        setattr(self, f"{prefix}_prix_vente_htva", prix_htva)
        setattr(self, f"{prefix}_tva_vente", tva)
        setattr(self, f"{prefix}_prix_ttc", prix_ttc)

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):



        # Calculs
        self.calcul_piece("pompe_carburant")
        self.calcul_piece("pompe_haute_pression")
        self.calcul_piece("rampe_injection")
        self.calcul_piece("capteur_pression_rampe")
        self.calcul_piece("tuyaux_haute_pression")
        self.calcul_piece("injecteurs")
        self.calcul_piece("connecteurs_injecteurs")

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
                        ancien_objet.kilometrage_injection
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
        if self.kilometrage_injection is not None:

            self.kilometrage_variation = (
                    self.kilometrage_injection
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_injection
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
                    _("Controle Injection")
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
                Maintenance.TypeMaintenance.INJECTION
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_injection is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_injection
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
                and self.kilometrage_injection is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_injection
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

        pieces = [
            ("pompe_carburant", _("Pompe à carburant")),
            ("pompe_haute_pression", _("Pompe haute pression")),
            ("rampe_injection", _("Rampe d'injection")),
            ("capteur_pression_rampe", _("Capteur de pression de rampe")),
            ("tuyaux_haute_pression", _("Tuyaux haute pression")),
            ("injecteurs", _("Injecteurs")),
            ("nettoyage_injecteurs", _("Nettoyage des injecteurs")),
            ("connecteurs_injecteurs", _("Connecteurs d'injecteurs")),
        ]

        for prefix, label in pieces:

            # ==================================================
            # ÉTAT
            # ==================================================

            etat = getattr(
                self,
                f"{prefix}_etat",
                None,
            )

            if etat not in [
                EtatInjection.NOT_OK,
                EtatInjection.REMPLACE,
                EtatInjection.NETTOYE,
            ]:
                continue

            # ==================================================
            # LIBELLÉ ÉTAT
            # ==================================================

            etat_label = dict(
                EtatInjection.choices
            ).get(
                etat,
                etat,
            )

            # ==================================================
            # FABRICANT
            # ==================================================

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

            # ==================================================
            # PRIX
            # ==================================================

            prix = getattr(
                self,
                f"{prefix}_prix",
                Decimal("0.00"),
            )

            if prix is None:
                prix = Decimal("0.00")

            prix = Decimal(str(prix))

            # ==================================================
            # QUANTITÉ
            # ==================================================

            quantite = getattr(
                self,
                f"{prefix}_quantite",
                0,
            )

            if quantite is None:
                quantite = 0

            quantite = Decimal(str(quantite))

            # Ne pas afficher une pièce sans quantité
            if quantite <= 0:
                continue

            # ==================================================
            # TOTAL
            # ==================================================

            total = prix * quantite
            total_general += total

            # ==================================================
            # RAPPORT
            # ==================================================

            rapport.append({
                "champ": label,
                "code": prefix,

                "etat": etat,
                "etat_label": etat_label,

                "fabricant": fabricant,
                "fabricant_label": fabricant_label,

                "prix": prix,
                "quantite": quantite,
                "total": total,
            })

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

        if self.kilometrage_injection is None:
            return

        km = Decimal(str(self.kilometrage_injection))

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

