from django.db import models
import uuid
from django.utils import timezone


class Fabricant(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nom


class CodeBarre(models.Model):
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.code


class Piece(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations véhicule
    modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pieces"
    )

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pieces"
    )

    vehicule = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pieces"
    )

    # Fabricants & codes-barres
    fabricants = models.ManyToManyField(
        Fabricant,
        related_name="pieces"
    )

    codes_barres = models.ManyToManyField(
        CodeBarre,
        related_name="pieces",
        blank=True
    )

    # Informations générales
    immatriculation = models.CharField(max_length=20, blank=True)
    annee = models.PositiveSmallIntegerField(default=timezone.now().year)  # année par défaut
    site = models.CharField(max_length=100, blank=True)
    pays = models.CharField(max_length=100, blank=True)
    emplacement_etagere = models.CharField(
        max_length=4,
        blank=True,
        help_text="A-Z / 1-50"
    )
    qualite = models.CharField(max_length=50, blank=True)

    # Références
    oem = models.CharField(max_length=50, blank=True, verbose_name="Code OEM")

    # Prix
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    majoration_pourcent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tva = models.DecimalField(max_digits=4, decimal_places=2, default=21.00)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Stock
    quantite_stock = models.PositiveIntegerField(default=0)
    quantite_utilisee = models.PositiveIntegerField(default=0)
    quantite_min = models.PositiveIntegerField(default=0)

    # Dates
    date_creation = models.DateTimeField(default=timezone.now)

    # Exemple de champ organe ou marque utilisé dans __str__
    organe = models.CharField(max_length=100, blank=True)
    marque = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = False

    def __str__(self):
        return f"{self.organe or 'Pièce'} - {self.marque or 'Marque'}"

    def calcul_prix_vente(self):
        """Calcul automatique du prix de vente"""
        return float(self.prix_achat) * (1 + float(self.majoration_pourcent) / 100)


class Inventaire(models.Model):
    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.CASCADE,
        related_name="inventaires"
    )

    variation = models.IntegerField(help_text="+ entrée / - sortie")
    stock_apres = models.PositiveIntegerField(default=0)
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.piece} : {self.variation}"

    def mise_a_jour_stock(self, variation):
        """Met à jour le stock de la pièce et crée un inventaire"""
        self.piece.quantite_stock += variation
        # Si sortie (variation négative), incrémente quantité utilisée
        if variation < 0:
            self.piece.quantite_utilisee += abs(variation)
        self.piece.save()

        # Enregistrement de la variation dans l'inventaire
        Inventaire.objects.create(
            piece=self.piece,
            variation=variation,
            stock_apres=self.piece.quantite_stock,
            date=timezone.now()
        )
