from django.db import models
from piece.models import Piece

class Cote(models.TextChoices):
    GAUCHE = "GA", "Gauche"
    DROIT = "DR", "Droit"

class Emplacement(models.TextChoices):
    AVANT = "AV", "Avant"
    ARRIERE = "AR", "Arrière"

class LibelleCarrosserie(models.TextChoices):
    PARE_CHOCS = "PARE_CHOCS", "Pare-chocs"
    BOUCLIER = "BOUCLIER", "Bouclier"
    PARE_BRIS = "PARE_BRIS", "Pare-brise"
    VITRE_PORTE = "VITRE_PORTE", "Vitres Porte"
    LUNETTE = "LUNETTE", "Lunette"
    RETROVISEUR = "RETROVISEUR", "Rétroviseur"
    AILE = "AILE", "Aile"
    ELARGISSEUR_AILE = "ELARG_AILE", "Élargisseur d’aile"
    BAS_DE_CAISSE = "BAS_CAISSE", "Bas de caisse"
    SUPPORT_RADIATEUR = "SUPP_RAD", "Support de radiateurs"
    SUPPORT_PARE_CHOC = "SUPP_PC", "Support pare choc"
    PORTE = "PORTE", "Porte"
    POIGNEE_PORTE = "POIGNEE", "Poignée de porte"
    COFFRE_HAILLON = "COFFRE", "Coffre haillon"
    JOINT_COFFRE = "JOINT_COFFRE", "Joint de coffre"
    JOINT_PORTE = "JOINT_PORTE", "Joint porte"
    COQUILLE_AILE = "COQUILLE", "Coquille d’aile"
    CLIPS = "CLIPS", "Clips"
    VISSERIE = "VISSERIE", "Visserie"


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
