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
    AJOUTER = "AJOUTER", _("Ajouté")


class EtatOptionnel(models.TextChoices):
    """Opération optionnelle (calibrage, diagnostic…)."""
    NON_PRESENT = "NON_PRESENT", _("Non présent")
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    AJOUTER = "AJOUTER", _("Ajouté")




class EtatDemontage(models.TextChoices):
    """Démontage / allègement."""
    NON_CONCERNE = "NON_CONCERNE", _("Non concerné")
    DEMONTE = "DEMONTE", _("Démonté")
    REMONTE = "REMONTE", _("Remonté")
    SUPPRIME = "SUPPRIME", _("Supprimé définitivement")


class TypeExtincteur(models.TextChoices):
    MANUEL = "MANUEL", _("Extincteur manuel")
    PLOMBE = "PLOMBE", _("Système d'extinction plombé (automatique)")
    LES_DEUX = "LES_DEUX", _("Système plombé + extincteur manuel")


class NormeExtincteur(models.TextChoices):
    FIA_8865_2015 = "FIA_8865_2015", _("FIA 8865-2015 (liste technique n°52)")
    LISTE_TECH_16 = "LISTE_TECH_16", _("Liste technique FIA n°16 (anciens systèmes homologués)")
    ANNEXE_J_253_7 = "ANNEXE_J_253_7", _("Annexe J – Art. 253-7 (extincteur manuel)")
    NON_CONFORME = "NON_CONFORME", _("Non conforme FIA / usage route")


class AgentExtincteur(models.TextChoices):
    AFFF = "AFFF", _("AFFF (mousse)")
    POUDRE = "POUDRE", _("Poudre")
    NOVEC = "NOVEC", _("Novec 1230 (FK-5-1-12)")
    ZERO_2000 = "ZERO_2000", _("Zero 2000")
    FX_GTEC = "FX_GTEC", _("FX G-TEC")
    VIRO3 = "VIRO3", _("Viro3")
    AUTRE = "AUTRE", _("Autre")


class DeclenchementExtincteur(models.TextChoices):
    SANS = "SANS", _("Sans déclencheur (manuel)")
    MECANIQUE = "MECANIQUE", _("Mécanique (câble)")
    ELECTRIQUE = "ELECTRIQUE", _("Électrique")


PIECES = [
    ("bouteille_extincteur", _("Bouteille / réservoir")),
    ("tuyaux_buses", _("Tuyaux et buses")),
    ("declencheur_interieur", _("Déclencheur intérieur")),
    ("declencheur_exterieur", _("Déclencheur extérieur")),
    ("fixations_extincteur", _("Supports de fixation (colliers métalliques)")),
    ("extincteur_manuel", _("Extincteur manuel")),
    ("pesee_charge", _("Pesée / contrôle de charge")),
    ("revision_extincteur", _("Recharge / révision")),
]


class Extincteur(TechnicienMixin, models.Model):



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
        related_name="pc_extincteur",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="pc_extincteur",
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
    kilometrage_pc_extincteur = models.PositiveIntegerField(
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
    type_extincteur = models.CharField(max_length=40, choices=TypeExtincteur.choices, default=TypeExtincteur.PLOMBE, verbose_name=_("Type de système"))
    norme_extincteur = models.CharField(max_length=40, choices=NormeExtincteur.choices, default=NormeExtincteur.FIA_8865_2015, verbose_name=_("Norme / homologation"), help_text=_("Voir la réglementation FIA (Annexe J, article 253-7) et le règlement de la discipline."))
    agent_extincteur = models.CharField(max_length=40, choices=AgentExtincteur.choices, default=AgentExtincteur.AFFF, verbose_name=_("Agent extincteur"))
    capacite_extincteur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Capacité (kg ou litres)"))
    declenchement = models.CharField(max_length=40, choices=DeclenchementExtincteur.choices, default=DeclenchementExtincteur.ELECTRIQUE, verbose_name=_("Déclenchement"))
    numero_homologation = models.CharField(max_length=100, blank=True, verbose_name=_("Numéro d'homologation"))
    date_fabrication = models.DateField(null=True, blank=True, verbose_name=_("Date de fabrication / dernier remplissage"))
    date_validite = models.DateField(null=True, blank=True, verbose_name=_("Date de validité (prochaine révision)"), help_text=_("Contrôle / révision périodique selon le fabricant et la FIA (en général tous les 2 ans)."))

    # -------------------------
    # COMPOSANTS
    # -------------------------
    # Bouteille / réservoir
    bouteille_extincteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Bouteille / réservoir"))
    bouteille_extincteur_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    bouteille_extincteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    bouteille_extincteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Tuyaux et buses
    tuyaux_buses = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Tuyaux et buses"))
    tuyaux_buses_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    tuyaux_buses_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    tuyaux_buses_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Déclencheur intérieur
    declencheur_interieur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Déclencheur intérieur"))
    declencheur_interieur_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    declencheur_interieur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    declencheur_interieur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Déclencheur extérieur
    declencheur_exterieur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Déclencheur extérieur"))
    declencheur_exterieur_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    declencheur_exterieur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    declencheur_exterieur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Supports de fixation (colliers métalliques)
    fixations_extincteur = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Supports de fixation (colliers métalliques)"))
    fixations_extincteur_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    fixations_extincteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    fixations_extincteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Extincteur manuel
    extincteur_manuel = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Extincteur manuel"))
    extincteur_manuel_fabricant = models.CharField(max_length=30, choices=FabricantCourse.choices, default=FabricantCourse.CHOISIR, verbose_name=_("Fabricant / marque"), blank=True)
    extincteur_manuel_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    extincteur_manuel_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Pesée / contrôle de charge
    pesee_charge = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Pesée / contrôle de charge"))
    pesee_charge_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    pesee_charge_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))

    # Recharge / révision
    revision_extincteur = models.CharField(max_length=25, choices=EtatOptionnel.choices, default=EtatOptionnel.NON_PRESENT, verbose_name=_("Recharge / révision"))
    revision_extincteur_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    revision_extincteur_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))


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
        related_name="pc_extincteur"
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
        related_name="pc_extincteur"
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
        related_name="pc_extincteur",
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

        if self.voiture_exemplaire and self.kilometrage_pc_extincteur is not None:
            if self.kilometrage_pc_extincteur < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_pc_extincteur": _(
                        "Le kilométrage ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

    class Meta:
        verbose_name = _("Extincteur")
        verbose_name_plural = _("Extincteur")

    def __str__(self):
        return f"Extincteur - {self.voiture_exemplaire}"



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
        # ANCIEN KM EXTINCTEUR
        # =========================
        ancien_kilometrage = 0

        if self.pk:

            ancien_objet = type(self).objects.filter(
                pk=self.pk
            ).first()

            if ancien_objet:
                ancien_kilometrage = (
                        ancien_objet.kilometrage_pc_extincteur
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
        if self.kilometrage_pc_extincteur is not None:

            self.kilometrage_variation = (
                    self.kilometrage_pc_extincteur
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km pc_extincteur
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_pc_extincteur
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
                    _("Extincteur")
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
                Maintenance.TypeMaintenance.PC_EXTINCTEUR
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_pc_extincteur is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_pc_extincteur
                )

            self.maintenance.save(
                update_fields=[
                    "type_maintenance",
                    "voiture_exemplaire",
                    "kilometres_chassis",
                ]
            )

        # =========================
        # SAVE EXTINCTEUR
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
                and self.kilometrage_pc_extincteur is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_pc_extincteur
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
                EtatOKNotOK.AJOUTER,
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

        if self.kilometrage_pc_extincteur is None:
            return

        km = Decimal(str(self.kilometrage_pc_extincteur))

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