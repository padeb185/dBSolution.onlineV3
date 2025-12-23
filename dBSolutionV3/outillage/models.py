from django.db import models
from fournisseur.models import Fournisseur

class Outillage(models.Model):
    id_outillage = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name="outillages")
    libelle = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)
    prix_htva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix HTVA")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00, verbose_name="Taux TVA (%)")
    montant_calcule = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    tva_a_recuperer = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    class Meta:
        verbose_name = "Outillage"
        verbose_name_plural = "Outillages"

    def save(self, *args, **kwargs):
        # Calcul automatique du montant total et de la TVA à récupérer
        self.montant_calcule = self.prix_htva * self.quantite
        self.tva_a_recuperer = self.montant_calcule * (self.taux_tva / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.libelle} ({self.reference}) - {self.quantite} pcs"
