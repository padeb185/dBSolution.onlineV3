from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece


class Cote(models.TextChoices):
    GAUCHE = "GA", _("Gauche")
    DROIT = "DR", _("Droit")


class Emplacement(models.TextChoices):
    AVANT = "AV", _("Avant")
    ARRIERE = "AR", _("Arrière")


class LibelleCarrosserie(models.TextChoices):
    PARE_CHOCS = "PARE_CHOCS", _("Pare-chocs")
    BOUCLIER = "BOUCLIER", _("Bouclier")
    PARE_BRIS = "PARE_BRIS", _("Pare-brise")
    VITRE_PORTE = "VITRE_PORTE", _("Vitres de porte")
    LUNETTE = "LUNETTE", _("Lunette")
    RETROVISEUR = "RETROVISEUR", _("Rétroviseur")
    AILE = "AILE", _("Aile")
    ELARGISSEUR_AILE = "ELARG_AILE", _("Élargisseur d’aile")
    BAS_DE_CAISSE = "BAS_CAISSE", _("Bas de caisse")
    SUPPORT_RADIATEUR = "SUPP_RAD", _("Support de radiateur")
    SUPPORT_PARE_CHOC = "SUPP_PC", _("Support de pare-chocs")
    PORTE = "PORTE", _("Porte")
    POIGNEE_PORTE = "POIGNEE", _("Poignée de porte")
    COFFRE_HAILLON = "COFFRE", _("Coffre / hayon")
    JOINT_COFFRE = "JOINT_COFFRE", _("Joint de coffre")
    JOINT_PORTE = "JOINT_PORTE", _("Joint de porte")
    COQUILLE_AILE = "COQUILLE", _("Coquille d’aile")
    CLIPS = "CLIPS", _("Clips")
    VISSERIE = "VISSERIE", _("Visserie")
    CAPOT = "CAPOT", _("Capot")


class Carrosserie(Piece):
    # Relations véhicule
    cote = models.CharField(max_length=2, choices=Cote.choices, null=True, blank=True)
    emplacement = models.CharField(max_length=2, choices=Emplacement.choices, null=True, blank=True)
    libelle = models.CharField(max_length=30, choices=LibelleCarrosserie.choices)

    # Peinture et vernis
    code_peinture = models.CharField(max_length=50, blank=True)
    quantite_peinture_l = models.FloatField(default=0.0)
    vernis = models.CharField(max_length=50, blank=True)
    quantite_vernis_l = models.FloatField(default=0.0)

    # Main d'œuvre
    temps_h = models.FloatField(default=0.0, help_text="Temps de main d'oeuvre en heures")
    taux_horaire = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Pièce carrosserie"
        verbose_name_plural = "Pièces carrosserie"

    def total_main_oeuvre(self):
        """Calcule le coût main d'œuvre en euros"""
        return self.temps_h * float(self.taux_horaire)

    def __str__(self):
        return f"{self.get_libelle_display()} - {self.get_cote_display() or 'N/A'}"
