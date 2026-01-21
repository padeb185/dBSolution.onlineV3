from django.db import models
from django.db.models import Q
import uuid
from django.utils.translation import gettext_lazy as _
from voiture.voiture_boite.models import VoitureBoite




class TypeMoteur(models.TextChoices):
    TURBO = "TURBO", _("Turbo")
    ATMOSPHERIQUE = "ATM", _("Atmosphérique")
    WANKEL = "WANKEL", _("Wankel")
    HYBRIDE_ESSENCE = "HYB_E", _("Hybride essence")
    HYBRIDE_TURBO_ESSENCE = "HYB_TE", _("Hybride turbo essence")
    ELECTRIQUE = "ELEC", _("Machine électrique")

class TypeCarburant(models.TextChoices):
    ESSENCE = "ESS", _("Essence")
    DIESEL = "DSL", _("Diesel")
    ELECTRICITE = "ELEC", _("Électricité")
    CNG = "CNG", _("Gaz naturel (CNG)")
    LPG = "LPG", _("GPL")
    HYDROGENE = "H2", _("Hydrogène")

class TypeDistribution(models.TextChoices):
    CHAINE = "CHAINE", _("Chaîne")
    COURROIE = "COURROIE", _("Courroie")

class MoteurVoiture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations multiples
    voitures_modeles = models.ManyToManyField(
        "voiture_modele.VoitureModele",
        related_name="moteurs",
        blank=True
    )

    voitures_exemplaires = models.ManyToManyField(
        "voiture_exemplaire.VoitureExemplaire",
        related_name="moteurs",
        blank=True
    )

    # Spécifications moteur
    motoriste = models.CharField(max_length=40)
    code_moteur = models.CharField(max_length=50)
    type_moteur = models.CharField(max_length=40, choices=TypeMoteur.choices)
    carburant = models.CharField(max_length=40, choices=TypeCarburant.choices)
    cylindree_l = models.FloatField(verbose_name="Cylindrée (L)")
    distribution = models.CharField(max_length=40, choices=TypeDistribution.choices)
    nombre_cylindres = models.IntegerField(
        default=1,
        verbose_name="Nombre de cylindres",
        null=True,
        blank=True)
    puissance_ch = models.IntegerField(null=True, blank=True)
    puissance_tr_min = models.IntegerField(verbose_name="Puissance à (tr/min)", null=True, blank=True)
    couple_nm = models.IntegerField(null=True, blank=True)
    couple_tr_min = models.PositiveIntegerField(verbose_name="Couple à (tr/min)", null=True, blank=True)
    qualite_huile = models.CharField(max_length=50, null=True, blank=True)
    quantite_huile_l = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    kilometrage_moteur = models.PositiveIntegerField(default=0, null=True, blank=True)
    numero_moteur = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    intervalle_km_entretien = models.PositiveIntegerField(default=15000, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    boite = models.ForeignKey(VoitureBoite, null=True, blank=True, on_delete=models.SET_NULL, related_name="moteurs")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(numero_moteur__gte=1) & Q(numero_moteur__lte=10),
                name="numero_moteur_1_10"
            ),
        ]

    def __str__(self):
        return f"Moteur {self.cylindree_l}L - {self.type_moteur}"

    def prochain_entretien_km(self):
        return self.kilometrage_moteur + self.intervalle_km_entretien

    def remplacer_moteur(self):
        if self.numero_moteur < 10:
            self.numero_moteur += 1
            self.kilometrage_moteur = 0
            self.save()

    def save(self, *args, **kwargs):
        """
        Remplissage automatique des champs si un moteur avec le même
        code_moteur et motoriste existe déjà.
        """
        # On ne copie que si on crée un nouveau moteur
        if not self.pk and self.code_moteur and self.motoriste:
            moteur_existant = MoteurVoiture.objects.filter(
                code_moteur=self.code_moteur,
                motoriste=self.motoriste
            ).first()

            if moteur_existant:
                champs_a_copier = [
                    "type_moteur", "carburant", "cylindree_l",
                    "distribution", "nombre_cylindres", "puissance_ch",
                    "puissance_tr_min", "couple_nm", "couple_tr_min",
                    "qualite_huile", "quantite_huile_l", "intervalle_km_entretien",
                ]

                for champ in champs_a_copier:
                    setattr(self, champ, getattr(moteur_existant, champ))

        super().save(*args, **kwargs)
