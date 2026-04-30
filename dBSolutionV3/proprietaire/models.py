from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from client_particulier.models import validate_iban
from django.http import JsonResponse
from django.db.models import Sum



class Proprietaire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)


    adresse = models.ForeignKey(
        "adresse.Adresse",
        on_delete=models.CASCADE,
        related_name="proprietaires",
        null=True,
        blank=True,
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires"
    )

    numero_telephone = models.CharField(
        _("Numéro de téléphone"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_permis = models.CharField(
        _("Numéro de permis de conduire"),
        max_length=50,
        null=True,
        blank=True
    )

    numero_carte_id = models.CharField(
        _("Numéro de carte d'identité"),
        max_length=20,
        null=True,
        blank=True
    )

    numero_compte = models.CharField(
        _("Numéro de compte bancaire"),
        max_length=34,
        null=True,
        blank=True,
        validators=[validate_iban]
    )
    numero_carte_bancaire = models.CharField(
        _("Numéro de carte bancaire"),
        max_length=20,
        null=True,
        blank=True
    )

    email = models.EmailField(
        _("Email"),
        max_length=100,
        null=True,
        blank=True
    )

    date_naissance = models.DateField(
        _("Date de naissance"),
        null=True,
        blank=True
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"





class ProprietaireVoiture(models.Model):
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture"
    )

    proprietaire = models.ForeignKey(
        "proprietaire.Proprietaire",
        on_delete=models.CASCADE,
        related_name="proprietaire_voitures"
    )

    part_proprietaire_pourcent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="proprietaires_voiture",
        null=True,
        blank=True,
    )

    remarques = models.TextField(
        verbose_name=_("Remarques"),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)

    def clean(self):
        total = (
                self.__class__.objects
                .filter(voiture_exemplaire=self.voiture_exemplaire)
                .exclude(pk=self.pk)
                .aggregate(total=Sum("part_proprietaire_pourcent"))
                ["total"] or 0
        )

        if total + self.part_proprietaire_pourcent > 100:
            raise ValidationError("Total des parts > 100% interdit.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



