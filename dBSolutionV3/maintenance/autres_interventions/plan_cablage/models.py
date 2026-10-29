"""
Plan de câblage d'un véhicule (fiche technique, sans facturation).

    PlanCablage        : câblage d'origine ou custom, nom du boîtier électronique (ECU, PDM…)
      └ ConnecteurCablage : branche vers un composant (ex. injecteur 1) – longueur, coudes, référence du connecteur
          └ FilCablage    : pin du boîtier → position / n° de pin du connecteur, couleur du fil / couleur de la bande,
                            fonction (+, −, signal…), section

Exemple : injecteur, 3 fils (+ rouge, − noir, signal jaune/blanc), 160 cm, deux coudes.
"""
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TypeCablage(models.TextChoices):
    ORIGINE = "ORIGINE", _("Câblage d'origine")
    CUSTOM = "CUSTOM", _("Câblage custom")


class CouleurFil(models.TextChoices):
    NOIR = "NOIR", _("Noir")
    ROUGE = "ROUGE", _("Rouge")
    JAUNE = "JAUNE", _("Jaune")
    VERT = "VERT", _("Vert")
    BLEU = "BLEU", _("Bleu")
    BLANC = "BLANC", _("Blanc")
    MARRON = "MARRON", _("Marron")
    GRIS = "GRIS", _("Gris")
    ORANGE = "ORANGE", _("Orange")
    VIOLET = "VIOLET", _("Violet")
    ROSE = "ROSE", _("Rose")
    BEIGE = "BEIGE", _("Beige")
    VERT_CLAIR = "VERT_CLAIR", _("Vert clair")
    BLEU_CLAIR = "BLEU_CLAIR", _("Bleu clair")
    TRANSPARENT = "TRANSPARENT", _("Transparent")


# Couleurs d'affichage (pastilles)
COULEURS_HEX = {
    "NOIR": "#111827", "ROUGE": "#dc2626", "JAUNE": "#facc15", "VERT": "#16a34a", "BLEU": "#2563eb",
    "BLANC": "#ffffff", "MARRON": "#7c2d12", "GRIS": "#9ca3af", "ORANGE": "#f97316", "VIOLET": "#7c3aed",
    "ROSE": "#f472b6", "BEIGE": "#e7d7b1", "VERT_CLAIR": "#86efac", "BLEU_CLAIR": "#7dd3fc",
    "TRANSPARENT": "#f3f4f6",
}


class FonctionFil(models.TextChoices):
    PLUS = "PLUS", _("+ Alimentation")
    PLUS_APC = "PLUS_APC", _("+ Après contact")
    MOINS = "MOINS", _("− Masse")
    SIGNAL = "SIGNAL", _("Signal")
    COMMANDE = "COMMANDE", _("Commande (pilotage)")
    REFERENCE_5V = "REF_5V", _("Référence 5 V")
    MASSE_CAPTEUR = "MASSE_CAPT", _("Masse capteur")
    CAN_H = "CAN_H", _("CAN High")
    CAN_L = "CAN_L", _("CAN Low")
    LIN = "LIN", _("LIN")
    BLINDAGE = "BLINDAGE", _("Blindage")
    AUTRE = "AUTRE", _("Autre")


class PlanCablage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, related_name="plans_cablage",
                                null=True, blank=True)
    voiture_exemplaire = models.ForeignKey("voiture_exemplaire.VoitureExemplaire", on_delete=models.CASCADE,
                                           related_name="plans_cablage", verbose_name=_("Véhicule"))

    type_cablage = models.CharField(_("Type de câblage"), max_length=10, choices=TypeCablage.choices,
                                    default=TypeCablage.ORIGINE)
    nom = models.CharField(_("Nom du faisceau"), max_length=120, blank=True,
                           help_text=_("Ex. : faisceau moteur, faisceau habitacle…"))
    nom_boitier = models.CharField(_("Nom du boîtier électronique"), max_length=120,
                                   help_text=_("Ex. : Bosch ME7.5, MoTeC M150, PDM…"))
    reference_boitier = models.CharField(_("Référence du boîtier"), max_length=120, blank=True)
    remarques = models.TextField(_("Remarques"), blank=True)

    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="plans_cablage_crees", editable=False)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True)

    class Meta:
        verbose_name = _("Plan de câblage")
        verbose_name_plural = _("Plans de câblage")
        ordering = ["type_cablage", "nom_boitier", "nom"]

    def __str__(self):
        return " – ".join(x for x in (self.nom_boitier, self.nom) if x) or str(_("Plan de câblage"))

    @property
    def nombre_connecteurs(self):
        return self.connecteurs.count()

    @property
    def nombre_fils(self):
        return FilCablage.objects.filter(connecteur__plan=self).count()

    @property
    def longueur_totale_cm(self):
        """Longueur de fil totale : longueur de chaque branche × nombre de fils."""
        total = 0
        for c in self.connecteurs.all():
            total += (c.longueur_cm or 0) * c.fils.count()
        return total


class ConnecteurCablage(models.Model):
    """Branche du faisceau vers un composant (injecteur, capteur, actionneur…)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plan = models.ForeignKey(PlanCablage, on_delete=models.CASCADE, related_name="connecteurs")
    nom = models.CharField(_("Composant / connecteur"), max_length=120,
                           help_text=_("Ex. : injecteur cylindre 1, capteur PMH, sonde lambda…"))
    reference_connecteur = models.CharField(_("Référence du connecteur"), max_length=120, blank=True,
                                            help_text=_("Ex. : Bosch EV1 2 voies, Deutsch DTM 3 voies…"))
    longueur_cm = models.PositiveIntegerField(_("Longueur (cm)"), null=True, blank=True)
    nombre_coudes = models.PositiveSmallIntegerField(_("Nombre de coudes"), default=0)
    gaine = models.CharField(_("Gaine / protection"), max_length=120, blank=True,
                             help_text=_("Ex. : DR-25, gaine tressée, thermo…"))
    remarques = models.CharField(_("Remarques"), max_length=255, blank=True)
    ordre = models.PositiveSmallIntegerField(_("Ordre"), default=0)

    class Meta:
        verbose_name = _("Connecteur")
        verbose_name_plural = _("Connecteurs")
        ordering = ["ordre", "nom"]

    def __str__(self):
        return self.nom

    @property
    def nombre_fils(self):
        return self.fils.count()


class FilCablage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connecteur = models.ForeignKey(ConnecteurCablage, on_delete=models.CASCADE, related_name="fils")
    pin_boitier = models.CharField(_("Pin boîtier"), max_length=20, blank=True, help_text=_("Ex. : A12, 45"))
    pin_connecteur = models.CharField(_("Pin connecteur (position)"), max_length=20, blank=True,
                                      help_text=_("Position / numéro de pin dans le connecteur"))
    couleur_fil = models.CharField(_("Couleur du fil"), max_length=12, choices=CouleurFil.choices)
    couleur_bande = models.CharField(_("Couleur de la bande"), max_length=12, choices=CouleurFil.choices,
                                     blank=True, help_text=_("Fil bicolore : ex. jaune / blanc"))
    fonction = models.CharField(_("Fonction"), max_length=12, choices=FonctionFil.choices,
                                default=FonctionFil.SIGNAL)
    description = models.CharField(_("Description"), max_length=120, blank=True,
                                   help_text=_("Ex. : commande injecteur 1"))
    section_mm2 = models.DecimalField(_("Section (mm²)"), max_digits=4, decimal_places=2, null=True, blank=True,
                                      validators=[MinValueValidator(0)])
    ordre = models.PositiveSmallIntegerField(_("Ordre"), default=0)

    class Meta:
        verbose_name = _("Fil")
        verbose_name_plural = _("Fils")
        ordering = ["ordre", "pin_connecteur"]

    def __str__(self):
        return f"{self.libelle_couleur} – {self.get_fonction_display()}"

    @property
    def libelle_couleur(self):
        """Ex. « Jaune / Blanc »."""
        if self.couleur_bande:
            return f"{self.get_couleur_fil_display()} / {self.get_couleur_bande_display()}"
        return str(self.get_couleur_fil_display())

    @property
    def hex_fil(self):
        return COULEURS_HEX.get(self.couleur_fil, "#ffffff")

    @property
    def hex_bande(self):
        return COULEURS_HEX.get(self.couleur_bande) if self.couleur_bande else None
