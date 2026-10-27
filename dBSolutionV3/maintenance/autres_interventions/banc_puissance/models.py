import uuid
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maintenance.autres_interventions.moteur.admission.models import TAUX_HORAIRE_CHOICES
from maintenance.choices import TVAConfig
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin


def chemin_courbe_banc(instance, filename):
    """
    Nom de fichier imprévisible, rangé par société : le PDF n'est jamais servi directement,
    il passe par la vue protégée « banc_puissance:banc_document ».
    """
    from django.db import connection
    schema = getattr(connection, "schema_name", "") or "public"
    return f"prive/banc_puissance/{schema}/{uuid.uuid4().hex}.pdf"


class TypeBanc(models.TextChoices):
    ROULEAUX = "ROULEAUX", _("Banc à rouleaux (inertiel)")
    ROULEAUX_FREIN = "ROULEAUX_FREIN", _("Banc à rouleaux à frein (charge)")
    MOYEUX = "MOYEUX", _("Banc à moyeux")
    MOTEUR = "MOTEUR", _("Banc moteur")


class MarqueBanc(models.TextChoices):
    CHOISIR = "CHOISIR", _("Choisir")
    DYNOJET = "DYNOJET", "Dynojet"
    MAHA = "MAHA", "MAHA"
    CARTEC = "CARTEC", "Cartec"
    DYNO_DYNAMICS = "DYNO_DYNAMICS", "Dyno Dynamics"
    MUSTANG = "MUSTANG", "Mustang Dynamometer"
    DIMSPORT = "DIMSPORT", "Dimsport"
    ROTOTEST = "ROTOTEST", "Rototest"
    DYNOCOM = "DYNOCOM", "Dynocom"
    MAINLINE = "MAINLINE", "Mainline"
    SUPERFLOW = "SUPERFLOW", "SuperFlow"
    POWER_DYNAMICS = "POWER_DYNAMICS", "Power Dynamics"
    AUTRE = "AUTRE", _("Autre")


class NormeCorrection(models.TextChoices):
    DIN_70020 = "DIN_70020", "DIN 70020"
    EWG_80_1269 = "EWG_80_1269", "CEE 80/1269 (EWG)"
    ISO_1585 = "ISO_1585", "ISO 1585"
    SAE_J1349 = "SAE_J1349", "SAE J1349"
    JIS_D1001 = "JIS_D1001", "JIS D1001"
    AUCUNE = "AUCUNE", _("Aucune (non corrigée)")


class CarburantBanc(models.TextChoices):
    SP95 = "SP95", _("Sans plomb 95")
    SP95_E10 = "SP95_E10", _("Sans plomb 95 E10")
    SP98 = "SP98", _("Sans plomb 98")
    SP102 = "SP102", _("Super 100 / 102")
    E85 = "E85", "E85"
    COURSE = "COURSE", _("Carburant course")
    DIESEL = "DIESEL", _("Diesel")
    AUTRE = "AUTRE", _("Autre")


class NiveauCartographie(models.TextChoices):
    STAGE_1 = "STAGE_1", _("Stage 1")
    STAGE_2 = "STAGE_2", _("Stage 2")
    STAGE_3 = "STAGE_3", _("Stage 3")
    SUR_MESURE = "SUR_MESURE", _("Sur mesure")
    ECO = "ECO", _("Éco / optimisation consommation")
    RETOUR_ORIGINE = "RETOUR_ORIGINE", _("Retour à l'origine")


class BancPuissance(TechnicienMixin, models.Model):
    pays = models.CharField(
        max_length=5,
        choices=TVAConfig.PAYS_CHOICES,
        default=TVAConfig.DEFAULT_PAYS,
        verbose_name=_("Pays"),
    )

    maintenance = models.ForeignKey(
        Maintenance,
        on_delete=models.CASCADE,
        related_name="banc_puissance",
        verbose_name=_("Maintenance"),
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="banc_puissance",
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

    kilometrage_banc = models.PositiveIntegerField(
        verbose_name=_("Kilométrage au passage au banc"),
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
    # BANC DE PUISSANCE
    # ======================================================
    date_passage = models.DateField(default=timezone.localdate, verbose_name=_("Date du passage au banc"))
    lieu_banc = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Lieu / préparateur du banc"))
    type_banc = models.CharField(max_length=20, choices=TypeBanc.choices, default=TypeBanc.ROULEAUX, verbose_name=_("Type de banc"))
    marque_banc = models.CharField(max_length=20, choices=MarqueBanc.choices, default=MarqueBanc.CHOISIR, verbose_name=_("Marque du banc"))
    norme_correction = models.CharField(max_length=20, choices=NormeCorrection.choices, default=NormeCorrection.DIN_70020, verbose_name=_("Norme de correction"))
    rapport_mesure = models.CharField(max_length=20, blank=True, default="", verbose_name=_("Rapport de boîte utilisé"))
    carburant = models.CharField(max_length=20, choices=CarburantBanc.choices, default=CarburantBanc.SP98, verbose_name=_("Carburant"))
    temperature_c = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name=_("Température ambiante (°C)"))
    pression_hpa = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name=_("Pression atmosphérique (hPa)"))
    humidite_pct = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(100)], verbose_name=_("Humidité (%)"))

    # ======================================================
    # CARTOGRAPHIE
    # ======================================================
    cartographie_effectuee = models.BooleanField(default=False, verbose_name=_("Cartographie réalisée"))
    niveau_cartographie = models.CharField(max_length=20, choices=NiveauCartographie.choices, default=NiveauCartographie.STAGE_1, verbose_name=_("Niveau de cartographie"))
    preparateur = models.CharField(max_length=120, blank=True, default="", verbose_name=_("Préparateur / programmeur"))
    calculateur = models.CharField(max_length=80, blank=True, default="", verbose_name=_("Calculateur (ECU / TCU)"))
    outil_cartographie = models.CharField(max_length=80, blank=True, default="", verbose_name=_("Outil / logiciel"))

    # ---------------- VALEURS SANS CARTOGRAPHIE (AVANT) ----------------
    avant_puissance_ch = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Puissance maximale (ch)"),
    )
    avant_regime_puissance = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Régime de puissance maxi (tr/min)"),
    )
    avant_couple_nm = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Couple maximal (Nm)"),
    )
    avant_regime_couple = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Régime de couple maxi (tr/min)"),
    )
    avant_puissance_roues_ch = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Puissance aux roues (ch)"),
    )
    avant_pdf = models.FileField(
        upload_to=chemin_courbe_banc, null=True, blank=True,
        verbose_name=_("Courbes (PDF, 10 Mo max.)"),
    )

    # ---------------- VALEURS APRÈS CARTOGRAPHIE ----------------
    apres_puissance_ch = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Puissance maximale (ch)"),
    )
    apres_regime_puissance = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Régime de puissance maxi (tr/min)"),
    )
    apres_couple_nm = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Couple maximal (Nm)"),
    )
    apres_regime_couple = models.PositiveIntegerField(
        null=True, blank=True, verbose_name=_("Régime de couple maxi (tr/min)"),
    )
    apres_puissance_roues_ch = models.DecimalField(
        max_digits=6, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(0)], verbose_name=_("Puissance aux roues (ch)"),
    )
    apres_pdf = models.FileField(
        upload_to=chemin_courbe_banc, null=True, blank=True,
        verbose_name=_("Courbes (PDF, 10 Mo max.)"),
    )

    # ======================================================
    # COÛTS
    # ======================================================
    prix_banc = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name=_("Prix du passage au banc HTVA"))
    prix_cartographie = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name=_("Prix de la cartographie HTVA"))

    remarques = models.TextField(blank=True, default="", verbose_name=_("Remarques"))

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


    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="banc_puissance",
        verbose_name=_("Main d'oeuvre")
    )

    # --- Technicien ---
    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Technicien"),
        related_name="banc_puissance"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Société"),
        related_name="banc_puissance"
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

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire_id and self.kilometrage_banc is not None:
            # Création : on compare au véhicule.
            # Modification : au kilométrage figé avant ce contrôle.
            if self.pk:
                minimum = self.kilometres_chassis or 0
            else:
                minimum = self.voiture_exemplaire.kilometres_chassis or 0

            if self.kilometrage_banc < minimum:
                raise ValidationError({
                    "kilometrage_banc": _(
                        "Le kilométrage du contrôle (%(km_controle)s) ne peut pas "
                        "être inférieur au kilométrage avant intervention (%(km_voiture)s)."
                    ) % {
                        "km_controle": self.kilometrage_banc,
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
            task_name = f"{_('Passage au banc de puissance')} {self.voiture_exemplaire}"

            self.main_oeuvre.descriptif = task_name
            self.main_oeuvre.save(update_fields=["descriptif"])

        # =========================
        # MAINTENANCE
        # =========================
        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.BANC_PUISSANCE
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
        if self.kilometrage_banc is not None:
            self.kilometrage_variation = max(
                self.kilometrage_banc - (self.kilometres_chassis or 0), 0
            )
        else:
            self.kilometrage_variation = 0

        # =========================
        # SAUVEGARDE PASSAGE AU BANC
        # =========================
        super().save(*args, **kwargs)

        # =========================
        # MISE À JOUR DU VÉHICULE
        # =========================
        if self.voiture_exemplaire_id and self.kilometrage_banc is not None:
            voiture = type(self.voiture_exemplaire).objects.get(
                pk=self.voiture_exemplaire_id
            )
            if self.kilometrage_banc > (voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = self.kilometrage_banc
                voiture.save(update_fields=["kilometres_chassis"])

    def __str__(self):
        if self.voiture_exemplaire:
            return f"Passage au banc de puissance - {self.voiture_exemplaire.id}"
        return "Passage au banc - non défini"

    class Meta:
        verbose_name = _("Passage au banc de puissance")
        verbose_name_plural = _("Passages au banc de puissance")

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
    # RÉSULTATS
    # ======================================================
    KW_PAR_CH = Decimal("0.73549875")

    @staticmethod
    def _ecart(avant, apres):
        if avant is None or apres is None:
            return None
        return (Decimal(apres) - Decimal(avant)).quantize(Decimal("0.1"))

    @staticmethod
    def _pourcentage(avant, apres):
        if not avant or apres is None:
            return None
        return ((Decimal(apres) - Decimal(avant)) / Decimal(avant) * 100).quantize(Decimal("0.1"))

    def _kw(self, ch):
        return None if ch is None else (Decimal(ch) * self.KW_PAR_CH).quantize(Decimal("0.1"))

    @property
    def avant_puissance_kw(self):
        return self._kw(self.avant_puissance_ch)

    @property
    def apres_puissance_kw(self):
        return self._kw(self.apres_puissance_ch)

    @property
    def gain_ch(self):
        return self._ecart(self.avant_puissance_ch, self.apres_puissance_ch)

    @property
    def gain_ch_pct(self):
        return self._pourcentage(self.avant_puissance_ch, self.apres_puissance_ch)

    @property
    def gain_nm(self):
        return self._ecart(self.avant_couple_nm, self.apres_couple_nm)

    @property
    def gain_nm_pct(self):
        return self._pourcentage(self.avant_couple_nm, self.apres_couple_nm)

    @property
    def pertes_transmission_pct(self):
        """Pertes de transmission estimées (puissance moteur vs roues), mesure la plus récente."""
        for moteur, roues in ((self.apres_puissance_ch, self.apres_puissance_roues_ch),
                              (self.avant_puissance_ch, self.avant_puissance_roues_ch)):
            if moteur and roues:
                return ((Decimal(moteur) - Decimal(roues)) / Decimal(moteur) * 100).quantize(Decimal("0.1"))
        return None

    # ======================================================
    # RAPPORT (coûts)
    # ======================================================
    def generer_rapport_remplacement(self):
        lignes = []
        for libelle, prix, prestataire in (
            (_("Passage au banc de puissance"), self.prix_banc, self.lieu_banc),
            (_("Cartographie"), self.prix_cartographie if self.cartographie_effectuee else Decimal("0"), self.preparateur),
        ):
            prix = Decimal(str(prix or "0")).quantize(Decimal("0.01"))
            if prix > 0:
                lignes.append({
                    "champ": libelle,
                    "etat": "FAIT",
                    "etat_label": _("Réalisé"),
                    "fabricant": prestataire,
                    "quantite": Decimal("1"),
                    "prix": prix,
                    "total": prix,
                })
        total = sum((l["total"] for l in lignes), Decimal("0.00")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {"lignes": lignes, "pieces": lignes, "total_pieces": total, "total_general": total}

    @property
    def total_general_avec_main_oeuvre(self):
        rapport = self.generer_rapport_remplacement()
        return (rapport["total_pieces"] + (self.cout_main_oeuvre or Decimal("0.00"))).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    def supprimer_fichiers(self):
        for champ in ("avant_pdf", "apres_pdf"):
            fichier = getattr(self, champ)
            if fichier:
                fichier.delete(save=False)
