from django.db import models

class Carrossier(models.Model):
    id = models.AutoField(primary_key=True)
    nom_societe = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    pays = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    numero_tva = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Carrossier"
        verbose_name_plural = "Carrossiers"

    def __str__(self):
        return self.nom_societe


class Intervention(models.Model):
    id = models.AutoField(primary_key=True)
    carrossier = models.ForeignKey(
        Carrossier,
        on_delete=models.CASCADE,
        related_name="interventions"
    )
    pare_chocs = models.BooleanField(default=False)
    bouclier = models.BooleanField(default=False)
    pare_brise = models.BooleanField(default=False)
    vitre_porte = models.BooleanField(default=False)
    lunette = models.BooleanField(default=False)
    retroviseur = models.BooleanField(default=False)
    aile = models.BooleanField(default=False)
    elargisseur_aile = models.BooleanField(default=False)
    bas_de_caisse = models.BooleanField(default=False)
    support_radiateur = models.BooleanField(default=False)
    support_pare_choc = models.BooleanField(default=False)
    porte = models.BooleanField(default=False)
    poignee_porte = models.BooleanField(default=False)
    coffre_haillon = models.BooleanField(default=False)
    joint_coffre = models.BooleanField(default=False)
    joint_porte = models.BooleanField(default=False)
    coquille_aile = models.BooleanField(default=False)
    clips = models.BooleanField(default=False)
    visserie = models.BooleanField(default=False)
    capot = models.BooleanField(default=False)

    montant_devis = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_facture = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Intervention"
        verbose_name_plural = "Interventions"

    def __str__(self):
        return f"Intervention {self.id} – {self.carrossier.nom_societe}"
