from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import RefroidissementFabricant, FabricantPiece, FabricantLubrifiant, HuileEtat, TVAConfig, \
    RouesSerrageEtat, RefroidissementQualiteEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


class EtatCulbuteur(models.TextChoices):
    """Tiges de culbuteur / culbuteurs : absents sur la plupart des moteurs modernes."""
    NON_PRESENT = "NON_PRESENT", _("Non présent")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


PIECES_CULASSE = [
    ("culasse", _("Culasse")),
    ("joint_culasse", _("Joint de culasse")),
    ("jeu_soupapes", _("Jeu aux soupapes")),
    ("guides_soupapes", _("Guides de soupapes")),
    ("soupapes", _("Soupapes")),
    ("ressorts_soupapes", _("Ressorts de soupapes")),
    ("clavettes_soupapes", _("Clavettes de soupapes")),
    ("sieges_soupapes", _("Sièges de soupapes")),
    ("rodage_soupapes", _("Rodage des soupapes")),
    ("arbre_cames_echappement", _("Arbre à cames d'échappement")),
    ("arbre_cames_admission", _("Arbre à cames d'admission")),
    ("planage_culasse", _("Planage de la culasse")),
    ("poussoirs_hydrauliques", _("Poussoirs hydrauliques")),
    ("tiges_culbuteur", _("Tiges de culbuteur")),
    ("culbuteurs", _("Culbuteurs")),
    ("huile_moteur", _("Huile moteur")),
    ("refroidissement", _("Liquide de refroidissement")),
]


class Culasse(TechnicienMixin, models.Model):



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
        related_name="culasse",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="culasse",
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
    kilometrage_culasse = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de la culasse")
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
            f"{prefix}_quantite": models.IntegerField(default=0),
        }




    # -------------------------
    # CULASSE
    # -------------------------
    culasse = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Culasse"))
    culasse_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    culasse_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    culasse_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    joint_culasse = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Joint de culasse"))
    joint_culasse_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    joint_culasse_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    joint_culasse_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    jeu_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Jeu aux soupapes"))
    jeu_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    jeu_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    jeu_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    guides_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Guides de soupapes"))
    guides_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    guides_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    guides_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Soupapes"))
    soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    ressorts_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Ressorts de soupapes"))
    ressorts_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    ressorts_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    ressorts_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    clavettes_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Clavettes de soupapes"))
    clavettes_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    clavettes_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    clavettes_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    sieges_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Sièges de soupapes"))
    sieges_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    sieges_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    sieges_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    rodage_soupapes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Rodage des soupapes"))
    rodage_soupapes_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    rodage_soupapes_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    rodage_soupapes_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    arbre_cames_echappement = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Arbre à cames d'échappement"))
    arbre_cames_echappement_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    arbre_cames_echappement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    arbre_cames_echappement_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    arbre_cames_admission = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Arbre à cames d'admission"))
    arbre_cames_admission_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    arbre_cames_admission_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    arbre_cames_admission_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    planage_culasse = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Planage de la culasse"))
    planage_culasse_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    planage_culasse_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    planage_culasse_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    poussoirs_hydrauliques = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Poussoirs hydrauliques"))
    poussoirs_hydrauliques_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    poussoirs_hydrauliques_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    poussoirs_hydrauliques_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    tiges_culbuteur = models.CharField(max_length=25, choices=EtatCulbuteur.choices, default=EtatCulbuteur.NON_PRESENT, verbose_name=_("Tiges de culbuteur"))
    tiges_culbuteur_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    tiges_culbuteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    tiges_culbuteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    culbuteurs = models.CharField(max_length=25, choices=EtatCulbuteur.choices, default=EtatCulbuteur.NON_PRESENT, verbose_name=_("Culbuteurs"))
    culbuteurs_fabricant = models.CharField(
        max_length=30,
        choices=FabricantPiece.choices,
        default=FabricantPiece.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    culbuteurs_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    culbuteurs_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # HUILE MOTEUR
    # -------------------------
    huile_moteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Huile moteur"))
    huile_moteur_fabricant = models.CharField(max_length=30, choices=FabricantLubrifiant.choices, default=FabricantLubrifiant.CHOISIR, verbose_name=_("Fabricant"))
    huile_moteur_qualite = models.CharField(max_length=25, choices=HuileEtat.choices, default=HuileEtat.CHOISIR, verbose_name=_("Viscosité de l'huile moteur"))
    huile_moteur_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    huile_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA par litre"))

    # -------------------------
    # LIQUIDE DE REFROIDISSEMENT
    # -------------------------
    refroidissement = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Liquide de refroidissement"))
    refroidissement_fabricant = models.CharField(max_length=25, choices=RefroidissementFabricant.choices, default=RefroidissementFabricant.CHOISIR, verbose_name=_("Fabricant"))
    refroidissement_qualite = models.CharField(max_length=25, choices=RefroidissementQualiteEtat.choices, default=RefroidissementQualiteEtat.G13, verbose_name=_("Qualité de liquide de refroidissement"))
    refroidissement_quantite = models.DecimalField(default=0.0, max_digits=4, decimal_places=1, verbose_name=_("Quantité ajoutée en litres"), validators=[StepValueValidator(0.1)])
    refroidissement_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA par litre"))

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
        related_name="culasse"
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
        related_name="culasse"
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
        related_name="culasse",
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

        if self.voiture_exemplaire and self.kilometrage_culasse is not None:
            if self.kilometrage_culasse < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_culasse": _(
                        "Le kilométrage de la culasse ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Culasse")
        verbose_name_plural = _("Culasses")

    def __str__(self):
        return f"Culasse - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_CULASSE:
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
        # ANCIEN KM CULASSE
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_culasse
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
        if self.kilometrage_culasse is not None:

            self.kilometrage_variation = (
                    self.kilometrage_culasse
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km culasse
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_culasse
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
                    _("Culasse")
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
                Maintenance.TypeMaintenance.CULASSE
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_culasse is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_culasse
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE CULASSE
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
                and self.kilometrage_culasse is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_culasse
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

        pieces = PIECES_CULASSE

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

        if self.kilometrage_culasse is None:
            return

        km = Decimal(str(self.kilometrage_culasse))

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