from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import FabricantRoulement, TVAConfig, RouesSerrageEtat
from utils.mixin import TechnicienMixin
from maintenance.models import Maintenance


class RoulementEtat(models.TextChoices):
    OK = "OK", _("OK")
    NOT_OK = "NOT_OK", _("À remplacer")
    REMPLACE = "REMPLACE", _("Remplacé")
    REPARE = "REPARE", _("Réparé")
    NON_PRESENT = "NON_PRESENT", _("Non présent")


class RoulementMontage(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    PRESSER = "PRESSER", _("Roulement à presser")
    VISSER = "VISSER", _("Roulement à visser")


class RoulementCote(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")

    AVG = "AVG", _("AVG")
    AVD = "AVD", _("AVD")
    ARG = "ARG", _("ARG")
    ARD = "ARD", _("ARD")


class Roulement(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="roulement",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="roulement",
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

    kilometrage_roulement = models.PositiveIntegerField(
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
    # PIÈCES DU ROULEMENT DE ROUE
    # (chaque pièce : état / fabricant / côté / quantité / prix)
    # Les types de roulement sont « Non présent » par défaut :
    # on ne renseigne que le type monté sur le véhicule.
    # ======================================================

    # --- Roulement simple ---
    roulement_simple = models.CharField(
        max_length=25,
        choices=RoulementEtat.choices,
        default=RoulementEtat.NON_PRESENT,
        verbose_name=_("Roulement simple"),
    )
    roulement_simple_fabricant = models.CharField(
        max_length=30,
        choices=FabricantRoulement.choices,
        default=FabricantRoulement.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulement_simple_cote = models.CharField(
        max_length=25,
        choices=RoulementCote.choices,
        default=RoulementCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    roulement_simple_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    roulement_simple_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Roulement avec bague ABS ---
    roulement_bague_abs = models.CharField(
        max_length=25,
        choices=RoulementEtat.choices,
        default=RoulementEtat.NON_PRESENT,
        verbose_name=_("Roulement avec bague ABS"),
    )
    roulement_bague_abs_fabricant = models.CharField(
        max_length=30,
        choices=FabricantRoulement.choices,
        default=FabricantRoulement.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulement_bague_abs_cote = models.CharField(
        max_length=25,
        choices=RoulementCote.choices,
        default=RoulementCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    roulement_bague_abs_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    roulement_bague_abs_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Roulement avec moyeu ---
    roulement_moyeu = models.CharField(
        max_length=25,
        choices=RoulementEtat.choices,
        default=RoulementEtat.NON_PRESENT,
        verbose_name=_("Roulement avec moyeu"),
    )
    roulement_moyeu_fabricant = models.CharField(
        max_length=30,
        choices=FabricantRoulement.choices,
        default=FabricantRoulement.CHOISIR,
        verbose_name=_("Fabricant"),
    )
    roulement_moyeu_cote = models.CharField(
        max_length=25,
        choices=RoulementCote.choices,
        default=RoulementCote.CHOISIR,
        verbose_name=_("Côté"),
    )
    roulement_moyeu_quantite = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantité"),
    )
    roulement_moyeu_prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_("Prix d'achat HTVA"),
    )

    # --- Montage du roulement (choix unique) ---
    montage_roulement = models.CharField(
        max_length=10,
        choices=RoulementMontage.choices,
        default=RoulementMontage.CHOISIR,
        verbose_name=_("Montage du roulement"),
    )

    # --- Opérations / pièces associées (cases à cocher) ---
    depose_repose_roue = models.BooleanField(default=False, verbose_name=_("Dépose / repose roue"))
    ecrou_cardan = models.BooleanField(default=False, verbose_name=_("Écrou de cardan"))
    rotule_triangle = models.BooleanField(default=False, verbose_name=_("Rotule(s) de suspension de triangle"))
    porte_moyeu = models.BooleanField(default=False, verbose_name=_("Porte-moyeu"))
    capteur_abs = models.BooleanField(default=False, verbose_name=_("Capteur ABS"))

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
        related_name="roulement",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="roulement"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="roulement"
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
    PIECES_DEF = [
        (_("Roulement simple"), "roulement_simple"),
        (_("Roulement avec bague ABS"), "roulement_bague_abs"),
        (_("Roulement avec moyeu"), "roulement_moyeu"),
    ]

    OPERATIONS_DEF = [
        "depose_repose_roue",
        "ecrou_cardan",
        "rotule_triangle",
        "porte_moyeu",
        "capteur_abs",
    ]

    @property
    def operations_effectuees(self):
        """Libellés des cases cochées (dépose/repose roue, écrou, rotules…)."""
        return [
            self._meta.get_field(nom).verbose_name
            for nom in self.OPERATIONS_DEF
            if getattr(self, nom, False)
        ]

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_roulement is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_roulement < minimum:
                raise ValidationError({
                    "kilometrage_roulement": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_roulement,
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
            task_name = f"{_('Contrôle des roulements de roue')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.ROULEMENT
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
        if self.kilometrage_roulement is not None:
            self.kilometrage_variation = max(
                self.kilometrage_roulement - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE CONTRÔLE ROULEMENT
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_roulement is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_roulement > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_roulement
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Contrôle roulements de roue - {self.voiture_exemplaire.id}"
        return "Contrôle roulements de roue - non défini"

    class Meta:
        verbose_name = _("Contrôle des roulements de roue")
        verbose_name_plural = _("Contrôles des roulements de roue")

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

    def pieces_controle(self):
        """Toutes les pièces contrôlées (hors 'Non présent'), pour le détail / PDF."""
        pieces = []
        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)
            if not etat or etat == RoulementEtat.NON_PRESENT:
                continue
            pieces.append({
                "base": base,
                "label": label,
                "etat": etat,
                "etat_label": getattr(self, f"get_{base}_display")(),
                "cote": self._cote_display(base),
                "fabricant": self._fabricant_display(base),
            })
        return pieces

    def generer_rapport_remplacement(self):
        lignes = []
        total_pieces = Decimal("0.00")

        etats_labels = {
            RoulementEtat.NOT_OK: _("À remplacer"),
            RoulementEtat.REMPLACE: _("Remplacé"),
        }

        for label, base in self.PIECES_DEF:
            etat = getattr(self, base, None)

            if etat not in etats_labels:
                continue

            prix = Decimal(str(getattr(self, f"{base}_prix", None) or "0.00"))
            quantite = Decimal(str(getattr(self, f"{base}_quantite", None) or "0"))

            if prix <= 0 or quantite <= 0:
                continue

            total_ligne = (prix * quantite).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            total_pieces += total_ligne

            lignes.append({
                "champ": label,
                "etat": etat,
                "etat_label": etats_labels[etat],
                "fabricant": self._fabricant_display(base),
                "cote": self._cote_display(base),
                "quantite": quantite,
                "prix": prix,
                "total": total_ligne,
            })

        total_pieces = total_pieces.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "lignes": lignes,
            "pieces": lignes,
            "total_pieces": total_pieces,
            "total_general": total_pieces,
        }

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        total_pieces = rapport.get("total_pieces", Decimal("0.00"))
        cout_main_oeuvre = self.cout_main_oeuvre or Decimal("0.00")

        return (total_pieces + cout_main_oeuvre).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
