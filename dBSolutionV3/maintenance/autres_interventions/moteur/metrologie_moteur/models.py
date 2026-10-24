"""
Métrologie moteur : relevé des cotes du moteur en centièmes de millimètre.

- Chemises : diamètre en haut / milieu / bas, sur deux axes (A = axe du vilebrequin,
  B = perpendiculaire) → ovalisation, conicité, usure.
- Pistons : diamètre de jupe → jeu piston / chemise.
- Segments : jeu à la coupe (feu, étanchéité, racleur).
- Vilebrequin : manetons et tourillons, deux sections × deux axes → ovalisation, conicité.
- Pied de bielle : alésage sur deux axes + diamètre de l'axe de piston → jeu.
- Alésage / course / cylindrée : calcul dans les deux sens.

Toutes les cotes sont saisies en millimètres avec deux décimales (centièmes).
Les tolérances constructeur saisies sur l'intervention permettent de signaler
automatiquement les cotes hors tolérance.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from maintenance.choices import TAUX_HORAIRE_CHOICES, TVAConfig
from maintenance.models import Maintenance
from utils.mixin import TechnicienMixin

PI = Decimal("3.14159265358979323846")
CENTIEME = Decimal("0.01")
DIXIEME_CM3 = Decimal("0.1")


def cote(verbose_name, help_text=""):
    """Cote en millimètres, au centième."""
    return models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        verbose_name=verbose_name, help_text=help_text,
    )


def _d(v):
    return None if v in (None, "") else Decimal(str(v))


def _valeurs(*vals):
    return [Decimal(str(v)) for v in vals if v is not None]


def _ecart(*vals):
    v = _valeurs(*vals)
    return (max(v) - min(v)) if len(v) >= 2 else None


def _verifier(valeur, mini=None, maxi=None):
    """OK / HORS / None (pas de valeur ou pas de tolérance)."""
    if valeur is None or (mini is None and maxi is None):
        return None
    if mini is not None and valeur < mini:
        return StatutCote.HORS
    if maxi is not None and valeur > maxi:
        return StatutCote.HORS
    return StatutCote.OK


def calcul_cylindree(alesage, course, cylindree, nombre_cylindres):
    """
    Cylindrée (cm³) = π/4 × alésage² × course × nombre de cylindres / 1000 (cotes en mm).
    - alésage + course connus  → cylindrée
    - cylindrée + alésage      → course
    - cylindrée + course       → alésage
    Retourne (alésage, course, cylindrée).
    """
    d, c, v = _d(alesage), _d(course), _d(cylindree)
    n = Decimal(nombre_cylindres or 0)
    if not n:
        return d, c, v
    k = PI / Decimal(4) * n / Decimal(1000)
    if d and c:
        v = (k * d * d * c).quantize(DIXIEME_CM3, rounding=ROUND_HALF_UP)
    elif v and d:
        c = (v / (k * d * d)).quantize(CENTIEME, rounding=ROUND_HALF_UP)
    elif v and c:
        d = (v / (k * c)).sqrt().quantize(CENTIEME, rounding=ROUND_HALF_UP)
    return d, c, v


class StatutCote(models.TextChoices):
    OK = "OK", _("Dans la tolérance")
    HORS = "HORS", _("Hors tolérance")


class MetrologieMoteur(TechnicienMixin, models.Model):

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
        Maintenance, on_delete=models.CASCADE, related_name="metrologie_moteur", null=True, blank=True
    )
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE,
        related_name="metrologie_moteur", null=True, blank=True
    )

    # -------------------------
    # KILOMÉTRAGES
    # -------------------------
    kilometres_chassis = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres chassis"))
    kilometres_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, editable=False, verbose_name=_("Kilomètres rollback"))
    kilometres_boite = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_boite_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback boite"))
    kilometres_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_moteur_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback moteur"))
    kilometres_embrayage = models.PositiveIntegerField(default=0, null=True, blank=True)
    kilometres_embrayage_rollback = models.PositiveIntegerField(default=0, null=True, blank=True, verbose_name=_("Kilomètres rollback embrayage"))

    kilometrage_metrologie = models.PositiveIntegerField(verbose_name=_("Kilométrage de l'intervention"))
    kilometrage_variation = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("Variation du kilométrage"))

    # -------------------------
    # MOTEUR : ALÉSAGE / COURSE / CYLINDRÉE
    # -------------------------
    nombre_cylindres = models.PositiveSmallIntegerField(
        default=4, validators=[MinValueValidator(1), MaxValueValidator(16)],
        verbose_name=_("Nombre de cylindres"),
    )
    alesage_nominal = cote(_("Alésage constructeur (mm)"))
    course_nominale = cote(_("Course constructeur (mm)"))
    cylindree_constructeur_cm3 = models.DecimalField(
        max_digits=8, decimal_places=1, null=True, blank=True, verbose_name=_("Cylindrée constructeur (cm³)")
    )
    alesage_mesure = cote(_("Alésage mesuré (mm)"), _("Vide : moyenne des chemises mesurées."))
    course_mesuree = cote(_("Course mesurée (mm)"))
    cylindree_cm3 = models.DecimalField(
        max_digits=8, decimal_places=1, null=True, blank=True, verbose_name=_("Cylindrée (cm³)"),
        help_text=_("Calculée à partir de l'alésage et de la course ; saisie, elle permet de calculer la cote manquante."),
    )

    # -------------------------
    # TOLÉRANCES CONSTRUCTEUR
    # -------------------------
    tol_chemise_diametre_min = cote(_("Chemise : diamètre mini"))
    tol_chemise_diametre_max = cote(_("Chemise : diamètre maxi (usure)"))
    tol_chemise_ovalisation_max = cote(_("Chemise : ovalisation maxi"))
    tol_chemise_conicite_max = cote(_("Chemise : conicité maxi"))
    tol_jeu_piston_min = cote(_("Jeu piston / chemise mini"))
    tol_jeu_piston_max = cote(_("Jeu piston / chemise maxi"))
    tol_segment_feu_min = cote(_("Segment de feu : jeu à la coupe mini"))
    tol_segment_feu_max = cote(_("Segment de feu : jeu à la coupe maxi"))
    tol_segment_etancheite_min = cote(_("Segment d'étanchéité : jeu à la coupe mini"))
    tol_segment_etancheite_max = cote(_("Segment d'étanchéité : jeu à la coupe maxi"))
    tol_segment_racleur_min = cote(_("Segment racleur : jeu à la coupe mini"))
    tol_segment_racleur_max = cote(_("Segment racleur : jeu à la coupe maxi"))
    tol_maneton_diametre_min = cote(_("Maneton : diamètre mini"))
    tol_maneton_diametre_max = cote(_("Maneton : diamètre maxi"))
    tol_maneton_ovalisation_max = cote(_("Maneton : ovalisation maxi"))
    tol_maneton_conicite_max = cote(_("Maneton : conicité maxi"))
    tol_tourillon_diametre_min = cote(_("Tourillon : diamètre mini"))
    tol_tourillon_diametre_max = cote(_("Tourillon : diamètre maxi"))
    tol_tourillon_ovalisation_max = cote(_("Tourillon : ovalisation maxi"))
    tol_tourillon_conicite_max = cote(_("Tourillon : conicité maxi"))
    tol_pied_bielle_ovalisation_max = cote(_("Pied de bielle : ovalisation maxi"))
    tol_jeu_pied_bielle_min = cote(_("Jeu axe / pied de bielle mini"))
    tol_jeu_pied_bielle_max = cote(_("Jeu axe / pied de bielle maxi"))

    # -------------------------
    # DIVERS
    # -------------------------
    remarques = models.TextField(verbose_name=_("Remarques"), blank=True, null=True)

    TAG_CHOICES = [
        ("VERT", _("Vert")),
        ("JAUNE", _("Jaune")),
        ("ROUGE", _("Rouge")),
    ]
    tag = models.CharField(max_length=10, choices=TAG_CHOICES, default="JAUNE", verbose_name=_("État visuel / Tag"))

    tech_technicien = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_("Technicien"), related_name="metrologie_moteur"
    )
    tech_nom_technicien = models.CharField(_("Nom du technicien"), max_length=255, blank=True)
    tech_role_technicien = models.CharField(_("Rôle du technicien"), max_length=255, blank=True)
    tech_societe = models.ForeignKey(
        "societe.Societe", on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name=_("Société"), related_name="metrologie_moteur"
    )

    taux_horaire = models.DecimalField(
        max_digits=10, decimal_places=2, choices=TAUX_HORAIRE_CHOICES,
        default=Decimal("50.00"), verbose_name=_("Taux horaire"),
    )
    main_oeuvre = models.ForeignKey(
        "maindoeuvre.MainDoeuvre", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="metrologie_moteur", verbose_name=_("Main d'oeuvre")
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Métrologie moteur")
        verbose_name_plural = _("Métrologies moteur")

    def __str__(self):
        return f"Métrologie moteur - {self.voiture_exemplaire}"

    def assign_technicien(self, user):
        self.tech_technicien = user
        self.tech_nom_technicien = f"{user.prenom} {user.nom}"
        self.tech_role_technicien = user.role
        self.tech_societe = user.societe

    def clean(self):
        super().clean()
        if self.voiture_exemplaire and self.kilometrage_metrologie is not None:
            if self.kilometrage_metrologie < (self.voiture_exemplaire.kilometres_chassis or 0):
                raise ValidationError({
                    "kilometrage_metrologie": _("Le kilométrage ne peut pas être inférieur au kilométrage du véhicule.")
                })

    # -------------------------
    # CALCULS
    # -------------------------
    @property
    def alesage_moyen_chemises(self):
        if not self.pk:
            return None
        valeurs = [v for c in self.cylindres.all() for v in c.chemise_valeurs]
        if not valeurs:
            return None
        return (sum(valeurs) / len(valeurs)).quantize(CENTIEME, rounding=ROUND_HALF_UP)

    def calculer_cylindree(self):
        d, c, v = calcul_cylindree(self.alesage_mesure, self.course_mesuree, self.cylindree_cm3, self.nombre_cylindres)
        self.alesage_mesure, self.course_mesuree, self.cylindree_cm3 = d, c, v

    def finaliser(self):
        """Après l'enregistrement des lignes : alésage moyen des chemises si vide, puis cylindrée."""
        if self.alesage_mesure is None:
            self.alesage_mesure = self.alesage_moyen_chemises
        self.calculer_cylindree()
        type(self).objects.filter(pk=self.pk).update(
            alesage_mesure=self.alesage_mesure,
            course_mesuree=self.course_mesuree,
            cylindree_cm3=self.cylindree_cm3,
        )

    @property
    def cylindree_unitaire_cm3(self):
        if self.cylindree_cm3 and self.nombre_cylindres:
            return (self.cylindree_cm3 / self.nombre_cylindres).quantize(DIXIEME_CM3, rounding=ROUND_HALF_UP)
        return None

    @property
    def rapport_course_alesage(self):
        if self.alesage_mesure and self.course_mesuree:
            return (self.course_mesuree / self.alesage_mesure).quantize(CENTIEME, rounding=ROUND_HALF_UP)
        return None

    @property
    def type_moteur_geometrie(self):
        r = self.rapport_course_alesage
        if r is None:
            return ""
        if r < Decimal("0.98"):
            return _("Super-carré")
        if r > Decimal("1.02"):
            return _("Longue course")
        return _("Carré")

    @property
    def ecart_cylindree_pct(self):
        if self.cylindree_cm3 and self.cylindree_constructeur_cm3:
            return ((self.cylindree_cm3 - self.cylindree_constructeur_cm3) / self.cylindree_constructeur_cm3
                    * 100).quantize(CENTIEME, rounding=ROUND_HALF_UP)
        return None

    def tolerances_dict(self):
        return {f.name[4:]: getattr(self, f.name) for f in self._meta.fields if f.name.startswith("tol_")}

    def synthese(self):
        """Toutes les cotes contrôlées hors tolérance : [{element, libelle, valeur, mini, maxi}]."""
        hors = []
        for c in self.cylindres.all():
            for ctl in c.controles():
                if ctl["statut"] == StatutCote.HORS:
                    hors.append({"element": _("Cylindre %(n)s") % {"n": c.numero}, **ctl})
        for t in self.tourillons.all():
            for ctl in t.controles():
                if ctl["statut"] == StatutCote.HORS:
                    hors.append({"element": _("Tourillon %(n)s") % {"n": t.numero}, **ctl})
        return hors

    @property
    def nombre_hors_tolerance(self):
        return len(self.synthese())

    # -------------------------
    # RAPPORT (gabarit commun des interventions : aucune pièce facturée)
    # -------------------------
    def generer_rapport_remplacement(self):
        return {"lignes": [], "total_general": Decimal("0.00")}

    # -------------------------
    # SAVE
    # -------------------------
    def save(self, *args, **kwargs):
        self.calculer_cylindree()

        if not self.tech_technicien_id and hasattr(self, "_user"):
            self.assign_technicien(self._user)

        voiture = None
        if self.voiture_exemplaire_id:
            voiture = type(self.voiture_exemplaire).objects.get(pk=self.voiture_exemplaire_id)

        # kilometres_chassis = kilométrage du véhicule AVANT l'intervention (renseigné par la vue)
        if self.kilometrage_metrologie is not None:
            self.kilometrage_variation = max(self.kilometrage_metrologie - (self.kilometres_chassis or 0), 0)
        else:
            self.kilometrage_variation = 0

        if self.main_oeuvre_id and self.voiture_exemplaire_id:
            self.main_oeuvre.descriptif = _("Métrologie moteur") + " " + str(self.voiture_exemplaire)
            self.main_oeuvre.save(update_fields=["descriptif"])

        if self.maintenance_id and self.voiture_exemplaire_id:
            self.maintenance.type_maintenance = Maintenance.TypeMaintenance.METROLOGIE_MOTEUR
            self.maintenance.voiture_exemplaire = self.voiture_exemplaire
            if self.kilometrage_metrologie is not None:
                self.maintenance.kilometres_chassis = self.kilometrage_metrologie
            self.maintenance.save(update_fields=["type_maintenance", "voiture_exemplaire", "kilometres_chassis"])

        super().save(*args, **kwargs)

        # Ne jamais faire redescendre le kilométrage général du véhicule
        if voiture is not None and self.kilometrage_metrologie is not None:
            if int(self.kilometrage_metrologie) >= int(voiture.kilometres_chassis or 0):
                voiture.kilometres_chassis = int(self.kilometrage_metrologie)
                voiture.save(update_fields=["kilometres_chassis"])

    # -------------------------
    # MAIN-D'ŒUVRE
    # -------------------------
    @property
    def temps_main_oeuvre_display(self):
        if not self.main_oeuvre:
            return "0h00"
        heures, minutes = divmod(self.main_oeuvre.temps_minutes or 0, 60)
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
        cout = (Decimal(str(self.main_oeuvre.temps_minutes or 0)) / Decimal("60")
                * Decimal(str(self.main_oeuvre.taux_horaire or 0)))
        return cout.quantize(CENTIEME, rounding=ROUND_HALF_UP)

    @property
    def total_general_avec_main_oeuvre(self):
        return (self.generer_rapport_remplacement()["total_general"] + self.cout_main_oeuvre).quantize(
            CENTIEME, rounding=ROUND_HALF_UP)


# =====================================================================
# MESURES PAR CYLINDRE
# =====================================================================
class MesureCylindre(models.Model):
    metrologie = models.ForeignKey(MetrologieMoteur, on_delete=models.CASCADE, related_name="cylindres",
                                   verbose_name=_("Métrologie"))
    numero = models.PositiveSmallIntegerField(verbose_name=_("Cylindre n°"))

    # Chemise : 3 hauteurs × 2 axes (A = axe du vilebrequin, B = perpendiculaire)
    chemise_haut_a = cote(_("Chemise haut – axe A"))
    chemise_haut_b = cote(_("Chemise haut – axe B"))
    chemise_milieu_a = cote(_("Chemise milieu – axe A"))
    chemise_milieu_b = cote(_("Chemise milieu – axe B"))
    chemise_bas_a = cote(_("Chemise bas – axe A"))
    chemise_bas_b = cote(_("Chemise bas – axe B"))

    piston_diametre = cote(_("Piston : diamètre de jupe"))

    segment_feu_jeu = cote(_("Segment de feu : jeu à la coupe"))
    segment_etancheite_jeu = cote(_("Segment d'étanchéité : jeu à la coupe"))
    segment_racleur_jeu = cote(_("Segment racleur : jeu à la coupe"))

    # Maneton : 2 sections × 2 axes
    maneton_1_a = cote(_("Maneton section 1 – axe A"))
    maneton_1_b = cote(_("Maneton section 1 – axe B"))
    maneton_2_a = cote(_("Maneton section 2 – axe A"))
    maneton_2_b = cote(_("Maneton section 2 – axe B"))

    # Pied de bielle
    pied_bielle_a = cote(_("Pied de bielle – axe A"))
    pied_bielle_b = cote(_("Pied de bielle – axe B"))
    axe_piston_diametre = cote(_("Axe de piston : diamètre"))

    remarque = models.CharField(max_length=200, blank=True, verbose_name=_("Remarque"))

    class Meta:
        ordering = ["numero", "id"]
        verbose_name = _("Mesure cylindre")
        verbose_name_plural = _("Mesures cylindres")

    def __str__(self):
        return f"Cylindre {self.numero}"

    # ---- chemise
    @property
    def chemise_valeurs(self):
        return _valeurs(self.chemise_haut_a, self.chemise_haut_b, self.chemise_milieu_a,
                        self.chemise_milieu_b, self.chemise_bas_a, self.chemise_bas_b)

    @property
    def chemise_min(self):
        v = self.chemise_valeurs
        return min(v) if v else None

    @property
    def chemise_max(self):
        v = self.chemise_valeurs
        return max(v) if v else None

    @property
    def chemise_ovalisation(self):
        """Plus grand écart A / B sur une même hauteur."""
        e = [x for x in (_ecart(self.chemise_haut_a, self.chemise_haut_b),
                         _ecart(self.chemise_milieu_a, self.chemise_milieu_b),
                         _ecart(self.chemise_bas_a, self.chemise_bas_b)) if x is not None]
        return max(e) if e else None

    @property
    def chemise_conicite(self):
        """Plus grand écart haut / bas sur un même axe."""
        e = [x for x in (_ecart(self.chemise_haut_a, self.chemise_milieu_a, self.chemise_bas_a),
                         _ecart(self.chemise_haut_b, self.chemise_milieu_b, self.chemise_bas_b)) if x is not None]
        return max(e) if e else None

    # ---- piston
    @property
    def jeu_piston_min(self):
        if self.piston_diametre is None or self.chemise_min is None:
            return None
        return self.chemise_min - self.piston_diametre

    @property
    def jeu_piston_max(self):
        if self.piston_diametre is None or self.chemise_max is None:
            return None
        return self.chemise_max - self.piston_diametre

    # ---- maneton
    @property
    def maneton_valeurs(self):
        return _valeurs(self.maneton_1_a, self.maneton_1_b, self.maneton_2_a, self.maneton_2_b)

    @property
    def maneton_min(self):
        v = self.maneton_valeurs
        return min(v) if v else None

    @property
    def maneton_max(self):
        v = self.maneton_valeurs
        return max(v) if v else None

    @property
    def maneton_ovalisation(self):
        e = [x for x in (_ecart(self.maneton_1_a, self.maneton_1_b), _ecart(self.maneton_2_a, self.maneton_2_b))
             if x is not None]
        return max(e) if e else None

    @property
    def maneton_conicite(self):
        e = [x for x in (_ecart(self.maneton_1_a, self.maneton_2_a), _ecart(self.maneton_1_b, self.maneton_2_b))
             if x is not None]
        return max(e) if e else None

    # ---- pied de bielle
    @property
    def pied_bielle_ovalisation(self):
        return _ecart(self.pied_bielle_a, self.pied_bielle_b)

    @property
    def jeu_pied_bielle_min(self):
        v = _valeurs(self.pied_bielle_a, self.pied_bielle_b)
        if not v or self.axe_piston_diametre is None:
            return None
        return min(v) - self.axe_piston_diametre

    @property
    def jeu_pied_bielle_max(self):
        v = _valeurs(self.pied_bielle_a, self.pied_bielle_b)
        if not v or self.axe_piston_diametre is None:
            return None
        return max(v) - self.axe_piston_diametre

    def controles(self):
        """Liste des grandeurs contrôlées avec leur statut par rapport aux tolérances."""
        t = self.metrologie.tolerances_dict()
        lignes = [
            (_("Chemise : diamètre mini"), self.chemise_min, t["chemise_diametre_min"], t["chemise_diametre_max"]),
            (_("Chemise : diamètre maxi"), self.chemise_max, t["chemise_diametre_min"], t["chemise_diametre_max"]),
            (_("Chemise : ovalisation"), self.chemise_ovalisation, None, t["chemise_ovalisation_max"]),
            (_("Chemise : conicité"), self.chemise_conicite, None, t["chemise_conicite_max"]),
            (_("Jeu piston / chemise mini"), self.jeu_piston_min, t["jeu_piston_min"], t["jeu_piston_max"]),
            (_("Jeu piston / chemise maxi"), self.jeu_piston_max, t["jeu_piston_min"], t["jeu_piston_max"]),
            (_("Segment de feu : jeu à la coupe"), self.segment_feu_jeu, t["segment_feu_min"], t["segment_feu_max"]),
            (_("Segment d'étanchéité : jeu à la coupe"), self.segment_etancheite_jeu, t["segment_etancheite_min"], t["segment_etancheite_max"]),
            (_("Segment racleur : jeu à la coupe"), self.segment_racleur_jeu, t["segment_racleur_min"], t["segment_racleur_max"]),
            (_("Maneton : diamètre mini"), self.maneton_min, t["maneton_diametre_min"], t["maneton_diametre_max"]),
            (_("Maneton : diamètre maxi"), self.maneton_max, t["maneton_diametre_min"], t["maneton_diametre_max"]),
            (_("Maneton : ovalisation"), self.maneton_ovalisation, None, t["maneton_ovalisation_max"]),
            (_("Maneton : conicité"), self.maneton_conicite, None, t["maneton_conicite_max"]),
            (_("Pied de bielle : ovalisation"), self.pied_bielle_ovalisation, None, t["pied_bielle_ovalisation_max"]),
            (_("Jeu axe / pied de bielle mini"), self.jeu_pied_bielle_min, t["jeu_pied_bielle_min"], t["jeu_pied_bielle_max"]),
            (_("Jeu axe / pied de bielle maxi"), self.jeu_pied_bielle_max, t["jeu_pied_bielle_min"], t["jeu_pied_bielle_max"]),
        ]
        return [
            {"libelle": lib, "valeur": val, "mini": mini, "maxi": maxi, "statut": _verifier(val, mini, maxi)}
            for lib, val, mini, maxi in lignes if val is not None
        ]

    @property
    def nombre_hors_tolerance(self):
        return sum(1 for c in self.controles() if c["statut"] == StatutCote.HORS)


# =====================================================================
# MESURES PAR TOURILLON (palier de vilebrequin)
# =====================================================================
class MesureTourillon(models.Model):
    metrologie = models.ForeignKey(MetrologieMoteur, on_delete=models.CASCADE, related_name="tourillons",
                                   verbose_name=_("Métrologie"))
    numero = models.PositiveSmallIntegerField(verbose_name=_("Tourillon n°"))

    section_1_a = cote(_("Tourillon section 1 – axe A"))
    section_1_b = cote(_("Tourillon section 1 – axe B"))
    section_2_a = cote(_("Tourillon section 2 – axe A"))
    section_2_b = cote(_("Tourillon section 2 – axe B"))

    remarque = models.CharField(max_length=200, blank=True, verbose_name=_("Remarque"))

    class Meta:
        ordering = ["numero", "id"]
        verbose_name = _("Mesure tourillon")
        verbose_name_plural = _("Mesures tourillons")

    def __str__(self):
        return f"Tourillon {self.numero}"

    @property
    def valeurs(self):
        return _valeurs(self.section_1_a, self.section_1_b, self.section_2_a, self.section_2_b)

    @property
    def diametre_min(self):
        v = self.valeurs
        return min(v) if v else None

    @property
    def diametre_max(self):
        v = self.valeurs
        return max(v) if v else None

    @property
    def ovalisation(self):
        e = [x for x in (_ecart(self.section_1_a, self.section_1_b), _ecart(self.section_2_a, self.section_2_b))
             if x is not None]
        return max(e) if e else None

    @property
    def conicite(self):
        e = [x for x in (_ecart(self.section_1_a, self.section_2_a), _ecart(self.section_1_b, self.section_2_b))
             if x is not None]
        return max(e) if e else None

    def controles(self):
        t = self.metrologie.tolerances_dict()
        lignes = [
            (_("Tourillon : diamètre mini"), self.diametre_min, t["tourillon_diametre_min"], t["tourillon_diametre_max"]),
            (_("Tourillon : diamètre maxi"), self.diametre_max, t["tourillon_diametre_min"], t["tourillon_diametre_max"]),
            (_("Tourillon : ovalisation"), self.ovalisation, None, t["tourillon_ovalisation_max"]),
            (_("Tourillon : conicité"), self.conicite, None, t["tourillon_conicite_max"]),
        ]
        return [
            {"libelle": lib, "valeur": val, "mini": mini, "maxi": maxi, "statut": _verifier(val, mini, maxi)}
            for lib, val, mini, maxi in lignes if val is not None
        ]

    @property
    def nombre_hors_tolerance(self):
        return sum(1 for c in self.controles() if c["statut"] == StatutCote.HORS)
