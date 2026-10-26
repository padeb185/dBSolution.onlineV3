from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantPneus, TVAConfig, RouesSerrageEtat
from maintenance.pneus.models import ValveType
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class RoueCrevaison(models.TextChoices):
    AVG = "AVG", _("Avant gauche (AVG)")
    AVD = "AVD", _("Avant droit (AVD)")
    ARG = "ARG", _("Arrière gauche (ARG)")
    ARD = "ARD", _("Arrière droit (ARD)")
    SECOURS = "SECOURS", _("Roue de secours")


class CauseCrevaison(models.TextChoices):
    CLOU = "CLOU", _("Clou / vis")
    OBJET = "OBJET", _("Objet tranchant (verre, métal…)")
    COUPURE = "COUPURE", _("Coupure / entaille")
    PINCEMENT = "PINCEMENT", _("Pincement (choc trottoir / nid-de-poule)")
    VALVE = "VALVE", _("Valve défectueuse")
    JANTE = "JANTE", _("Fuite au talon / jante")
    INCONNUE = "INCONNUE", _("Inconnue")


class LocalisationCrevaison(models.TextChoices):
    BANDE = "BANDE", _("Bande de roulement (zone réparable)")
    EPAULE = "EPAULE", _("Épaule (non réparable)")
    FLANC = "FLANC", _("Flanc (non réparable)")
    VALVE = "VALVE", _("Valve")
    TALON = "TALON", _("Talon / jante")


class SolutionCrevaison(models.TextChoices):
    REPARATION = "REPARATION", _("Réparation")
    REMPLACEMENT_1 = "REMPLACEMENT_1", _("Remplacement d'un pneu")
    REMPLACEMENT_2 = "REMPLACEMENT_2", _("Remplacement de 2 pneus (même essieu)")


class TypeReparation(models.TextChoices):
    MECHE = "MECHE", _("Mèche")
    CHAMPIGNON = "CHAMPIGNON", _("Champignon")
    RUSTINE = "RUSTINE", _("Rustine (patch intérieur)")


ROUE_OPPOSEE = {"AVG": "AVD", "AVD": "AVG", "ARG": "ARD", "ARD": "ARG"}
LOCALISATIONS_NON_REPARABLES = {"EPAULE", "FLANC"}


class Crevaison(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="crevaison",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="crevaison",
        verbose_name=_("Véhicule"),
        null=True,
        blank=True
    )

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_crevaison = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au moment du contrôle"),
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

    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    # ======================================================
    # CREVAISON
    # ======================================================
    roue = models.CharField(max_length=10, choices=RoueCrevaison.choices, default=RoueCrevaison.AVG,
                            verbose_name=_("Roue crevée"))
    cause = models.CharField(max_length=12, choices=CauseCrevaison.choices, default=CauseCrevaison.CLOU,
                             verbose_name=_("Cause"))
    localisation = models.CharField(max_length=10, choices=LocalisationCrevaison.choices,
                                    default=LocalisationCrevaison.BANDE, verbose_name=_("Localisation du dommage"))
    solution = models.CharField(max_length=16, choices=SolutionCrevaison.choices, default=SolutionCrevaison.REPARATION,
                                verbose_name=_("Solution"))

    # --- Réparation
    type_reparation = models.CharField(max_length=12, choices=TypeReparation.choices, blank=True,
                                       verbose_name=_("Type de réparation"))
    reparation_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                          verbose_name=_("Prix de la réparation (consommable) HTVA"))

    # --- Remplacement (1 ou 2 pneus)
    pneu_fabricant = models.CharField(max_length=30, choices=FabricantPneus.choices, default=FabricantPneus.CHOISIR,
                                      verbose_name=_("Manufacturier"))
    pneu_nouveau = models.ForeignKey("voiture_pneus.VoiturePneus", on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="+", verbose_name=_("Pneu monté"),
                                     help_text=_("Laisser vide pour reprendre la même référence."))
    pneu_dimension = models.CharField(max_length=40, blank=True, verbose_name=_("Dimension"),
                                      help_text=_("Ex. : 225/45 R17 94Y"))
    pneu_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                    verbose_name=_("Prix d'achat HTVA par pneu"))

    # --- Valve / équilibrage / pression
    valve_remplacee = models.BooleanField(default=False, verbose_name=_("Valve remplacée"))
    valve_type = models.CharField(max_length=25, choices=ValveType.choices, default=ValveType.CAOUTCHOUC,
                                  verbose_name=_("Type de valve"))
    valve_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                     verbose_name=_("Prix d'achat HTVA par valve"))
    equilibrage = models.BooleanField(default=False, verbose_name=_("Équilibrage"))
    masses_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                      verbose_name=_("Masses d'équilibrage HTVA"))
    pression_bar = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True,
                                       verbose_name=_("Pression après intervention (bar)"))

    remarques = models.TextField(blank=True, verbose_name=_("Remarques"))

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        default="VERT",
        verbose_name=_("État visuel / Tag"),
    )

    serrage_roues = models.CharField(max_length=25, choices=RouesSerrageEtat.choices, default=RouesSerrageEtat.A_FAIRE,
                                     verbose_name=_("Serrage des roues"))

    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crevaison",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="crevaison"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="crevaison"
    )
    taux_horaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"),
        verbose_name=_("Taux horaire"),
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    # ======================================================
    # LISTE DES PIÈCES (source unique pour le rapport)
    # ======================================================
    PIECES_DEF = []

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        erreurs = {}
        if self.solution == SolutionCrevaison.REPARATION:
            if self.localisation in LOCALISATIONS_NON_REPARABLES:
                erreurs["solution"] = _("Un dommage sur l'épaule ou le flanc n'est pas réparable : remplacez le pneu.")
            if not self.type_reparation:
                erreurs["type_reparation"] = _("Choisissez la réparation : mèche, champignon ou rustine.")
        elif self.solution == SolutionCrevaison.REMPLACEMENT_2 and self.roue == RoueCrevaison.SECOURS:
            erreurs["solution"] = _("La roue de secours n'a pas de roue opposée sur l'essieu.")
        if erreurs:
            raise ValidationError(erreurs)
        if self.voiture_exemplaire_id and self.kilometrage_crevaison is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_crevaison < minimum:
                raise ValidationError({
                    "kilometrage_crevaison": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_crevaison,
                        "km_voiture": minimum,
                    }
                })

    def save(self, *args, **kwargs):

        # =========================
        # TECHNICIEN
        # =========================
        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            task_name = f"{_('Crevaison')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.CREVAISON
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            self.maintenance.save(
                update_fields=["type_maintenance", "voiture_exemplaire"]
            )

        # =========================
        # KILOMÉTRAGE AVANT INTERVENTION
        # (figé uniquement à la création)
        # =========================
        if self.voiture_exemplaire_id and self._state.adding and not self.kilometres_chassis:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            self.kilometres_chassis = voiture.kilometres_chassis or 0

        # =========================
        # CALCUL VARIATION (jamais négative : champ PositiveInteger)
        # =========================
        if self.kilometrage_crevaison is not None:
            self.kilometrage_variation = max(
                self.kilometrage_crevaison - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CREVAISON
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_crevaison is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_crevaison > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_crevaison
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Crevaison - {self.voiture_exemplaire.id}"
        return "Crevaison - non défini"

    class Meta:
        verbose_name = _("Crevaison")
        verbose_name_plural = _("Crevaisons")

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
        if self.main_oeuvre and self.main_oeuvre.taux_horaire is not None:
            return self.main_oeuvre.taux_horaire

        return Decimal("0.00")

    @property
    def cout_main_oeuvre(self):
        if not self.main_oeuvre:
            return Decimal("0.00")

        temps_minutes = self.main_oeuvre.temps_minutes or 0
        taux_horaire = self.main_oeuvre.taux_horaire or Decimal("0.00")

        cout = (
                Decimal(str(temps_minutes))
                / Decimal("60")
                * Decimal(str(taux_horaire))
        )

        return cout.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # ======================================================
    # RAPPORT
    # ======================================================

    def _choice_display(self, base, suffixe):
        """Libellé d'un champ <base>_<suffixe>, ou '' s'il n'existe pas ou vaut sa valeur par défaut."""
        attr = f"{base}_{suffixe}"
        valeur = getattr(self, attr, None)
        if not valeur:
            return ""
        try:
            defaut = self._meta.get_field(attr).default
        except Exception:
            defaut = None
        if valeur == defaut:
            return ""
        return getattr(self, f"get_{attr}_display")()

    def _fabricant_display(self, base):
        return self._choice_display(base, "fabricant")

    def _cote_display(self, base):
        return self._choice_display(base, "cote")

    # ======================================================
    # CREVAISON : roues concernées et rapport
    # ======================================================
    @property
    def est_reparation(self):
        return self.solution == SolutionCrevaison.REPARATION

    @property
    def nombre_pneus_remplaces(self):
        return {SolutionCrevaison.REMPLACEMENT_1: 1, SolutionCrevaison.REMPLACEMENT_2: 2}.get(self.solution, 0)

    @property
    def roues_concernees(self):
        """Roue crevée (+ roue opposée du même essieu pour un remplacement de 2 pneus)."""
        roues = [self.roue]
        if self.solution == SolutionCrevaison.REMPLACEMENT_2 and self.roue in ROUE_OPPOSEE:
            roues.append(ROUE_OPPOSEE[self.roue])
        return roues

    @property
    def roues_concernees_display(self):
        return " + ".join(roue for roue in self.roues_concernees)

    def pieces_controle(self):
        return []

    def _ligne(self, libelle, quantite, prix, fabricant=""):
        prix = Decimal(str(prix or 0))
        quantite = Decimal(str(quantite or 0))
        total = (prix * quantite).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {
            "champ": libelle, "etat": "REMPLACE", "etat_label": _("Remplacé"),
            "fabricant": fabricant, "cote": self.roues_concernees_display,
            "quantite": quantite, "prix": prix, "total": total,
        }

    def generer_rapport_remplacement(self):
        """Lignes facturables : réparation ou pneu(s), valve(s), masses d'équilibrage."""
        lignes = []
        if self.est_reparation:
            if self.reparation_prix:
                libelle = _("Réparation de crevaison – %(type)s") % {"type": self.get_type_reparation_display() or "-"}
                ligne = self._ligne(libelle, 1, self.reparation_prix)
                ligne["etat"], ligne["etat_label"] = "REPARE", _("Réparé")
                lignes.append(ligne)
        elif self.nombre_pneus_remplaces and self.pneu_prix:
            fabricant = self.get_pneu_fabricant_display() if self.pneu_fabricant != FabricantPneus.CHOISIR else ""
            libelle = _("Pneu") + (f" {self.pneu_dimension}" if self.pneu_dimension else "")
            lignes.append(self._ligne(libelle, self.nombre_pneus_remplaces, self.pneu_prix, fabricant))
        if self.valve_remplacee and self.valve_prix:
            nb = self.nombre_pneus_remplaces or 1
            lignes.append(self._ligne(self.get_valve_type_display(), nb, self.valve_prix))
        if self.equilibrage and self.masses_prix:
            lignes.append(self._ligne(_("Masses d'équilibrage"), 1, self.masses_prix))

        total = sum((l["total"] for l in lignes), Decimal("0.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {"lignes": lignes, "pieces": lignes, "total_pieces": total, "total_general": total}

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        total_pieces = rapport.get("total_pieces", Decimal("0.00"))
        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return (total_pieces + cout_main_oeuvre).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
