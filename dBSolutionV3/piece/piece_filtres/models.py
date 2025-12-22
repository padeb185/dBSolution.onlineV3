import uuid
from django.db import models

class Fabricant(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom


class CodeBarre(models.Model):
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.code

class TypeFluide(models.TextChoices):
    HUILE_MOTEUR = "HUILE_MOTEUR", "Huile moteur"
    HUILE_BOITE = "HUILE_BOITE", "Huile de boîte"
    HUILE_PONT = "HUILE_PONT", "Huile de pont"
    LIQUIDE_REFROIDISSEMENT = "LR", "Liquide de refroidissement"
    LAVE_GLACE = "LAVE_GLACE", "Lave-glace"
    LIQUIDE_FREIN = "LIQ_FREIN", "Liquide de frein"
    HUILE_DIRECTION = "HUILE_DIR", "Huile de direction"


class Fluide(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations véhicule
    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fluides"
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fluides"
    )

    # Fabricants & codes
    fabricants = models.ManyToManyField(
        Fabricant,
        related_name="fluides"
    )

    codes_barres = models.ManyToManyField(
        CodeBarre,
        related_name="fluides",
        blank=True
    )

    # Références
    oem = models.CharField(
        max_length=50,
        blank=True
    )

    # Identification
    type_fluide = models.CharField(
        max_length=30,
        choices=TypeFluide.choices
    )

    nom_fluide = models.CharField(
        max_length=100
    )

    # Stock (en litres)
    quantite_stock = models.FloatField(default=0.0)
    quantite_utilisee = models.FloatField(default=0.0)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(voiture_modele__isnull=False) |
                    models.Q(voiture_exemplaire__isnull=False)
                ),
                name="fluide_lie_a_voiture"
            )
        ]

    def __str__(self):
        return f"{self.nom_fluide} ({self.type_fluide})"


class StockFluide(models.Model):
    fluide = models.ForeignKey(
        Fluide,
        on_delete=models.CASCADE,
        related_name="variations_stock"
    )

    variation = models.FloatField(
        help_text="+ entrée / - sortie (en litres)"
    )

    stock_apres = models.FloatField()

    commentaire = models.TextField(blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fluide} : {self.variation} L"


    def mise_a_jour_stock(self, variation):
        self.quantite_stock += variation

        if variation < 0:
            self.quantite_utilisee += abs(variation)

        self.save()

        StockFluide.objects.create(
            fluide=self,
            variation=variation,
            stock_apres=self.quantite_stock
        )

