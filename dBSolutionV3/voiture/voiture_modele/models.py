import uuid

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django import forms
from django.db import models
from societe.models import Societe


class VoitureModele(models.Model):
    class NombrePortes(models.IntegerChoices):
        DEUX = 2, "2 portes"
        TROIS = 3, "3 portes"
        CINQ = 5, "5 portes"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations
    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.PROTECT,
        related_name="modeles"
    )
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)

    # Informations du modèle
    nom_modele = models.CharField(max_length=100)
    nom_variante = models.CharField(max_length=100, blank=True, null=True)
    nombre_portes = models.IntegerField(choices=NombrePortes.choices)

    nbre_places = models.PositiveSmallIntegerField()

    taille_reservoir = models.DecimalField(max_digits=5, decimal_places=2, help_text="En litres")

    capacite_batterie = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Capacité batterie en kWh"
    )

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
        super().clean()  # Appel recommandé
        marque = self.voiture_marque
        nom_modele = self.nom_modele
        nom_variante = self.nom_variante

        if marque and nom_modele:
            qs = VoitureModele.objects.filter(
                voiture_marque=marque,
                nom_modele__iexact=nom_modele,
            )

            # Vérifier la variante si elle est définie
            if nom_variante:
                qs = qs.filter(nom_variante__iexact=nom_variante) if nom_variante else qs.filter(
                    nom_variante__isnull=True)

            else:
                # Si aucune variante, ne considérer que les modèles sans variante
                qs = qs.filter(nom_variante__isnull=True)

            # Exclure l’instance actuelle si modification
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(
                    _("Ce modèle avec cette variante existe déjà pour cette marque.")
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # valide l’instance avant sauvegarde
        super().save(*args, **kwargs)