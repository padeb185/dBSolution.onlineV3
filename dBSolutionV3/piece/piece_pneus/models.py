
from django.db import models
from piece.models import Piece


class PiecePneus(Piece):
    TRAIN_CHOICES = [
        ("av", "Train AV"),
        ("ar", "Train AR"),
    ]

    TYPE_CHOICES = [
        ("slick", "Slick"),
        ("semi_slick", "Semi-slick"),
        ("pluie", "Pluie"),
        ("neige", "Neige"),
    ]

    MANUFACTURIER_CHOICES = [
        ("michelin", "Michelin"),
        ("pirelli", "Pirelli"),
    ]

    train = models.CharField(max_length=2, choices=TRAIN_CHOICES)
    valve = models.BooleanField(default=True)
    savon = models.BooleanField(default=True)
    manufacturier = models.CharField(max_length=50, choices=MANUFACTURIER_CHOICES)
    largeur = models.PositiveIntegerField()
    hauteur = models.PositiveIntegerField()
    jante = models.PositiveIntegerField(help_text="Diamètre en pouces")
    type_pneu = models.CharField(max_length=20, choices=TYPE_CHOICES)
    indice_charge = models.CharField(max_length=10)
    indice_vitesse = models.CharField(max_length=10)
    quantite_montee = models.PositiveIntegerField(default=0)


    def total_pneus(self):
        return self.quantite_montee + self.quantite_stock

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
