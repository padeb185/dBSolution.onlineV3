import uuid
from django.db import models

class Fournisseur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom du fournisseur")
    adresse = models.ForeignKey(
        'adresse.Adresse',
        on_delete=models.PROTECT,
        related_name='fournisseurs'
    )
    pays = models.CharField(max_length=100, verbose_name="Pays")
    numero_tva = models.CharField(max_length=20, unique=True, verbose_name="Numéro de TVA")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, verbose_name="Taux de TVA (%)")

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @property
    def total_htva(self):
        """Somme de tous les montants HTVA des factures liées"""
        return sum(f.montant_htva for f in self.factures.all())

    @property
    def total_tva(self):
        """Somme de toutes les TVA des factures liées"""
        return sum(f.tva_a_payer for f in self.factures.all())

    @property
    def total_ttc(self):
        """Somme totale TTC des factures"""
        return self.total_htva + self.total_tva


class Facture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.CASCADE,
        related_name='factures'
    )
    reference = models.CharField(max_length=100, verbose_name="Référence facture")
    montant_htva = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant HTVA")
    date_facture = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date_facture']

    def __str__(self):
        return f"{self.reference} - {self.fournisseur.nom}"

    @property
    def tva_a_payer(self):
        """Calcule la TVA de cette facture en fonction du taux du fournisseur"""
        return self.montant_htva * (self.fournisseur.taux_tva / 100)

    @property
    def total_ttc(self):
        """Montant TTC de cette facture"""
        return self.montant_htva + self.tva_a_payer
