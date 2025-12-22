from django.db import models
import uuid

class TypeMoteur(models.TextChoices):
    TURBO = "TURBO", "Turbo"
    ATMOSPHERIQUE = "ATM", "Atmosphérique"
    WANKEL = "WANKEL", "Wankel"
    HYBRIDE_ESSENCE = "HYB_E", "Hybride essence"
    HYBRIDE_TURBO_ESSENCE = "HYB_TE", "Hybride turbo essence"
    ELECTRIQUE = "ELEC", "Machine électrique"


class TypeCarburant(models.TextChoices):
    ESSENCE = "ESS", "Essence"
    DIESEL = "DSL", "Diesel"
    ELECTRICITE = "ELEC", "Électricité"
    CNG = "CNG", "Gaz naturel (CNG)"
    LPG = "LPG", "GPL"
    HYDROGENE = "H2", "Hydrogène"


class TypeDistribution(models.TextChoices):
    CHAINE = "CHAINE", "Chaîne"
    COURROIE = "COURROIE", "Courroie"





class MoteurVoiture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations
    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.CASCADE,
        related_name="moteurs",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="moteurs",
        null=True,
        blank=True
    )

    # Spécifications moteur
    type_moteur = models.CharField(
        max_length=20,
        choices=TypeMoteur.choices
    )

    carburant = models.CharField(
        max_length=20,
        choices=TypeCarburant.choices
    )

    cylindree_l = models.FloatField(
        verbose_name="Cylindrée (L)"
    )

    distribution = models.CharField(
        max_length=20,
        choices=TypeDistribution.choices
    )

    nombre_cylindres = models.PositiveSmallIntegerField()

    # Performances
    puissance_ch = models.PositiveIntegerField()
    puissance_tr_min = models.PositiveIntegerField(
        verbose_name="Puissance à (tr/min)"
    )

    couple_nm = models.PositiveIntegerField()
    couple_tr_min = models.PositiveIntegerField(
        verbose_name="Couple à (tr/min)"
    )

    # Lubrification
    qualite_huile = models.CharField(
        max_length=50
    )

    quantite_huile_l = models.FloatField(
        verbose_name="Quantité d’huile (L)"
    )

    # Suivi moteur
    kilometrage_moteur = models.PositiveIntegerField(default=0)

    numero_moteur = models.PositiveSmallIntegerField(
        default=1,
        help_text="1 à 10 (incrémenté à chaque remplacement)"
    )

    intervalle_km_entretien = models.PositiveIntegerField(
        default=15000,
        verbose_name="Intervalle entretien (km)"
    )

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(numero_moteur__gte=1, numero_moteur__lte=10),
                name="numero_moteur_1_10"
            ),
            models.CheckConstraint(
                check=(
                    models.Q(voiture_modele__isnull=False) |
                    models.Q(voiture_exemplaire__isnull=False)
                ),
                name="moteur_lie_a_voiture"
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
