import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from client.models import Client
from societe_cliente.models import SocieteCliente
from django.db import models
from piece.models import Piece



class Panier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers"
    )
    societe = models.ForeignKey(
        SocieteCliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers"
    )

    date_creation = models.DateTimeField(default=timezone.now)
    date_modification = models.DateTimeField(auto_now=True)

    valide = models.BooleanField(default=False)  # devient True lors de la facturation

    def total_ht(self):
        return sum(item.total_ht() for item in self.items.all())

    def __str__(self):
        return f"Panier {self.id}"





class PanierItem(models.Model):
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name="items"
    )

    piece = models.ForeignKey(
        Piece,
        on_delete=models.PROTECT
    )

    quantite = models.PositiveIntegerField(default=1)

    prix_achat_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix d'achat HT"
    )

    taux_tva_fournisseur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="TVA fournisseur (%)"
    )

    # 📈 MARGE
    marge = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Marge (%)"
    )

    # 💵 VENTE
    prix_unitaire_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire HT (vente)"
    )

    taux_tva_client = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="TVA client (%)"
    )


    def prix_vente_ht_calcule(self):
        """
        Prix de vente HT basé sur prix achat + marge
        """
        return self.prix_achat_ht * (Decimal("1.0") + self.marge / Decimal("100"))

    def total_ht(self):
        return self.quantite * self.prix_unitaire_ht

    def total_tva(self):
        return self.total_ht() * (self.taux_tva_client / Decimal("100"))

    def total_ttc(self):
        return self.total_ht() + self.total_tva()

    def __str__(self):
        return f"{self.piece} x {self.quantite}"

    class Meta:
        unique_together = ("panier", "piece")



