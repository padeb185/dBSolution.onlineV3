import uuid
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class FabricantJante(models.TextChoices):
    CONSTRUCTEUR_OEM = "CONSTRUCTEUR_OEM", _("Constructeur (origine)")
    ADVAN = "ADVAN", "Advan (Yokohama)"
    AEZ = "AEZ", "AEZ"
    ALPINA = "ALPINA", "Alpina"
    APEX = "APEX", "Apex"
    ATS = "ATS", "ATS"
    BBS = "BBS", "BBS"
    BC_FORGED = "BC_FORGED", "BC Forged"
    BORBET = "BORBET", "Borbet"
    BRAID = "BRAID", "Braid"
    BRIXTON = "BRIXTON", "Brixton Forged"
    COMPOMOTIVE = "COMPOMOTIVE", "Compomotive"
    CROMODORA = "CROMODORA", "Cromodora"
    DOTZ = "DOTZ", "Dotz"
    ENKEI = "ENKEI", "Enkei"
    FONDMETAL = "FONDMETAL", "Fondmetal"
    FORGELINE = "FORGELINE", "Forgeline"
    FUCHS = "FUCHS", "Fuchs"
    GOTTI = "GOTTI", "Gotti"
    HRE = "HRE", "HRE"
    JAPAN_RACING = "JAPAN_RACING", "Japan Racing"
    KONIG = "KONIG", "Konig"
    MAK = "MAK", "MAK"
    MOMO = "MOMO", "Momo"
    MSW = "MSW", "MSW (OZ)"
    OZ = "OZ", "OZ Racing"
    RAYS = "RAYS", "Rays / Volk Racing"
    RIAL = "RIAL", "Rial"
    RONAL = "RONAL", "Ronal"
    ROTIFORM = "ROTIFORM", "Rotiform"
    SPARCO = "SPARCO", "Sparco"
    SPEEDLINE = "SPEEDLINE", "Speedline Corse"
    TEAM_DYNAMICS = "TEAM_DYNAMICS", "Team Dynamics"
    VOSSEN = "VOSSEN", "Vossen"
    WEDS = "WEDS", "Weds"
    WORK = "WORK", "Work Wheels"
    AUTRE = "AUTRE", _("Autre")


class MatiereJante(models.TextChoices):
    ALU_COULE = "ALU_COULE", _("Aluminium coulé")
    ALU_FLOW_FORMING = "ALU_FLOW_FORMING", _("Aluminium flow-forming")
    ALU_FORGE = "ALU_FORGE", _("Aluminium forgé")
    ACIER = "ACIER", _("Acier (tôle)")
    MAGNESIUM = "MAGNESIUM", _("Magnésium")
    CARBONE = "CARBONE", _("Carbone")
    CARBONE_ALU = "CARBONE_ALU", _("Hybride carbone / aluminium")


class ConstructionJante(models.TextChoices):
    MONOBLOC = "MONOBLOC", _("1 pièce (monobloc)")
    DEUX_PIECES = "DEUX_PIECES", _("2 pièces")
    TROIS_PIECES = "TROIS_PIECES", _("3 pièces")


class ProfilRebord(models.TextChoices):
    J = "J", "J"
    JJ = "JJ", "JJ"
    JK = "JK", "JK"
    K = "K", "K"
    B = "B", "B"
    P = "P", "P"


class NombreFixations(models.IntegerChoices):
    ECROU_CENTRAL = 1, _("Écrou central (centerlock)")
    TROIS = 3, "3"
    QUATRE = 4, "4"
    CINQ = 5, "5"
    SIX = 6, "6"
    HUIT = 8, "8"


# Valeurs à une décimale (« 18.0 ») : identiques à ce que renvoie la base,
# pour que le menu déroulant retrouve la valeur enregistrée.
DIAMETRES = sorted(
    (Decimal(f"{d:.1f}"), f'{d:g}"'.replace(".", ","))
    for d in (10, 12, 13, 14, 15, 16, 16.5, 17, 18, 19, 20, 21, 22, 23, 24)
)


class VoitureJante(models.Model):
    """Jeu de jantes du catalogue de la société, lié à un ou plusieurs véhicules."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="jantes",
        null=True,
        blank=True,
    )

    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="jantes",
        blank=True,
    )
    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="jantes",
        blank=True,
        verbose_name=_("Véhicules"),
    )

    # ---------------- Identification ----------------
    fabricant = models.CharField(
        max_length=30, choices=FabricantJante.choices,
        default=FabricantJante.CONSTRUCTEUR_OEM, verbose_name=_("Fabricant"),
    )
    nom_modele = models.CharField(max_length=80, blank=True, default="", verbose_name=_("Modèle de jante"))
    reference = models.CharField(max_length=50, blank=True, default="", verbose_name=_("Référence / n° OEM"))
    origine = models.BooleanField(default=True, verbose_name=_("Jantes d'origine"))
    competition = models.BooleanField(default=False, verbose_name=_("Jantes compétition"))

    # ---------------- Construction ----------------
    matiere = models.CharField(
        max_length=20, choices=MatiereJante.choices,
        default=MatiereJante.ALU_COULE, verbose_name=_("Matière"),
    )
    construction = models.CharField(
        max_length=15, choices=ConstructionJante.choices,
        default=ConstructionJante.MONOBLOC, verbose_name=_("Jante en pièces"),
    )
    finition = models.CharField(max_length=60, blank=True, default="", verbose_name=_("Couleur / finition"))

    # ---------------- Fixation ----------------
    nombre_fixations = models.PositiveSmallIntegerField(
        choices=NombreFixations.choices, default=NombreFixations.CINQ,
        verbose_name=_("Nombre de goujons / vis"),
    )
    entraxe_mm = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal("70")), MaxValueValidator(Decimal("210"))],
        verbose_name=_("Entraxe (PCD, mm)"),
        help_text=_("Ex. 105 pour une jante 5x105."),
    )
    alesage_mm = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal("40")), MaxValueValidator(Decimal("170"))],
        verbose_name=_("Alésage central (mm)"),
    )

    # ---------------- Dimensions avant ----------------
    diametre_av = models.DecimalField(
        max_digits=4, decimal_places=1, choices=DIAMETRES, default=Decimal("17.0"),
        verbose_name=_("Diamètre avant (pouces)"),
    )
    largeur_av = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal("7.5"),
        validators=[MinValueValidator(Decimal("3")), MaxValueValidator(Decimal("16"))],
        verbose_name=_("Largeur avant (J, pouces)"),
    )
    profil = models.CharField(
        max_length=10, choices=ProfilRebord.choices, default=ProfilRebord.J,
        verbose_name=_("Profil du rebord"),
    )
    deport_av = models.SmallIntegerField(
        default=35,
        validators=[MinValueValidator(-80), MaxValueValidator(120)],
        verbose_name=_("Déport avant (ET, mm)"),
    )

    # ---------------- Dimensions arrière ----------------
    diametre_ar = models.DecimalField(
        max_digits=4, decimal_places=1, choices=DIAMETRES, default=Decimal("17.0"),
        verbose_name=_("Diamètre arrière (pouces)"),
    )
    largeur_ar = models.DecimalField(
        max_digits=4, decimal_places=1, default=Decimal("7.5"),
        validators=[MinValueValidator(Decimal("3")), MaxValueValidator(Decimal("16"))],
        verbose_name=_("Largeur arrière (J, pouces)"),
    )
    deport_ar = models.SmallIntegerField(
        default=35,
        validators=[MinValueValidator(-80), MaxValueValidator(120)],
        verbose_name=_("Déport arrière (ET, mm)"),
    )

    # ---------------- Caractéristiques ----------------
    poids_kg = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=_("Poids par jante (kg)"),
    )
    charge_max_kg = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Charge maximale (kg)"))
    quantite = models.PositiveSmallIntegerField(default=4, verbose_name=_("Nombre de jantes"))

    # ---------------- Achat ----------------
    prix_achat = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat HTVA (jeu)"),
    )
    date_achat = models.DateField(null=True, blank=True, verbose_name=_("Date d'achat"))

    remarques = models.TextField(blank=True, default="", verbose_name=_("Remarques"))

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = _("Jante")
        verbose_name_plural = _("Jantes")
        ordering = ["fabricant", "nom_modele"]

    # ---------------- Affichage ----------------
    @staticmethod
    def _nombre(valeur):
        if valeur is None:
            return ""
        texte = f"{Decimal(valeur).normalize():f}"
        return texte.replace(".", ",")

    @property
    def entraxe(self):
        """« 5x105 », « Écrou central » ou ''."""
        if self.nombre_fixations == NombreFixations.ECROU_CENTRAL:
            return str(_("Écrou central"))
        if not self.entraxe_mm:
            return ""
        return f"{self.nombre_fixations}x{self._nombre(self.entraxe_mm)}"

    def _dimension(self, largeur, diametre, deport):
        return f"{self._nombre(largeur)}{self.profil} x {self._nombre(diametre)} ET{deport}"

    @property
    def dimension_av(self):
        return self._dimension(self.largeur_av, self.diametre_av, self.deport_av)

    @property
    def dimension_ar(self):
        return self._dimension(self.largeur_ar, self.diametre_ar, self.deport_ar)

    @property
    def est_decalee(self):
        return (self.diametre_av, self.largeur_av, self.deport_av) != (self.diametre_ar, self.largeur_ar, self.deport_ar)

    @property
    def libelle(self):
        nom = self.get_fabricant_display()
        if self.nom_modele:
            nom = f"{nom} {self.nom_modele}"
        return nom

    def __str__(self):
        dims = self.dimension_av if not self.est_decalee else f"{self.dimension_av} / {self.dimension_ar}"
        entraxe = f" – {self.entraxe}" if self.entraxe else ""
        return f"{self.libelle} {dims}{entraxe}"
