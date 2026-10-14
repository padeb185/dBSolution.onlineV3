from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import StepValueValidator, MaxValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from maintenance.choices import FabricantBatterie, TVAConfig, RouesSerrageEtat, TAUX_HORAIRE_CHOICES
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance







class EtatOKNotOK(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("A Remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")


PIECES_BATTERIE = [
    ("batterie_neuve", _("Batterie neuve")),
    ("cosses", _("Cosses / bornes")),
]


class TensionBatterie(models.IntegerChoices):
    V6 = 6, _("6 V")
    V12 = 12, _("12 V")
    V24 = 24, _("24 V")
    V48 = 48, _("48 V (hybride léger)")


class TechnologieBatterie(models.TextChoices):
    PLOMB = "PLOMB", _("Plomb-acide (standard)")
    EFB = "EFB", _("EFB (Start & Stop)")
    AGM = "AGM", _("AGM (Start & Stop)")
    GEL = "GEL", _("Gel")
    LITHIUM = "LITHIUM", _("Lithium (LiFePO4)")


# Niveau de technologie : une batterie de remplacement doit être de niveau égal ou supérieur
NIVEAU_TECHNOLOGIE = {"PLOMB": 0, "EFB": 1, "GEL": 2, "AGM": 2, "LITHIUM": 3}


class DiagnosticBatterie(models.TextChoices):
    NON_TESTE = "NON_TESTE", _("Non testée")
    BONNE = "BONNE", _("Bonne")
    A_RECHARGER = "A_RECHARGER", _("À recharger puis retester")
    FAIBLE = "FAIBLE", _("Faible – à surveiller")
    A_REMPLACER = "A_REMPLACER", _("À remplacer")


class CircuitCharge(models.TextChoices):
    NON_MESURE = "NON_MESURE", _("Non mesuré")
    OK = "OK", _("OK")
    SOUS_CHARGE = "SOUS_CHARGE", _("Sous-charge (alternateur / régulateur ?)")
    SURCHARGE = "SURCHARGE", _("Surcharge (régulateur ?)")


class Batterie(TechnicienMixin, models.Model):



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
        related_name="batterie",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="batterie",
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
    kilometrage_batterie = models.PositiveIntegerField(
        verbose_name= _("Kilométrage de la batterie")
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
    # 1. BATTERIE EN PLACE (plaque signalétique)
    # -------------------------
    actuelle_fabricant = models.CharField(max_length=30, choices=FabricantBatterie.choices, default=FabricantBatterie.CHOISIR, verbose_name=_("Fabricant de la batterie en place"))
    actuelle_technologie = models.CharField(max_length=10, choices=TechnologieBatterie.choices, default=TechnologieBatterie.PLOMB, verbose_name=_("Technologie"))
    actuelle_tension = models.PositiveSmallIntegerField(choices=TensionBatterie.choices, default=TensionBatterie.V12, verbose_name=_("Tension nominale (V)"))
    actuelle_capacite_ah = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(400)], verbose_name=_("Capacité (Ah)"))
    actuelle_cca = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(2000)], verbose_name=_("Courant de démarrage nominal (A EN)"))

    # -------------------------
    # 2. TEST / DIAGNOSTIC
    # -------------------------
    test_tension_repos = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Tension au repos (V)"), help_text=_("Moteur arrêté depuis au moins 1 h, consommateurs coupés."))
    test_tension_demarrage = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Tension minimale au démarrage (V)"))
    test_tension_charge = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name=_("Tension de charge moteur tournant (V)"))
    test_cca_mesure = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(2000)], verbose_name=_("Courant de démarrage mesuré au testeur (A EN)"))
    test_soh = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(100)], verbose_name=_("État de santé SOH (%)"), help_text=_("Valeur indiquée par le testeur, si disponible."))

    test_diagnostic = models.CharField(max_length=15, choices=DiagnosticBatterie.choices, default=DiagnosticBatterie.NON_TESTE, editable=False, verbose_name=_("Diagnostic"))
    test_circuit_charge = models.CharField(max_length=15, choices=CircuitCharge.choices, default=CircuitCharge.NON_MESURE, editable=False, verbose_name=_("Circuit de charge"))
    test_etat_charge = models.PositiveSmallIntegerField(null=True, blank=True, editable=False, verbose_name=_("État de charge estimé (%)"))
    test_detail = models.TextField(blank=True, default="", editable=False, verbose_name=_("Détail du diagnostic"))

    # -------------------------
    # 3. REMPLACEMENT
    # -------------------------
    batterie_neuve = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Batterie neuve"))
    batterie_neuve_fabricant = models.CharField(max_length=30, choices=FabricantBatterie.choices, default=FabricantBatterie.CHOISIR, verbose_name=_("Fabricant"))
    batterie_neuve_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    batterie_neuve_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))
    batterie_neuve_technologie = models.CharField(max_length=10, choices=TechnologieBatterie.choices, default=TechnologieBatterie.PLOMB, verbose_name=_("Technologie de la batterie neuve"))
    batterie_neuve_tension = models.PositiveSmallIntegerField(choices=TensionBatterie.choices, default=TensionBatterie.V12, verbose_name=_("Tension nominale de la batterie neuve (V)"))
    batterie_neuve_capacite_ah = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(400)], verbose_name=_("Capacité de la batterie neuve (Ah)"))
    batterie_neuve_cca = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(2000)], verbose_name=_("Courant de démarrage de la batterie neuve (A EN)"))
    batterie_neuve_enregistree = models.BooleanField(default=False, verbose_name=_("Batterie enregistrée / codée dans le véhicule (BMS)"), help_text=_("Obligatoire sur de nombreux véhicules Start & Stop (BMW, VAG, Mercedes…)."))

    cosses = models.CharField(max_length=25, choices=EtatOKNotOK.choices, default=EtatOKNotOK.OK, verbose_name=_("Cosses / bornes"))
    cosses_fabricant = models.CharField(max_length=30, choices=FabricantBatterie.choices, default=FabricantBatterie.CHOISIR, verbose_name=_("Fabricant"))
    cosses_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA"))
    cosses_quantite = models.IntegerField(default=0, verbose_name=_("Quantité"))

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
        related_name="batterie"
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
        related_name="batterie"
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
        related_name="batterie",
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

        if self.voiture_exemplaire and self.kilometrage_batterie is not None:
            if self.kilometrage_batterie < self.voiture_exemplaire.kilometres_chassis:
                raise ValidationError({
                    "kilometrage_batterie": _(
                        "Le kilométrage de la batterie ne peut pas être inférieur au kilométrage du véhicule."
                    )
                })

        self.normaliser_remplacement()
        self.verifier_compatibilite_remplacement()

    # ------------------------------------------------------------------
    # REMPLACEMENT : la batterie neuve doit convenir au véhicule
    # ------------------------------------------------------------------
    TECHNOLOGIES_ACCEPTEES = {
        "PLOMB": {"PLOMB", "EFB", "AGM"},
        "EFB": {"EFB", "AGM"},
        "AGM": {"AGM"},
        "GEL": {"GEL"},
        "LITHIUM": {"LITHIUM"},
    }

    def normaliser_remplacement(self):
        """
        Une batterie neuve (ou des cosses) dont le prix ou les caractéristiques
        sont saisis est forcément remplacée : l'état passe à « Remplacé » et la
        quantité à 1, pour qu'elle soit reprise dans le rapport et la facture.
        """
        neuve_saisie = bool(
            (self.batterie_neuve_prix or 0) > 0
            or self.batterie_neuve_capacite_ah
            or self.batterie_neuve_cca
        )
        if neuve_saisie and self.batterie_neuve == EtatOKNotOK.OK:
            self.batterie_neuve = EtatOKNotOK.REMPLACE
        if self.batterie_neuve == EtatOKNotOK.REMPLACE and not self.batterie_neuve_quantite:
            self.batterie_neuve_quantite = 1

        if (self.cosses_prix or 0) > 0 and self.cosses == EtatOKNotOK.OK:
            self.cosses = EtatOKNotOK.REMPLACE
        if self.cosses == EtatOKNotOK.REMPLACE and not self.cosses_quantite:
            self.cosses_quantite = 1

    def verifier_compatibilite_remplacement(self):
        if self.batterie_neuve != EtatOKNotOK.REMPLACE:
            return

        erreurs = {}

        if self.batterie_neuve_tension != self.actuelle_tension:
            erreurs["batterie_neuve_tension"] = _(
                "La tension doit être identique à celle de la batterie d'origine (%(v)s V)."
            ) % {"v": self.actuelle_tension}

        if not self.batterie_neuve_capacite_ah:
            erreurs["batterie_neuve_capacite_ah"] = _("Indiquez la capacité (Ah) de la batterie neuve.")
        elif self.actuelle_capacite_ah and self.batterie_neuve_capacite_ah < self.actuelle_capacite_ah:
            erreurs["batterie_neuve_capacite_ah"] = _(
                "La capacité doit être au moins égale à celle d'origine (%(ah)s Ah)."
            ) % {"ah": self.actuelle_capacite_ah}

        if not self.batterie_neuve_cca:
            erreurs["batterie_neuve_cca"] = _("Indiquez le courant de démarrage (A EN) de la batterie neuve.")
        elif self.actuelle_cca and self.batterie_neuve_cca < self.actuelle_cca:
            erreurs["batterie_neuve_cca"] = _(
                "Le courant de démarrage doit être au moins égal à celui d'origine (%(a)s A EN)."
            ) % {"a": self.actuelle_cca}

        acceptees = self.TECHNOLOGIES_ACCEPTEES.get(self.actuelle_technologie, {self.actuelle_technologie})
        if self.batterie_neuve_technologie not in acceptees:
            erreurs["batterie_neuve_technologie"] = _(
                "Technologie incompatible avec la batterie d'origine (%(orig)s). Technologies acceptées : %(ok)s."
            ) % {
                "orig": self.get_actuelle_technologie_display(),
                "ok": ", ".join(str(TechnologieBatterie(t).label) for t in sorted(acceptees)),
            }

        if erreurs:
            raise ValidationError(erreurs)

    # ------------------------------------------------------------------
    # DIAGNOSTIC À PARTIR DES MESURES
    # ------------------------------------------------------------------
    # Tension au repos d'une batterie plomb 12 V → état de charge
    COURBE_CHARGE_12V = [
        (Decimal("11.89"), 0), (Decimal("12.06"), 25), (Decimal("12.24"), 50),
        (Decimal("12.45"), 75), (Decimal("12.65"), 100),
    ]

    @classmethod
    def etat_de_charge(cls, tension_12v):
        points = cls.COURBE_CHARGE_12V
        if tension_12v <= points[0][0]:
            return 0
        if tension_12v >= points[-1][0]:
            return 100
        for (v1, p1), (v2, p2) in zip(points, points[1:]):
            if v1 <= tension_12v <= v2:
                return int(round(p1 + (p2 - p1) * float((tension_12v - v1) / (v2 - v1))))
        return None

    def calculer_diagnostic(self):
        facteur = Decimal(self.actuelle_tension or 12) / Decimal("12")
        notes = []
        remplacer = faible = recharger = False
        mesure = False
        soc = None

        # État de charge (tension au repos)
        if self.test_tension_repos:
            mesure = True
            if self.actuelle_technologie == TechnologieBatterie.LITHIUM:
                notes.append(_("Batterie lithium : l'état de charge ne se déduit pas de la tension au repos."))
            else:
                soc = self.etat_de_charge(Decimal(self.test_tension_repos) / facteur)
                notes.append(_("Tension au repos %(v)s V → état de charge estimé %(soc)s %%.") % {"v": self.test_tension_repos, "soc": soc})
                if soc is not None and soc < 75:
                    recharger = True
                    if soc == 0:
                        notes.append(_("Décharge profonde : recharger puis retester. Si la tension ne tient pas, remplacer."))
                    else:
                        notes.append(_("Batterie insuffisamment chargée : recharger avant de conclure."))

        # Courant de démarrage mesuré / nominal
        if self.test_cca_mesure is not None and self.actuelle_cca:
            mesure = True
            ratio = Decimal(self.test_cca_mesure) / Decimal(self.actuelle_cca) * 100
            ratio = int(ratio.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            notes.append(_("Courant de démarrage mesuré %(m)s A pour %(n)s A nominal (%(r)s %%).") % {"m": self.test_cca_mesure, "n": self.actuelle_cca, "r": ratio})
            if ratio < 60:
                remplacer = True
                notes.append(_("Moins de 60 % du courant nominal : batterie usée."))
            elif ratio < 80:
                faible = True
                notes.append(_("Entre 60 et 80 % du courant nominal : batterie faible."))

        # État de santé donné par le testeur
        if self.test_soh is not None:
            mesure = True
            if self.test_soh < 50:
                remplacer = True
                notes.append(_("État de santé %(soh)s %% : remplacement conseillé.") % {"soh": self.test_soh})
            elif self.test_soh < 70:
                faible = True
                notes.append(_("État de santé %(soh)s %% : batterie fatiguée.") % {"soh": self.test_soh})

        # Chute de tension au démarrage
        if self.test_tension_demarrage:
            mesure = True
            seuil = (Decimal("9.6") * facteur).quantize(Decimal("0.1"))
            if Decimal(self.test_tension_demarrage) < seuil:
                if soc is None or soc >= 75:
                    remplacer = True
                    notes.append(_("Tension au démarrage %(v)s V inférieure à %(s)s V avec une batterie chargée : batterie usée.") % {"v": self.test_tension_demarrage, "s": seuil})
                else:
                    recharger = True
                    notes.append(_("Tension au démarrage %(v)s V trop basse : recharger puis refaire le test.") % {"v": self.test_tension_demarrage})

        # Circuit de charge (moteur tournant)
        circuit = CircuitCharge.NON_MESURE
        if self.test_tension_charge:
            v = Decimal(self.test_tension_charge) / facteur
            if v < Decimal("13.2"):
                circuit = CircuitCharge.SOUS_CHARGE
                notes.append(_("Tension de charge %(v)s V trop basse : contrôler l'alternateur, la courroie et le régulateur (attention aux alternateurs pilotés).") % {"v": self.test_tension_charge})
            elif v > Decimal("14.9"):
                circuit = CircuitCharge.SURCHARGE
                notes.append(_("Tension de charge %(v)s V trop élevée : contrôler le régulateur.") % {"v": self.test_tension_charge})
            else:
                circuit = CircuitCharge.OK

        if not mesure:
            diagnostic = DiagnosticBatterie.NON_TESTE
        elif remplacer:
            diagnostic = DiagnosticBatterie.A_REMPLACER
        elif recharger:
            diagnostic = DiagnosticBatterie.A_RECHARGER
        elif faible:
            diagnostic = DiagnosticBatterie.FAIBLE
        else:
            diagnostic = DiagnosticBatterie.BONNE

        self.test_diagnostic = diagnostic
        self.test_circuit_charge = circuit
        self.test_etat_charge = soc
        self.test_detail = "\n".join(str(n) for n in notes)
        return diagnostic

    class Meta:
        verbose_name = _("Batterie")
        verbose_name_plural = _("Batteries")

    def __str__(self):
        return f"Batterie moteur - {self.voiture_exemplaire}"



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
        for prefix, _label in PIECES_BATTERIE:
            self.calcul_piece(prefix)

        # Diagnostic recalculé à chaque enregistrement
        self.calculer_diagnostic()

        # Batterie neuve / cosses saisies : état « Remplacé » et quantité 1 (facturation)
        self.normaliser_remplacement()

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
                        ancien_objet.kilometrage_batterie
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
        if self.kilometrage_batterie is not None:

            self.kilometrage_variation = (
                    self.kilometrage_batterie
                    - ancien_kilometrage
            )

            # =========================================
            # IMPORTANT
            # Le km chassis devient le km admission
            # =========================================
            self.kilometres_chassis = (
                self.kilometrage_batterie
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
                    _("Batterie")
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
                Maintenance.TypeMaintenance.BATTERIE
            )

            self.maintenance.voiture_exemplaire = (
                self.voiture_exemplaire
            )

            if self.kilometrage_batterie is not None:
                self.maintenance.kilometres_chassis = (
                    self.kilometrage_batterie
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
                and self.kilometrage_batterie is not None
        ):

            nouveau_kilometrage = int(
                self.kilometrage_batterie
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

        pieces = PIECES_BATTERIE

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

        if self.kilometrage_batterie is None:
            return

        km = Decimal(str(self.kilometrage_batterie))

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