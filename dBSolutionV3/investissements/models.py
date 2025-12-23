from django.db import models
from fournisseur.models import Fournisseur  # si tu as un modèle Fournisseur


class Investissement(models.Model):
    id_investissement = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="investissements")

    # Libellé de l'investissement (ex: pont, machine à pneus, etc.)
    LIBELLE_CHOICES = [
        ('PONT', 'Pont'),
        ('MACHINE_GEOMETRIE', 'Machine de géométrie'),
        ('MACHINE_PNEUS', 'Machine à pneus'),
        ('EQUILIBREUSE', 'Équilibreuse'),
        ('COMPRESSEUR', 'Compresseur'),
        ('BOOSTER_BATTERIE', 'Booster batterie'),
        ('BOOSTER_PNEUS', 'Booster pneus'),
        ('TUYAUX_AIR', 'Tuyaux pression d’air'),
        ('CONNECTEURS', 'Connecteurs'),
        ('MOBILIER', 'Mobilier'),
        ('ORDINATEUR', 'Ordinateur'),
        ('APPAREIL_DIAGNOSTIC', 'Appareil de diagnostic'),
    ]
    libelle = models.CharField(max_length=50, choices=LIBELLE_CHOICES)

    # Détails de l'investissement
    details = models.TextField(blank=True, null=True)
    temps_amortissement = models.PositiveIntegerField(help_text="Durée d'amortissement en mois ou années")

    # Type d'amortissement : linéaire, dégressif, etc.
    TYPE_AMORTISSEMENT_CHOICES = [
        ('LINEAIRE', 'Linéaire'),
        ('DEGRESSIF', 'Dégressif'),
        ('AUTRE', 'Autre'),
    ]
    type_amortissement = models.CharField(max_length=20, choices=TYPE_AMORTISSEMENT_CHOICES, default='LINEAIRE')

    class Meta:
        verbose_name = "Investissement"
        verbose_name_plural = "Investissements"

    def __str__(self):
        return f"{self.get_libelle_display()} - Fournisseur: {self.fournisseur}"
