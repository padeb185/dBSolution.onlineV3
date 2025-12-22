from django.db import models
import uuid




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
        blank=True
    )

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    vehicule = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )



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
    annee = models.PositiveSmallIntegerField()
    site = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    emplacement_etagere = models.CharField(
        max_length=4,
        help_text="A-Z / 1-50"
    )

    qualite = models.CharField(max_length=50)

    # Références
    oem = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Code OEM"
    )

    # Prix
    prix_achat = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    majoration_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    tva = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=21.00
    )

    prix_vente = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Stock
    quantite_stock = models.PositiveIntegerField(default=0)
    quantite_utilisee = models.PositiveIntegerField(default=0)
    quantite_min = models.PositiveIntegerField(default=0)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organe} - {self.marque}"



class Inventaire(models.Model):
    piece = models.ForeignKey(
        Piece,
        on_delete=models.CASCADE,
        related_name="inventaires"
    )

    variation = models.IntegerField(
        help_text="+ entrée / - sortie"
    )

    stock_apres = models.PositiveIntegerField()

    commentaire = models.TextField(blank=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.piece} : {self.variation}"

    def mise_a_jour_stock(self, variation):
        self.quantite_stock += variation
        self.save()

        Inventaire.objects.create(
            piece=self,
            variation=variation,
            stock_apres=self.quantite_stock
        )


    def calcul_prix_vente(self):
        return self.prix_achat * (1 + self.majoration_pourcent / 100)
