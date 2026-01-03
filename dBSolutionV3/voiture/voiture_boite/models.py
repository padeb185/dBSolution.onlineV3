from django.db import models
import uuid
from django.db.models import Q


class TypeEntretienBoite(models.TextChoices):
    VIDANGE = "VIDANGE", "Vidange"
    FILTRE = "FILTRE", "Changement filtre"
    REMPLACEMENT = "REMPLACEMENT", "Remplacement boîte"


class VoitureBoite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relations (1 des 2 obligatoire)
    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.CASCADE,
        related_name="boites",
        null=True,
        blank=True
    )

    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="boites",
        null=True,
        blank=True
    )

    # Lubrification
    qualite_huile = models.CharField(max_length=20, verbose_name="Qualité huile boîte")
    quantite_huile_l = models.FloatField(verbose_name="Quantité huile boîte (L)")

    # Suivi kilométrique
    kilometrage_boite = models.PositiveIntegerField(default=0)
    intervalle_entretien_km = models.PositiveIntegerField(default=60000, verbose_name="Intervalle entretien (km)")

    # Historique entretien
    dernier_entretien = models.CharField(max_length=20, choices=TypeEntretienBoite.choices, null=True, blank=True)

    # Gestion remplacement
    numero_boite = models.PositiveSmallIntegerField(default=1, help_text="1 à 10 (incrémenté à chaque remplacement)")

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(numero_boite__gte=1) & Q(numero_boite__lte=10),
                name="numero_boite_1_10"
            ),
            models.CheckConstraint(
                condition=Q(voiture_modele__isnull=False) | Q(voiture_exemplaire__isnull=False),
                name="boite_liée_a_voiture"
            ),
        ]

    def __str__(self):
        return f"Boîte #{self.numero_boite} - {self.kilometrage_boite} km"

    def prochain_entretien_km(self):
        return self.kilometrage_boite + self.intervalle_entretien_km

    def remplacer_boite(self):
        if self.numero_boite < 10:
            self.numero_boite += 1
            self.kilometrage_boite = 0
            self.dernier_entretien = TypeEntretienBoite.REMPLACEMENT
            self.save()

    def vidange(self):
        self.dernier_entretien = TypeEntretienBoite.VIDANGE
        self.save()

    def changer_filtre(self):
        self.dernier_entretien = TypeEntretienBoite.FILTRE
        self.save()
