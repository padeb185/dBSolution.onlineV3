import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from client_particulier.models import ClientParticulier
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
        ClientParticulier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers_client",
        verbose_name=_("Client")
    )

    societe = models.ForeignKey(
        SocieteCliente,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paniers_societe",
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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("Identifiant")
    )

    panier = models.ForeignKey(
        Panier,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Panier")
    )

    piece = models.ForeignKey(
        Piece,
        on_delete=models.PROTECT,
        related_name="panier_items",
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

    marge = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Marge (%)")
    )

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

    class Meta:
        verbose_name = _("Ligne de panier")
        verbose_name_plural = _("Lignes de panier")
        unique_together = ("panier", "piece")

    def __str__(self):
        return _("%(piece)s × %(quantite)s") % {
            "piece": self.piece,
            "quantite": self.quantite,
        }

    def prix_vente_ht_calcule(self):
        return self.prix_achat_ht * (Decimal("1.0") + self.marge / Decimal("100"))

    def total_ht(self):
        return self.quantite * self.prix_unitaire_ht

    def total_tva(self):
        return self.total_ht() * (self.taux_tva_client / Decimal("100"))

    def total_ttc(self):
        return self.total_ht() + self.total_tva()
