import uuid
from django.core.exceptions import ValidationError

from django.db import models
from societe.models import Societe

class VoitureModele(models.Model):
    class NombrePortes(models.IntegerChoices):
        DEUX = 2, "2 portes"
        TROIS = 3, "3 portes"
        CINQ = 5, "5 portes"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="modeles"
    )
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    nom_modele = models.CharField(max_length=100)
    nom_variante = models.CharField(max_length=100, blank=True, null=True)
    nombre_portes = models.IntegerField(choices=NombrePortes.choices)
    nbre_places = models.PositiveSmallIntegerField()
    taille_reservoir = models.DecimalField(max_digits=5, decimal_places=2, help_text="En litres")
    capacite_batterie = models.PositiveIntegerField(null=True, blank=True, help_text="Capacité batterie en kWh")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["voiture_marque", "nom_modele", "nom_variante"],
                name="unique_modele_variante_par_marque"
            )
        ]

    def __str__(self):
        return f"{self.voiture_marque} {self.nom_modele} {self.nom_variante or ''}".strip()

    def clean(self):
        super().clean()
        if self.voiture_marque and self.nom_modele:
            qs = VoitureModele.objects.filter(
                voiture_marque=self.voiture_marque,
                nom_modele__iexact=self.nom_modele,
            )
            if self.nom_variante:
                qs = qs.filter(nom_variante__iexact=self.nom_variante)
            else:
                qs = qs.filter(nom_variante__isnull=True)

            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(_("Ce modèle avec cette variante existe déjà pour cette marque."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Valide l’instance avant sauvegarde
        super().save(*args, **kwargs)