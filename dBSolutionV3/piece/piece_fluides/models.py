from django.utils import timezone
from django.db import models
from piece.models import Piece


class TypeFluide(models.TextChoices):
    HUILE_MOTEUR = "HUILE_MOTEUR", "Huile moteur"
    HUILE_BOITE = "HUILE_BOITE", "Huile de boîte"
    HUILE_PONT = "HUILE_PONT", "Huile de pont"
    LIQUIDE_REFROIDISSEMENT = "LDR", "Liquide de refroidissement"
    LAVE_GLACE = "LAVE_GLACE", "Lave-glace"
    LIQUIDE_FREIN = "LIQ_FREIN", "Liquide de frein"
    HUILE_DIRECTION = "HUILE_DIR", "Huile de direction"


class Fluide(Piece):
    type_fluide = models.CharField(max_length=30, choices=TypeFluide.choices)
    nom_fluide = models.CharField(max_length=100)
    qualite_fluide = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Fluide"
        verbose_name_plural = "Fluides"

    def __str__(self):
        return f"{self.nom_fluide} ({self.get_type_fluide_display()})"


class InventaireFluide(models.Model):
    fluide = models.ForeignKey(
        Fluide,
        on_delete=models.CASCADE,
        related_name="inventaires_fluide"
    )
    variation = models.FloatField(help_text="+ entrée / - sortie (litres)")
    stock_apres = models.FloatField(default=0.0)
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Met à jour le stock du fluide
        self.fluide.quantite_stock += self.variation
        if self.variation < 0:
            self.fluide.quantite_utilisee += abs(self.variation)
        self.stock_apres = self.fluide.quantite_stock
        self.fluide.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fluide} : {self.variation} L"




class InventaireFluide(models.Model):
    fluide = models.ForeignKey(
        Fluide,
        on_delete=models.CASCADE,
        related_name="inventaires_fluides"
    )

    variation = models.FloatField(
        help_text="+ entrée / - sortie (litres)"
    )

    stock_apres = models.FloatField(default=0.0)
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.fluide.quantite_stock += self.variation
        if self.variation < 0:
            self.fluide.quantite_utilisee += abs(self.variation)

        self.stock_apres = self.fluide.quantite_stock
        self.fluide.save()
        super().save(*args, **kwargs)
