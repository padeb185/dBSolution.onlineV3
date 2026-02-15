import uuid
from django.db import models
from django.core.validators import MinValueValidator


class AssurancePolice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assurance = models.ForeignKey(
        'assurance.Assurance',
        on_delete=models.PROTECT,
        related_name='polices'
    )

    voiture_exemplaire = models.ForeignKey(
        'voiture_exemplaire.VoitureExemplaire',
        on_delete=models.PROTECT,
        related_name='polices_assurance'
    )

    numero_contrat = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Numéro de contrat"
    )

    date_debut = models.DateField(
        verbose_name="Date de début"
    )

    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )

    prime_mensuelle = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prime mensuelle (€)",
        null=True,
        blank=True
    )

    prime_annuelle = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Prime annuelle (€)",
        null=True,
        blank=True
    )

    franchise = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Franchise (€)",
        null=True,
        blank=True
    )

    TYPE_COUVERTURE_CHOICES = [
        ('rc', 'RC (Responsabilité civile)'),
        ('mini_omnium', 'Mini-Omnium'),
        ('omnium', 'Omnium complète'),
        ('omnium_financiere', 'Omnium financière'),
    ]

    type_couverture = models.CharField(
        max_length=20,
        choices=TYPE_COUVERTURE_CHOICES,
        default='rc',
        verbose_name="Type de couverture"
    )

    bonus_malus = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Bonus-Malus"
    )

    conducteur_principal = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Conducteur principal"
    )

    actif = models.BooleanField(
        default=True,
        verbose_name="Police active"
    )

    remarques = models.TextField(
        null=True,
        blank=True,
        verbose_name="Remarques"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Police d'assurance"
        verbose_name_plural = "Polices d'assurance"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.numero_contrat} - {self.exemplaire}"

