from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Fabricant(models.Model):
    nom = models.CharField(max_length=100, verbose_name=_("Nom"))
    pays = models.CharField(max_length=100, blank=True, verbose_name=_("Pays"))

    def __str__(self):
        return self.nom


class CodeBarre(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Code-barre"))

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
        related_name="pieces",
        verbose_name=_("Modèle")
    )

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pieces",
        verbose_name=_("Marque")
    )

    vehicule = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pieces",
        verbose_name=_("Véhicule")
    )

    # Fabricants & codes-barres
    fabricants = models.ManyToManyField(
        Fabricant,
        related_name="pieces",
        verbose_name=_("Fabricants")
    )

    codes_barres = models.ManyToManyField(
        CodeBarre,
        related_name="pieces",
        blank=True,
        verbose_name=_("Codes-barres")
    )

    # Informations générales
    immatriculation = models.CharField(max_length=20, blank=True, verbose_name=_("Immatriculation"))
    annee = models.PositiveSmallIntegerField(default=timezone.now().year, verbose_name=_("Année"))
    site = models.CharField(max_length=100, blank=True, verbose_name=_("Site"))
    pays = models.CharField(max_length=100, blank=True, verbose_name=_("Pays"))
    emplacement_etagere = models.CharField(
        max_length=4,
        blank=True,
        help_text=_("A-Z / 1-50"),
        verbose_name=_("Emplacement étagère")
    )
    qualite = models.CharField(max_length=50, blank=True, verbose_name=_("Qualité"))

    # Références
    oem = models.CharField(max_length=50, blank=True, verbose_name=_("Code OEM"))

    # Prix
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix d'achat"))
    majoration_pourcent = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_("Majoration (%)"))
    tva = models.DecimalField(max_digits=4, decimal_places=2, default=21.00, verbose_name=_("TVA (%)"))
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix de vente"))

    # Stock
    quantite_stock = models.PositiveIntegerField(default=0, verbose_name=_("Quantité en stock"))
    quantite_utilisee = models.PositiveIntegerField(default=0, verbose_name=_("Quantité utilisée"))
    quantite_min = models.PositiveIntegerField(default=0, verbose_name=_("Quantité minimale"))

    # Dates
    date_creation = models.DateTimeField(default=timezone.now, verbose_name=_("Date de création"))

    # Exemple de champ organe ou marque utilisé dans __str__
    organe = models.CharField(max_length=100, blank=True, verbose_name=_("Organe"))
    marque = models.CharField(max_length=100, blank=True, verbose_name=_("Marque"))

    class Meta:
        verbose_name = _("Pièce")
        verbose_name_plural = _("Pièces")

    def __str__(self):
        return _("%(organe)s - %(marque)s") % {
            "organe": self.organe or _("Pièce"),
            "marque": self.marque or _("Marque")
        }

    def calcul_prix_vente(self):
        """Calcul automatique du prix de vente"""
        return float(self.prix_achat) * (1 + float(self.majoration_pourcent) / 100)


class Inventaire(models.Model):
    piece = models.ForeignKey(
        "piece.Piece",
        on_delete=models.CASCADE,
        related_name="inventaires",
        verbose_name=_("Pièce")
    )

    variation = models.IntegerField(help_text=_("+ entrée / - sortie"), verbose_name=_("Variation"))
    stock_apres = models.PositiveIntegerField(default=0, verbose_name=_("Stock après"))
    commentaire = models.TextField(blank=True, verbose_name=_("Commentaire"))
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Inventaire")
        verbose_name_plural = _("Inventaires")

    def __str__(self):
        return _("%(piece)s : %(variation)d") % {
            "piece": self.piece,
            "variation": self.variation
        }

    def mise_a_jour_stock(self, variation):
        """Met à jour le stock de la pièce et crée un inventaire"""
        self.piece.quantite_stock += variation
        if variation < 0:
            self.piece.quantite_utilisee += abs(variation)
        self.piece.save()

        Inventaire.objects.create(
            piece=self.piece,
            variation=variation,
            stock_apres=self.piece.quantite_stock,
            date=timezone.now()
        )
