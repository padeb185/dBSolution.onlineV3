import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from client.models import Client
from societe_cliente.models import SocieteCliente
from piece.models import Piece


class Panier(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Identifiant")
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers",
        verbose_name=_("Client")
    )

    societe = models.ForeignKey(
        SocieteCliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers",
        verbose_name=_("Société cliente")
    )

    date_creation = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Date de création")
    )

    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de modification")
    )

    valide = models.BooleanField(
        default=False,
        verbose_name=_("Validé")
    )  # devient True lors de la facturation

    def total_ht(self):
        return sum(item.total_ht() for item in self.items.all())

    def __str__(self):
        return _("Panier %(id)s") % {"id": self.id}

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Paniers")


class PanierItem(models.Model):
    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Panier")
    )

    piece = models.ForeignKey(
        Piece,
        on_delete=models.PROTECT,
        verbose_name=_("Pièce")
    )

    quantite = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantité")
    )

    prix_achat_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix d'achat HT")
    )

    taux_tva_fournisseur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("TVA fournisseur (%)")
    )

    # 📈 MARGE
    marge = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Marge (%)")
    )

    # 💵 VENTE
    prix_unitaire_ht = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Prix unitaire HT (vente)")
    )

    taux_tva_client = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("TVA client (%)")
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
        return _("%(piece)s × %(quantite)s") % {
            "piece": self.piece,
            "quantite": self.quantite,
        }

    class Meta:
        verbose_name = _("Ligne de panier")
        verbose_name_plural = _("Lignes de panier")
        unique_together = ("panier", "piece")
