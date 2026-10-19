from decimal import Decimal

from django.conf import settings
from django.db import models
import uuid
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CategoriePiece(models.TextChoices):
    """Familles de pièces (catalogue unique, une catégorie par type de maintenance)."""
    MOTEUR = "MOTEUR", _("Moteur")
    DISTRIBUTION = "DISTRIBUTION", _("Distribution")
    FILTRES = "FILTRES", _("Filtres")
    FLUIDES = "FLUIDES", _("Fluides (huiles, liquides)")
    ALLUMAGE = "ALLUMAGE", _("Allumage / bougies")
    INJECTION = "INJECTION", _("Injection / admission")
    TURBO = "TURBO", _("Turbo")
    REFROIDISSEMENT = "REFROIDISSEMENT", _("Refroidissement")
    ECHAPPEMENT = "ECHAPPEMENT", _("Échappement")
    EMBRAYAGE = "EMBRAYAGE", _("Embrayage")
    BOITE = "BOITE", _("Boîte de vitesses")
    TRANSMISSION = "TRANSMISSION", _("Transmission / cardans")
    FREINS = "FREINS", _("Freins")
    PNEUS = "PNEUS", _("Pneus")
    JANTES = "JANTES", _("Jantes / roues")
    SUSPENSION = "SUSPENSION", _("Suspension")
    TRAIN_AV = "TRAIN_AV", _("Train avant / direction")
    TRAIN_AR = "TRAIN_AR", _("Train arrière")
    ROULEMENTS = "ROULEMENTS", _("Roulements")
    SILENT_BLOC = "SILENT_BLOC", _("Silent blocs")
    ELECTRICITE = "ELECTRICITE", _("Électricité / batterie / démarreur")
    ELECTRONIQUE = "ELECTRONIQUE", _("Électronique / capteurs")
    ECLAIRAGE = "ECLAIRAGE", _("Éclairage / ampoules")
    ESSUYAGE = "ESSUYAGE", _("Essuyage")
    CLIMATISATION = "CLIMATISATION", _("Climatisation")
    CARROSSERIE = "CARROSSERIE", _("Carrosserie")
    HABITACLE = "HABITACLE", _("Habitacle")
    ESTHETIQUE = "ESTHETIQUE", _("Esthétique / produits d'entretien")
    AUTRE = "AUTRE", _("Autre")


class UnitePiece(models.TextChoices):
    PIECE = "PIECE", _("Pièce(s)")
    LITRE = "LITRE", _("Litre(s)")
    KG = "KG", _("Kilo(s)")
    METRE = "METRE", _("Mètre(s)")
    KIT = "KIT", _("Kit(s)")


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

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="pieces",
        null=True,
        blank=True,
    )

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
        blank=True,
        verbose_name=_("Fabricants")
    )

    # Catalogue / stock
    designation = models.CharField(max_length=150, blank=True, verbose_name=_("Désignation"))
    categorie = models.CharField(max_length=20, choices=CategoriePiece.choices, default=CategoriePiece.AUTRE,
                                 verbose_name=_("Catégorie"))
    fabricant = models.ForeignKey(Fabricant, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="pieces_principales", verbose_name=_("Fabricant"))
    reference_fabricant = models.CharField(max_length=60, blank=True, verbose_name=_("Référence fabricant"))
    unite = models.CharField(max_length=10, choices=UnitePiece.choices, default=UnitePiece.PIECE,
                             verbose_name=_("Unité"))
    actif = models.BooleanField(default=True, verbose_name=_("Active"))

    codes_barres = models.ManyToManyField(
        CodeBarre,
        related_name="pieces",
        blank=True,
        verbose_name=_("Codes-barres")
    )

    # Informations générales
    immatriculation = models.CharField(max_length=20, blank=True, verbose_name=_("Immatriculation"))
    annee = models.PositiveSmallIntegerField(default=timezone.now().year, verbose_name=_("Année"))
    site = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Site"))
    pays = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Pays"))
    emplacement_etagere = models.CharField(
        max_length=4,
        blank=True,
        help_text=_("A-Z / 1-4 / 1-50"),
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
    # Décimales : fluides au litre. Le stock peut devenir négatif (pièce utilisée avant son entrée en stock).
    quantite_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Quantité en stock"))
    quantite_utilisee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Quantité utilisée"))
    quantite_min = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Quantité minimale"))

    # Dates
    date_creation = models.DateTimeField(default=timezone.now, verbose_name=_("Date de création"))

    # Exemple de champ organe ou marque utilisé dans __str__
    organe = models.CharField(max_length=100, blank=True, verbose_name=_("Organe"))
    marque = models.CharField(max_length=100, blank=True, verbose_name=_("Marque"))

    class Meta:
        verbose_name = _("Pièce")
        verbose_name_plural = _("Pièces")
        ordering = ["categorie", "designation", "oem"]
        constraints = [
            # Un code OEM = une seule pièce par société
            models.UniqueConstraint(
                fields=["societe", "oem"],
                condition=~models.Q(oem=""),
                name="piece_oem_unique_par_societe",
            ),
        ]

    def __str__(self):
        nom = self.designation or self.organe or _("Pièce")
        return f"{nom} – {self.oem}" if self.oem else str(nom)

    @property
    def nom_fabricant(self):
        if self.fabricant_id:
            return self.fabricant.nom
        f = self.fabricants.first()
        return f.nom if f else (self.marque or "")

    @property
    def eans(self):
        return [c.code for c in self.codes_barres.all()]

    @property
    def en_alerte(self):
        return self.quantite_min and self.quantite_stock <= self.quantite_min

    @property
    def valeur_stock(self):
        return (Decimal(self.quantite_stock or 0) * Decimal(self.prix_achat or 0)).quantize(Decimal("0.01"))

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



# ======================================================================
# STOCK : mouvements, pièces utilisées par maintenance, inventaires
# ======================================================================
class MouvementStock(models.Model):
    """Variation de stock (entrée, sortie, inventaire, correction). quantite > 0 entrée, < 0 sortie."""

    class Type(models.TextChoices):
        ENTREE = "ENTREE", _("Entrée (achat / réception)")
        SORTIE = "SORTIE", _("Sortie (utilisation / facture)")
        INVENTAIRE = "INVENTAIRE", _("Régularisation d'inventaire")
        CORRECTION = "CORRECTION", _("Correction manuelle")
        RETOUR = "RETOUR", _("Retour fournisseur / annulation")

    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="mouvements_stock")
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="mouvements", verbose_name=_("Pièce"))
    type_mouvement = models.CharField(max_length=12, choices=Type.choices, verbose_name=_("Type"))
    quantite = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Quantité (+/-)"))
    stock_avant = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Stock avant"))
    stock_apres = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Stock après"))
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                        verbose_name=_("Prix unitaire HTVA"))
    maintenance = models.ForeignKey("maintenance.Maintenance", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="mouvements_stock", verbose_name=_("Maintenance"))
    facture = models.ForeignKey("facture.Facture", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="mouvements_stock", verbose_name=_("Facture"))
    commentaire = models.CharField(max_length=255, blank=True, verbose_name=_("Commentaire"))
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="mouvements_stock", verbose_name=_("Utilisateur"))
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Date"))

    class Meta:
        verbose_name = _("Mouvement de stock")
        verbose_name_plural = _("Mouvements de stock")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.piece} : {self.quantite:+}"


class PieceUtilisee(models.Model):
    """
    Pièce ou fluide utilisé dans une maintenance.
    Le stock est débité à l'émission de la facture de la maintenance (ou manuellement).
    """
    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="pieces_utilisees")
    maintenance = models.ForeignKey("maintenance.Maintenance", on_delete=models.CASCADE,
                                    related_name="pieces_utilisees", verbose_name=_("Maintenance"))
    piece = models.ForeignKey(Piece, on_delete=models.PROTECT, related_name="utilisations", verbose_name=_("Pièce"))
    # Ligne de pièce de l'intervention (ex. « capteur_lacet ») quand saisie depuis le formulaire de maintenance
    prefixe = models.CharField(max_length=80, blank=True, default="", verbose_name=_("Ligne de l'intervention"))
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name=_("Quantité"))
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("Prix unitaire HTVA"))
    mouvement = models.OneToOneField(MouvementStock, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="piece_utilisee", verbose_name=_("Sortie de stock"))
    facture = models.ForeignKey("facture.Facture", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="pieces_utilisees", verbose_name=_("Facture"))
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="pieces_utilisees")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Pièce utilisée")
        verbose_name_plural = _("Pièces utilisées")
        ordering = ["created_at"]

    @property
    def debitee(self):
        return self.mouvement_id is not None

    @property
    def total(self):
        return (Decimal(self.quantite or 0) * Decimal(self.prix_unitaire or 0)).quantize(Decimal("0.01"))


class InventaireStock(models.Model):
    """Inventaire physique : comptage des pièces, puis régularisation des écarts à la clôture."""

    class Statut(models.TextChoices):
        EN_COURS = "EN_COURS", _("En cours")
        CLOTURE = "CLOTURE", _("Clôturé")

    societe = models.ForeignKey("societe.Societe", on_delete=models.CASCADE, null=True, blank=True,
                                related_name="inventaires_stock")
    date = models.DateField(default=timezone.localdate, verbose_name=_("Date"))
    categorie = models.CharField(max_length=20, choices=CategoriePiece.choices, blank=True,
                                 verbose_name=_("Catégorie (vide = toutes)"))
    statut = models.CharField(max_length=10, choices=Statut.choices, default=Statut.EN_COURS, verbose_name=_("Statut"))
    commentaire = models.CharField(max_length=255, blank=True, verbose_name=_("Commentaire"))
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="inventaires_stock")
    cloture_le = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Inventaire de stock")
        verbose_name_plural = _("Inventaires de stock")
        ordering = ["-date", "-id"]


class LigneInventaire(models.Model):
    inventaire = models.ForeignKey(InventaireStock, on_delete=models.CASCADE, related_name="lignes")
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="lignes_inventaire")
    stock_theorique = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantite_comptee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = [("inventaire", "piece")]

    @property
    def ecart(self):
        if self.quantite_comptee is None:
            return None
        return self.quantite_comptee - self.stock_theorique
