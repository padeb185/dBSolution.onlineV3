from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantFrein, TVAConfig, RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")
    NETTOYER = "NETTOYER", _("Nettoyé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


PIECES_NETTOYAGE_FREINS = [
    ("disques_avant", _("Disques avant")),
    ("plaquettes_avant", _("Plaquettes avant")),
    ("etriers_avant", _("Étriers avant")),
    ("disques_arriere", _("Disques arrière")),
    ("plaquettes_arriere", _("Plaquettes arrière")),
    ("etriers_arriere", _("Étriers arrière")),
    ("tambours_arriere", _("Tambours arrière")),
    ("glissieres", _("Glissières / colonnettes d'étriers")),
    ("ressorts_anti_bruit", _("Ressorts / clips anti-bruit")),
    ("cache_poussiere", _("Soufflets / cache-poussière")),
    ("nettoyant_freins", _("Nettoyant freins")),
    ("graisse_freins", _("Graisse spéciale freins")),
]


class NettoyageFreins(TechnicienMixin, models.Model):



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
        related_name="nettoyage_freins",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="nettoyage_freins",
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
    kilometrage_nettoyage_freins = models.PositiveIntegerField(
        verbose_name= _("Kilométrage du nettoyage des freins")
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
    # CONTRÔLES ET MESURES
    # -------------------------
    controle_produit = models.CharField(max_length=60, blank=True, default="", verbose_name=_("Produit nettoyant utilisé"))
    controle_roues_demontees = models.BooleanField(default=False, verbose_name=_("Roues démontées"))
    controle_avant = models.BooleanField(default=False, verbose_name=_("Freins avant nettoyés"))
    controle_arriere = models.BooleanField(default=False, verbose_name=_("Freins arrière nettoyés"))
    controle_glissieres_graissees = models.BooleanField(default=False, verbose_name=_("Glissières graissées (graisse spéciale freins)"))
    controle_essai = models.BooleanField(default=False, verbose_name=_("Essai de freinage effectué"))

    # -------------------------
    # AVANT
    # -------------------------
    disques_avant_epaisseur = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    disques_avant_fentes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes"))
    disques_avant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques avant"))
    disques_avant_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    disques_avant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    disques_avant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    plaquettes_avant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes avant"))
    plaquettes_avant_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    plaquettes_avant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    plaquettes_avant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    etriers_avant = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Étriers avant"))
    etriers_avant_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    etriers_avant_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    etriers_avant_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # ARRIÈRE
    # -------------------------
    disques_arriere_epaisseur = models.FloatField(default=0.0, verbose_name=_("Épaisseur des disques avant (mm)"))
    disques_arriere_fentes = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK,verbose_name=_("Présence de fentes"))
    disques_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Disques arrière"))
    disques_arriere_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    disques_arriere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    disques_arriere_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    plaquettes_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Plaquettes arrière"))
    plaquettes_arriere_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    plaquettes_arriere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    plaquettes_arriere_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    etriers_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Étriers arrière"))
    etriers_arriere_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    etriers_arriere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    etriers_arriere_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    tambours_arriere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.NON_PRESENT, verbose_name=_("Tambours arrière"))
    tambours_arriere_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    tambours_arriere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    tambours_arriere_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # ACCESSOIRES
    # -------------------------
    glissieres = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Glissières / colonnettes d'étriers"))
    glissieres_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    glissieres_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    glissieres_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    ressorts_anti_bruit = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Ressorts / clips anti-bruit"))
    ressorts_anti_bruit_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    ressorts_anti_bruit_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    ressorts_anti_bruit_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    cache_poussiere = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Soufflets / cache-poussière"))
    cache_poussiere_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    cache_poussiere_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    cache_poussiere_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    # -------------------------
    # PRODUITS
    # -------------------------
    nettoyant_freins = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Nettoyant freins"))
    nettoyant_freins_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    nettoyant_freins_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    nettoyant_freins_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

    graisse_freins = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Graisse spéciale freins"))
    graisse_freins_fabricant = models.CharField(max_length=30, choices=FabricantFrein.choices, default=FabricantFrein.CHOISIR, verbose_name=_("Fabricant"))
    graisse_freins_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    graisse_freins_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))



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
        related_name="nettoyage_freins"
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
        related_name="nettoyage_freins"
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
        related_name="nettoyage_freins",
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

        if self.voiture_exemplaire and self.kilometrage_nettoyage_freins is not None:
            if self.kilometrage_nettoyage_freins < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_nettoyage_freins": _(
                        "Le kilométrage du nettoyage des freins ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Nettoyage des freins")
        verbose_name_plural = _("Nettoyage des freins")

    def __str__(self):
        return f"Nettoyage des freins - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_NETTOYAGE_FREINS:
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
        # ANCIEN KM ADMISSION
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_nettoyage_freins
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
        if self.kilometrage_nettoyage_freins is not None:

            self.kilometrage_variation = (
                    self.kilometrage_nettoyage_freins
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_nettoyage_freins
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
                    _("Nettoyage des freins")
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
                Maintenance.TypeMaintenance.NETTOYAGE_FREINS
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_nettoyage_freins is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_nettoyage_freins
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
                and self.kilometrage_nettoyage_freins is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_nettoyage_freins
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

        pieces = PIECES_NETTOYAGE_FREINS

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
                        EtatOKNotOK.choices
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

        if self.kilometrage_nettoyage_freins is None:
            return

        km = Decimal(str(self.kilometrage_nettoyage_freins))

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