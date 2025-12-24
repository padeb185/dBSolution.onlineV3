from django.db import models
from django.utils.translation import gettext_lazy as _
from piece.models import Piece

class PiecePneus(Piece):
    TRAIN_CHOICES = [
        ("av", _("Train AV")),
        ("ar", _("Train AR")),
    ]

    TYPE_CHOICES = [
        ("slick", _("Slick")),
        ("semi_slick", _("Semi-slick")),
        ("pluie", _("Pluie")),
        ("neige", _("Neige")),
    ]

    MANUFACTURIER_CHOICES = [
        ("michelin", _("Michelin")),
        ("pirelli", _("Pirelli")),
    ]

    train = models.CharField(max_length=2, choices=TRAIN_CHOICES, verbose_name=_("Train"))
    valve = models.BooleanField(default=True, verbose_name=_("Valve"))
    savon = models.BooleanField(default=True, verbose_name=_("Savon"))
    manufacturier = models.CharField(max_length=50, choices=MANUFACTURIER_CHOICES, verbose_name=_("Manufacturier"))
    largeur = models.PositiveIntegerField(verbose_name=_("Largeur"))
    hauteur = models.PositiveIntegerField(verbose_name=_("Hauteur"))
    jante = models.PositiveIntegerField(help_text=_("Diamètre en pouces"), verbose_name=_("Jante"))
    type_pneu = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("Type de pneu"))
    indice_charge = models.CharField(max_length=10, verbose_name=_("Indice de charge"))
    indice_vitesse = models.CharField(max_length=10, verbose_name=_("Indice de vitesse"))
    quantite_montee = models.PositiveIntegerField(default=0, verbose_name=_("Quantité montée"))

    def total_pneus(self):
        """Total montés + stock"""
        return self.quantite_montee + self.quantite_stock

    @staticmethod
    def total_pneus_all(vehicule_id=None):
        """Total pneus montés pour un véhicule ou pour tous"""
        pneus = PiecePneus.objects.all()
        if vehicule_id:
            pneus = pneus.filter(vehicule_id=vehicule_id)
        total_montee = sum(p.quantite_montee for p in pneus)
        total_stock = sum(p.quantite_stock for p in pneus)
        return {"total_montee": total_montee, "total_stock": total_stock, "total": total_montee + total_stock}

    def alerte_stock(self, seuil=5):
        """Retourne True si stock trop bas"""
        return self.quantite_stock <= seuil

    class Meta:
        verbose_name = _("Pneu")
        verbose_name_plural = _("Pneus")

    def __str__(self):
        return _("%(type)s – %(largeur)s/%(hauteur)s R%(jante)s") % {
            "type": self.get_type_pneu_display(),
            "largeur": self.largeur,
            "hauteur": self.hauteur,
            "jante": self.jante
        }
