"""
Parking : plan en grille (lignes A–Z × emplacements 1–X), dimensions en mètres.

Chaque case du plan est :
  - un box vertical (par défaut, voiture garée de haut en bas) ou horizontal (voiture garée de gauche à droite) :
    code « lettre + numéro » (A1, B12…), une seule immatriculation à la fois ;
  - une ligne d'accès (allée de circulation) ;
  - une zone inaccessible (coins, piliers…).
Le plan ne stocke que les cases qui ne sont pas des box verticaux : {"A1": "ACCES", "B3": "BOX_H", "J50": "BLOQUE"}.
"""
import re
import string
from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

LETTRES = string.ascii_uppercase  # A–Z : 26 lignes au maximum
MAX_LIGNES = 26
MAX_EMPLACEMENTS = 200


TYPES_BOX = ("BOX", "BOX_H")   # box vertical (voiture garée de haut en bas) / horizontal (de gauche à droite)


class TypeCase(models.TextChoices):
    BOX = "BOX", _("Box vertical")
    BOX_H = "BOX_H", _("Box horizontal")
    ACCES = "ACCES", _("Ligne d'accès")
    BLOQUE = "BLOQUE", _("Zone inaccessible")
    VIDE = "VIDE", _("Sans case")   # la case n'existe pas (ligne plus courte, forme irrégulière)


RE_CODE = re.compile(r"^([A-Z])([1-9][0-9]{0,2})$")

PAYS_DEFAUT = "Belgique"

# Mise en forme des plaques (mêmes couleurs que components/plaque.html) :
# pays -> (code du pays sur la bande, fond, texte, bordure, étoiles UE)
STYLES_PLAQUE = {
    "Belgique": ("B", "#FFFFFF", "#8B0000", "#8B0000", True),
    "Luxembourg": ("L", "#FFEB3B", "#000000", "#000000", True),
    "Pays-Bas": ("NL", "#F7C600", "#000000", "#000000", True),
    "France": ("F", "#FFFFFF", "#000000", "#000000", True),
    "Allemagne": ("D", "#FFFFFF", "#000000", "#000000", True),
    "Autriche": ("A", "#FFFFFF", "#000000", "#C8102E", True),
    "Irlande": ("IRL", "#FFFFFF", "#000000", "#000000", True),
    "Italie": ("I", "#FFFFFF", "#000000", "#000000", True),
    "Espagne": ("E", "#FFFFFF", "#000000", "#000000", True),
    "Portugal": ("P", "#FFFFFF", "#000000", "#000000", True),
    "Grèce": ("GR", "#FFFFFF", "#000000", "#000000", True),
    "Chypre": ("CY", "#FFFFFF", "#000000", "#000000", True),
    "Malte": ("M", "#FFFFFF", "#000000", "#000000", True),
    "Danemark": ("DK", "#FFFFFF", "#000000", "#C8102E", True),
    "Suède": ("S", "#FFFFFF", "#000000", "#000000", True),
    "Finlande": ("FIN", "#FFFFFF", "#000000", "#000000", True),
    "Estonie": ("EST", "#FFFFFF", "#000000", "#000000", True),
    "Lettonie": ("LV", "#FFFFFF", "#000000", "#000000", True),
    "Lituanie": ("LT", "#FFFFFF", "#000000", "#000000", True),
    "Pologne": ("PL", "#FFFFFF", "#000000", "#000000", True),
    "Tchéquie": ("CZ", "#FFFFFF", "#000000", "#000000", True),
    "Slovaquie": ("SK", "#FFFFFF", "#000000", "#000000", True),
    "Hongrie": ("H", "#FFFFFF", "#000000", "#000000", True),
    "Slovénie": ("SLO", "#FFFFFF", "#000000", "#00843D", True),
    "Croatie": ("HR", "#FFFFFF", "#000000", "#000000", True),
    "Roumanie": ("RO", "#FFFFFF", "#000000", "#000000", True),
    "Bulgarie": ("BG", "#FFFFFF", "#000000", "#000000", True),
    "Royaume-Uni": ("UK", "#FFFFFF", "#000000", "#000000", False),
    "Norvège": ("N", "#FFFFFF", "#000000", "#000000", False),
    "Suisse": ("CH", "#FFFFFF", "#000000", "#000000", False),
}


def style_plaque(pays):
    """{"pays", "code", "fond", "texte", "bordure", "etoiles", "bande", "suisse"} pour dessiner la plaque."""
    code, fond, texte, bordure, etoiles = STYLES_PLAQUE.get(pays or "", ("", "#FFFFFF", "#000000", "#9CA3AF", False))
    return {"pays": pays or "", "code": code, "fond": fond, "texte": texte, "bordure": bordure,
            "etoiles": etoiles, "bande": bool(code) and pays != "Suisse", "suisse": pays == "Suisse"}


def normaliser_immatriculation(valeur):
    """Majuscules, séparateurs ramenés à un tiret (comparaison des plaques)."""
    texte = re.sub(r"[\s\-‐-―._·/]+", "-", (valeur or "").strip().upper()).strip("-")
    return texte[:12]


def cle_plaque(valeur):
    """Plaque sans séparateurs : 1-ABC-123 et 1ABC123 sont la même plaque."""
    return re.sub(r"[^A-Z0-9]", "", (valeur or "").upper())


class Parking(models.Model):
    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="parkings",
        verbose_name=_("Société"),
    )
    nom = models.CharField(_("Nom du parking"), max_length=100)

    # Dimensions réelles (mètres) : largeur = sens des emplacements (1 → X), longueur = sens des lignes (A → Z)
    largeur_m = models.DecimalField(
        _("Largeur (m)"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal("1"))],
        help_text=_("Sens des emplacements 1 → X."),
    )
    longueur_m = models.DecimalField(
        _("Longueur (m)"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(Decimal("1"))],
        help_text=_("Sens des lignes A → Z."),
    )
    nombre_lignes = models.PositiveSmallIntegerField(
        _("Nombre de lignes (A–Z)"), default=10,
        validators=[MinValueValidator(1), MaxValueValidator(MAX_LIGNES)],
    )
    nombre_emplacements = models.PositiveSmallIntegerField(
        _("Emplacements par ligne (1–X)"), default=50,
        validators=[MinValueValidator(1), MaxValueValidator(MAX_EMPLACEMENTS)],
    )

    # Dimensions réelles d'un box (m) : vertical = largeur × longueur (2,50 × 5,00), horizontal = l'inverse
    box_largeur_m = models.DecimalField(
        _("Largeur d'un box (m)"), max_digits=5, decimal_places=2, default=Decimal("2.50"),
        validators=[MinValueValidator(Decimal("1"))],
        help_text=_("Box vertical : largeur × longueur. Box horizontal : longueur × largeur."),
    )
    box_longueur_m = models.DecimalField(
        _("Longueur d'un box (m)"), max_digits=5, decimal_places=2, default=Decimal("5.00"),
        validators=[MinValueValidator(Decimal("1"))],
    )
    largeur_allee_m = models.DecimalField(
        _("Largeur d'une ligne d'accès (m)"), max_digits=5, decimal_places=2, default=Decimal("6.00"),
        validators=[MinValueValidator(Decimal("1"))],
        help_text=_("Profondeur d'une ligne entièrement en accès (allée de circulation)."),
    )

    # Cases qui ne sont pas des box : {"A1": "ACCES", "J50": "BLOQUE"}
    plan = models.JSONField(_("Plan"), default=dict, blank=True)

    remarques = models.TextField(_("Remarques"), blank=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Parking")
        verbose_name_plural = _("Parkings")
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    # -------------------------
    # Géométrie
    # -------------------------
    @property
    def lettres(self):
        return list(LETTRES[: self.nombre_lignes or 0])

    @property
    def numeros(self):
        return list(range(1, (self.nombre_emplacements or 0) + 1))

    @property
    def largeur_case_m(self):
        """Largeur d'une case (m) = largeur du parking / emplacements par ligne."""
        if not self.nombre_emplacements:
            return Decimal("0")
        return (Decimal(self.largeur_m) / self.nombre_emplacements).quantize(Decimal("0.01"), ROUND_HALF_UP)

    @property
    def longueur_case_m(self):
        """Profondeur d'une case (m) = longueur du parking / nombre de lignes."""
        if not self.nombre_lignes:
            return Decimal("0")
        return (Decimal(self.longueur_m) / self.nombre_lignes).quantize(Decimal("0.01"), ROUND_HALF_UP)

    @property
    def ratio_case_css(self):
        """Longueur / largeur d'un box vertical (éditeur du plan), avec un point décimal pour le CSS."""
        largeur = Decimal(self.box_largeur_m or 0)
        if not largeur:
            return "1"
        ratio = Decimal(self.box_longueur_m or 0) / largeur
        ratio = min(max(ratio, Decimal("0.25")), Decimal("4"))
        return f"{ratio:.3f}"

    @property
    def surface_m2(self):
        return (Decimal(self.largeur_m) * Decimal(self.longueur_m)).quantize(Decimal("0.01"), ROUND_HALF_UP)

    def code_valide(self, code):
        m = RE_CODE.match(code or "")
        if not m:
            return False
        lettre, numero = m.group(1), int(m.group(2))
        return lettre in self.lettres and 1 <= numero <= (self.nombre_emplacements or 0)

    def type_case(self, code):
        return (self.plan or {}).get(code, TypeCase.BOX)

    def est_box(self, code):
        return self.code_valide(code) and self.type_case(code) in TYPES_BOX

    def codes_box(self):
        return [f"{l}{n}" for l in self.lettres for n in self.numeros if self.type_case(f"{l}{n}") in TYPES_BOX]

    @property
    def nombre_box(self):
        total = len(self.lettres) * len(self.numeros)
        hors_box = sum(1 for code, t in (self.plan or {}).items() if t not in TYPES_BOX and self.code_valide(code))
        return total - hors_box

    @property
    def nombre_occupes(self):
        return self.occupations.count()

    @property
    def nombre_libres(self):
        return max(self.nombre_box - self.nombre_occupes, 0)

    # -------------------------
    # Plan
    # -------------------------
    @staticmethod
    def nettoyer_plan(plan, lettres, nombre_emplacements):
        """Garde les cases valides qui ne sont pas des box."""
        propre = {}
        for code, t in (plan or {}).items():
            code = str(code).upper()
            m = RE_CODE.match(code)
            if not m or t not in (TypeCase.BOX_H, TypeCase.ACCES, TypeCase.BLOQUE, TypeCase.VIDE):
                continue
            if m.group(1) in lettres and 1 <= int(m.group(2)) <= nombre_emplacements:
                propre[code] = t
        return propre

    def grille(self):
        """Lignes du plan pour l'affichage : [{"lettre", "cases": [{"code", "numero", "type", "occupation"}]}]."""
        occupations = {o.code: o for o in self.occupations.select_related(
            "vehicule", "vehicule__voiture_marque", "vehicule__voiture_modele")}
        plan = self.plan or {}
        return [
            {
                "lettre": l,
                "cases": [
                    {
                        "code": f"{l}{n}",
                        "numero": n,
                        "type": plan.get(f"{l}{n}", TypeCase.BOX),
                        "est_box": plan.get(f"{l}{n}", TypeCase.BOX) in TYPES_BOX,
                        "occupation": occupations.get(f"{l}{n}"),
                    }
                    for n in self.numeros
                ],
            }
            for l in self.lettres
        ]

    def dimensions_case(self, type_case, hauteur_ligne=None):
        """(largeur, hauteur) en mètres d'une case : box vertical 2,5 × 5, box horizontal 5 × 2,5, autre = largeur d'un box."""
        l, L = Decimal(self.box_largeur_m), Decimal(self.box_longueur_m)
        if type_case == TypeCase.BOX_H:
            return L, l
        if type_case == TypeCase.BOX:
            return l, L
        if type_case == TypeCase.VIDE:
            return Decimal("0"), Decimal("0")
        return l, hauteur_ligne

    def dessin(self):
        """
        Plan à l'échelle (mètres) : chaque ligne A–Z est une rangée de cases de tailles réelles.
        Hauteur d'une rangée = plus grand box de la rangée (largeur d'allée si la rangée n'a aucun box).
        """
        grille = self.grille()
        rangees = []
        largeur_max = Decimal("0")
        hauteur_totale = Decimal("0")
        for ligne in grille:
            hauteurs = [self.dimensions_case(c["type"])[1] for c in ligne["cases"] if c["est_box"]]
            hauteur = max(hauteurs) if hauteurs else Decimal(self.largeur_allee_m)
            longueur = Decimal("0")
            for c in ligne["cases"]:
                w, h = self.dimensions_case(c["type"], hauteur)
                c["largeur_m"], c["hauteur_m"] = w, h
                c["largeur_css"], c["hauteur_css"] = f"{w:.3f}", f"{h:.3f}"
                c["horizontal"] = c["type"] == TypeCase.BOX_H
                c["vide"] = c["type"] == TypeCase.VIDE
                longueur += w
            ligne.update(hauteur_m=hauteur, hauteur_css=f"{hauteur:.3f}", longueur_m=longueur,
                         trop_longue=longueur > Decimal(self.largeur_m))
            largeur_max = max(largeur_max, longueur)
            hauteur_totale += hauteur
            rangees.append(ligne)
        return {
            "rangees": rangees,
            "largeur_m": largeur_max,
            "hauteur_m": hauteur_totale,
            "largeur_css": f"{largeur_max:.3f}",
            "hauteur_css": f"{hauteur_totale:.3f}",
            "trop_profond": hauteur_totale > Decimal(self.longueur_m),
            "lignes_trop_longues": [r["lettre"] for r in rangees if r["trop_longue"]],
            "cases_max": max((sum(1 for c in r["cases"] if not c["vide"]) for r in rangees), default=0),
        }

    def codes_occupes_hors_box(self, lettres=None, nombre_emplacements=None, plan=None):
        """Box occupés qui ne seraient plus des box (plan modifié ou parking réduit)."""
        lettres = lettres if lettres is not None else self.lettres
        nombre_emplacements = nombre_emplacements if nombre_emplacements is not None else self.nombre_emplacements
        plan = plan if plan is not None else (self.plan or {})
        bloques = []
        for o in self.occupations.all():
            m = RE_CODE.match(o.code)
            hors_grille = not m or m.group(1) not in lettres or int(m.group(2)) > nombre_emplacements
            if hors_grille or plan.get(o.code, TypeCase.BOX) not in TYPES_BOX:
                bloques.append(o.code)
        return sorted(bloques)

    def clean(self):
        if self.pk:
            lettres = list(LETTRES[: self.nombre_lignes or 0])
            bloques = self.codes_occupes_hors_box(lettres, self.nombre_emplacements or 0)
            if bloques:
                raise ValidationError(
                    _("Ces box sont occupés et sortiraient du parking : %(codes)s. Libérez-les d'abord.")
                    % {"codes": ", ".join(bloques)}
                )


class OccupationBox(models.Model):
    """Un box occupé : une seule immatriculation par box, un véhicule dans un seul box."""

    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name="occupations",
                                verbose_name=_("Parking"))
    code = models.CharField(_("Box"), max_length=4)
    vehicule = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boxes_parking",
        verbose_name=_("Véhicule"),
    )
    immatriculation = models.CharField(_("Immatriculation"), max_length=12)
    pays = models.CharField(_("Pays de la plaque"), max_length=20, default=PAYS_DEFAUT, blank=True)
    remarque = models.CharField(_("Remarque"), max_length=120, blank=True)
    depuis = models.DateTimeField(_("Depuis le"), default=timezone.now)
    modifie_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Modifié par"),
    )

    class Meta:
        verbose_name = _("Box occupé")
        verbose_name_plural = _("Box occupés")
        ordering = ["parking", "code"]
        constraints = [
            models.UniqueConstraint(fields=["parking", "code"], name="parking_box_unique"),
        ]

    def __str__(self):
        return f"{self.parking} – {self.code} : {self.immatriculation}"

    @property
    def pays_plaque(self):
        """Pays de la plaque : celui du véhicule enregistré, sinon celui saisi pour le box."""
        return (getattr(self.vehicule, "pays", None) if self.vehicule_id else None) or self.pays or PAYS_DEFAUT

    @property
    def plaque(self):
        return style_plaque(self.pays_plaque)

    @property
    def libelle_vehicule(self):
        v = self.vehicule
        if not v:
            return ""
        return f"{v.voiture_marque.nom_marque} {v.voiture_modele.nom_modele}".strip()
