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


PIECES_FUSIBLES = [
    ("boite_fusibles_moteur", _("Boîte à fusibles compartiment moteur")),
    ("boite_fusibles_habitacle", _("Boîte à fusibles habitacle (côté conducteur)")),
    ("boite_fusibles_coffre", _("Boîte à fusibles coffre / arrière")),
    ("fusibles_lame", _("Fusibles à lame (standard)")),
    ("mini_fusibles", _("Mini-fusibles")),
    ("maxi_fusibles", _("Maxi-fusibles")),
    ("mega_fusibles", _("Méga-fusibles (fusibles à vis)")),
    ("relais_fusibles", _("Relais")),
    ("controle_fusibles", _("Contrôle des fusibles (test de continuité)")),
]


class Fusibles(TechnicienMixin, models.Model):



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
        related_name="fusibles_fusibles",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="fusibles_fusibles",
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
    kilometrage_fusibles = models.PositiveIntegerField(
        verbose_name=_("Kilométrage de l'intervention")
    )

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )


    # -------------------------
    # PIÈCES : BOÎTES À FUSIBLES, FUSIBLES, RELAIS
    # -------------------------
    # Boîte à fusibles compartiment moteur
    boite_fusibles_moteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Boîte à fusibles compartiment moteur"))
    boite_fusibles_moteur_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    boite_fusibles_moteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    boite_fusibles_moteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Boîte à fusibles habitacle (côté conducteur)
    boite_fusibles_habitacle = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Boîte à fusibles habitacle (côté conducteur)"))
    boite_fusibles_habitacle_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    boite_fusibles_habitacle_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    boite_fusibles_habitacle_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Boîte à fusibles coffre / arrière
    boite_fusibles_coffre = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Boîte à fusibles coffre / arrière"))
    boite_fusibles_coffre_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    boite_fusibles_coffre_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    boite_fusibles_coffre_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Fusibles à lame (standard)
    fusibles_lame = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Fusibles à lame (standard)"))
    fusibles_lame_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    fusibles_lame_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    fusibles_lame_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Mini-fusibles
    mini_fusibles = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Mini-fusibles"))
    mini_fusibles_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    mini_fusibles_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    mini_fusibles_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Maxi-fusibles
    maxi_fusibles = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Maxi-fusibles"))
    maxi_fusibles_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    maxi_fusibles_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    maxi_fusibles_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Méga-fusibles (fusibles à vis)
    mega_fusibles = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Méga-fusibles (fusibles à vis)"))
    mega_fusibles_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    mega_fusibles_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    mega_fusibles_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Relais
    relais_fusibles = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Relais"))
    relais_fusibles_fabricant = models.CharField(max_length=30, choices=FabricantPiece.choices, default=FabricantPiece.CHOISIR, verbose_name=_("Fabricant"), blank=True)
    relais_fusibles_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    relais_fusibles_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Contrôle des fusibles (test de continuité)
    controle_fusibles = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Contrôle des fusibles (test de continuité)"))
    controle_fusibles_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    controle_fusibles_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


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
        related_name="fusibles_fusibles"
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
        related_name="fusibles_fusibles"
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
        related_name="fusibles_fusibles",
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

        if self.voiture_exemplaire and self.kilometrage_fusibles is not None:
            if self.kilometrage_fusibles < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_fusibles": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Boîtes à fusibles")
        verbose_name_plural = _("Boîtes à fusibles")

    def __str__(self):
        return f"Boîtes à fusibles - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_FUSIBLES:
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
        # ANCIEN KM FUSIBLES
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_fusibles
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
        if self.kilometrage_fusibles is not None:

            self.kilometrage_variation = (
                    self.kilometrage_fusibles
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km fusibles
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_fusibles
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
                    _("Boîtes à fusibles")
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
                Maintenance.TypeMaintenance.FUSIBLES
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_fusibles is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_fusibles
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE FUSIBLES
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
                and self.kilometrage_fusibles is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_fusibles
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

        pieces = PIECES_FUSIBLES

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

        if self.kilometrage_fusibles is None:
            return

        km = Decimal(str(self.kilometrage_fusibles))

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

# =====================================================================
# DÉTAIL DES FUSIBLES : boîte (emplacement), repère, ampérage, organe protégé
# =====================================================================
class EmplacementBoiteFusibles(models.TextChoices):
    MOTEUR = "MOTEUR", _("Compartiment moteur")
    CONDUCTEUR = "CONDUCTEUR", _("Habitacle – côté conducteur")
    PASSAGER = "PASSAGER", _("Habitacle – côté passager")
    COFFRE = "COFFRE", _("Coffre / arrière")
    BATTERIE = "BATTERIE", _("Sur la batterie (pôle +)")
    AUTRE = "AUTRE", _("Autre emplacement")


class TypeFusible(models.TextChoices):
    LAME = "LAME", _("Fusible à lame (standard)")
    MINI = "MINI", _("Mini-fusible")
    MICRO = "MICRO", _("Micro-fusible")
    MAXI = "MAXI", _("Maxi-fusible")
    MEGA = "MEGA", _("Méga-fusible (à vis)")
    CARTOUCHE = "CARTOUCHE", _("Fusible cartouche (J-case)")
    RELAIS = "RELAIS", _("Relais")


class EtatFusible(models.TextChoices):
    OK = "OK", _("OK")
    GRILLE = "GRILLE", _("Grillé")
    REMPLACE = "REMPLACE", _("Remplacé")


class CircuitFusible(models.TextChoices):
    """Circuit protégé par le fusible (liste ; « Autre » + précision libre)."""
    VIDE = "", "---------"
    # Éclairage
    PHARE_AVG = "PHARE_AVG", _("Phare avant gauche")
    PHARE_AVD = "PHARE_AVD", _("Phare avant droit")
    CODE_G = "CODE_G", _("Feu de croisement gauche")
    CODE_D = "CODE_D", _("Feu de croisement droit")
    ROUTE_G = "ROUTE_G", _("Feu de route gauche")
    ROUTE_D = "ROUTE_D", _("Feu de route droit")
    ANTIBROUILLARD_AV = "ANTIBROUILLARD_AV", _("Antibrouillards avant")
    ANTIBROUILLARD_AR = "ANTIBROUILLARD_AR", _("Antibrouillard arrière")
    POSITION_G = "POSITION_G", _("Feux de position gauche")
    POSITION_D = "POSITION_D", _("Feux de position droit")
    FEUX_AR_G = "FEUX_AR_G", _("Feu arrière gauche")
    FEUX_AR_D = "FEUX_AR_D", _("Feu arrière droit")
    STOP = "STOP", _("Feux stop")
    CLIGNOTANTS = "CLIGNOTANTS", _("Clignotants / feux de détresse")
    RECUL = "RECUL", _("Feux de recul")
    PLAQUE = "PLAQUE", _("Éclairage de plaque")
    PLAFONNIER = "PLAFONNIER", _("Plafonnier / éclairage intérieur")
    # Moteur
    CALCULATEUR_MOTEUR = "CALCULATEUR_MOTEUR", _("Calculateur moteur")
    INJECTION = "INJECTION", _("Injection / injecteurs")
    POMPE_CARBURANT = "POMPE_CARBURANT", _("Pompe à carburant")
    ALLUMAGE = "ALLUMAGE", _("Bobines d'allumage")
    PRECHAUFFAGE = "PRECHAUFFAGE", _("Bougies de préchauffage")
    DEMARREUR = "DEMARREUR", _("Démarreur")
    ALTERNATEUR = "ALTERNATEUR", _("Alternateur / charge")
    VENTILATEUR_MOTEUR = "VENTILATEUR_MOTEUR", _("Ventilateur de refroidissement")
    SONDES_LAMBDA = "SONDES_LAMBDA", _("Sondes lambda (chauffage)")
    # Châssis / sécurité
    ABS_ESP = "ABS_ESP", _("ABS / ESP")
    DIRECTION_ASSISTEE = "DIRECTION_ASSISTEE", _("Direction assistée")
    AIRBAGS = "AIRBAGS", _("Airbags")
    BOITE_AUTO = "BOITE_AUTO", _("Boîte de vitesses automatique")
    FREIN_PARKING = "FREIN_PARKING", _("Frein de parking électrique")
    # Habitacle / confort
    TABLEAU_BORD = "TABLEAU_BORD", _("Tableau de bord / instruments")
    AUTORADIO = "AUTORADIO", _("Autoradio / multimédia")
    ALLUME_CIGARE = "ALLUME_CIGARE", _("Allume-cigare / prise 12 V")
    PRISES_USB = "PRISES_USB", _("Prises USB")
    CLIMATISATION = "CLIMATISATION", _("Climatisation")
    VENTILATION = "VENTILATION", _("Ventilation / pulseur d'air")
    VITRES_AV = "VITRES_AV", _("Lève-vitres avant")
    VITRES_AR = "VITRES_AR", _("Lève-vitres arrière")
    VERROUILLAGE = "VERROUILLAGE", _("Verrouillage centralisé")
    RETROVISEURS = "RETROVISEURS", _("Rétroviseurs électriques")
    SIEGES_CHAUFFANTS = "SIEGES_CHAUFFANTS", _("Sièges chauffants")
    SIEGES_ELECTRIQUES = "SIEGES_ELECTRIQUES", _("Sièges électriques")
    TOIT_OUVRANT = "TOIT_OUVRANT", _("Toit ouvrant")
    ESSUIE_GLACE_AV = "ESSUIE_GLACE_AV", _("Essuie-glace avant")
    ESSUIE_GLACE_AR = "ESSUIE_GLACE_AR", _("Essuie-glace arrière")
    LAVE_GLACE = "LAVE_GLACE", _("Lave-glace")
    DEGIVRAGE_AR = "DEGIVRAGE_AR", _("Dégivrage lunette arrière")
    PARE_BRISE_CHAUFFANT = "PARE_BRISE_CHAUFFANT", _("Pare-brise chauffant")
    KLAXON = "KLAXON", _("Avertisseur sonore (klaxon)")
    ALARME = "ALARME", _("Alarme / antidémarrage")
    ATTELAGE = "ATTELAGE", _("Attelage / prise remorque")
    BATTERIE = "BATTERIE", _("Alimentation batterie (principal)")
    AUTRE = "AUTRE", _("Autre (préciser)")


# Ampérages normalisés (code couleur des fusibles automobiles)
AMPERAGES_FUSIBLES = ["1", "2", "3", "4", "5", "7.5", "10", "15", "20", "25", "30", "35", "40", "50", "60",
                      "70", "80", "100", "125", "150", "175", "200", "250", "300"]


class FusibleDetail(models.Model):
    intervention = models.ForeignKey(Fusibles, on_delete=models.CASCADE, related_name="detail_fusibles",
                                     verbose_name=_("Intervention"))
    emplacement = models.CharField(max_length=12, choices=EmplacementBoiteFusibles.choices,
                                   default=EmplacementBoiteFusibles.MOTEUR, verbose_name=_("Emplacement de la boîte"))
    repere = models.CharField(max_length=20, blank=True, verbose_name=_("Numéro sur la boîte (F12, SB3…)"))
    circuit = models.CharField(max_length=30, choices=CircuitFusible.choices, blank=True, default="",
                               verbose_name=_("Circuit protégé"))
    type_fusible = models.CharField(max_length=10, choices=TypeFusible.choices, default=TypeFusible.LAME,
                                    verbose_name=_("Type"))
    amperage = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True,
                                   verbose_name=_("Ampérage (A)"))
    organe = models.CharField(max_length=150, blank=True, verbose_name=_("Précision"))
    etat = models.CharField(max_length=10, choices=EtatFusible.choices, default=EtatFusible.OK,
                            verbose_name=_("État"))
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "id"]
        verbose_name = _("Fusible")
        verbose_name_plural = _("Fusibles")

    @property
    def circuit_affiche(self):
        """« Phare avant droit », « Autre : prise remorque », ou la précision seule."""
        if self.circuit and self.circuit != CircuitFusible.AUTRE:
            return self.get_circuit_display() + (f" ({self.organe})" if self.organe else "")
        return self.organe or (self.get_circuit_display() if self.circuit else "")

    def __str__(self):
        a = f" {self.amperage_affiche} A" if self.amperage is not None else ""
        return f"{self.repere or self.get_type_fusible_display()}{a} – {self.circuit_affiche}"

    @property
    def amperage_affiche(self):
        if self.amperage is None:
            return ""
        return format(self.amperage.normalize(), "f")


# Type de fusible → ligne de pièce facturée (quantité = nombre de fusibles remplacés de ce type)
LIGNE_PAR_TYPE = {
    TypeFusible.LAME: "fusibles_lame",
    TypeFusible.MINI: "mini_fusibles",
    TypeFusible.MICRO: "mini_fusibles",
    TypeFusible.MAXI: "maxi_fusibles",
    TypeFusible.CARTOUCHE: "maxi_fusibles",
    TypeFusible.MEGA: "mega_fusibles",
    TypeFusible.RELAIS: "relais_fusibles",
}


def synchroniser_quantites(intervention):
    """
    Pour chaque type présent dans le détail : quantité de la ligne facturée = nombre de fusibles remplacés
    (état « Remplacé »). La ligne passe à « Remplacé » si au moins un fusible a été remplacé.
    Les types absents du détail gardent la quantité saisie à la main.
    """
    lignes = list(intervention.detail_fusibles.all())
    if not lignes:
        return False
    compte = {}
    for l in lignes:
        prefixe = LIGNE_PAR_TYPE.get(l.type_fusible)
        if not prefixe:
            continue
        compte.setdefault(prefixe, 0)
        if l.etat == EtatFusible.REMPLACE:
            compte[prefixe] += 1
    change = False
    for prefixe, n in compte.items():
        if getattr(intervention, f"{prefixe}_quantite", None) != n:
            setattr(intervention, f"{prefixe}_quantite", n)
            change = True
        etat = getattr(intervention, prefixe, None)
        if n > 0 and etat != "REMPLACE":
            setattr(intervention, prefixe, "REMPLACE")
            change = True
        elif n == 0 and etat == "REMPLACE":
            setattr(intervention, prefixe, "OK")
            change = True
    if change:
        intervention.save()
    return change
