import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class AssurancePolice(models.Model):
    FREQUENCE_CHOICES = [
        ('mensuel', _('Mensuel')),
        ('annuel', _('Annuel')),
    ]

    MODE_PAIEMENT_CHOICES = [
        ('virement', _('Virement')),
        ('domiciliation', _('Domiciliation')),
        ('cash', _('Cash')),
        ('carte', _('Carte bancaire')),
    ]

    TYPE_COUVERTURE_CHOICES = [
        ('rc', _('Responsabilité civile')),
        ('mini_omnium', _('Mini-Omnium')),
        ('omnium', _('Omnium complète')),
        ('omnium_financiere', _('Omnium financière')),
    ]



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assurance = models.ForeignKey(
        'assurance.Assurance',
        on_delete=models.PROTECT,
        related_name='polices',
        blank=True,
    )

    voiture_exemplaire = models.ForeignKey(
        'voiture_exemplaire.VoitureExemplaire',
        on_delete=models.PROTECT,
        related_name='polices_assurance',
        blank=True,
    )

    numero_contrat = models.CharField(max_length=100, unique=True)

    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    prime_mensuelle = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True, blank=True
    )

    prime_annuelle = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True, blank=True
    )

    franchise = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True, blank=True
    )

    type_couverture = models.CharField(
        max_length=20,
        choices=TYPE_COUVERTURE_CHOICES,
        default='rc',
        verbose_name=_("Type de couverture")
    )

    bonus_malus = models.IntegerField(null=True, blank=True)

    frequence_paiement = models.CharField(
        max_length=10,
        choices=FREQUENCE_CHOICES,
        default='annuel',
        verbose_name=_("Fréquence de paiement")
    )

    mode_paiement = models.CharField(
        max_length=15,
        choices=MODE_PAIEMENT_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Mode de paiement")
    )

    courtier = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    document_pdf = models.FileField(
        upload_to='assurances/polices/',
        null=True,
        blank=True
    )

    actif = models.BooleanField(default=True)

    remarques = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_debut']
        verbose_name = _("Police d'assurance")
        verbose_name_plural = _("Polices d'assurance")

    def __str__(self):
        return f"{self.numero_contrat} - {self.voiture_exemplaire}"

    # 🔎 PROPRIÉTÉS UTILES

    @property
    def est_expiree(self):
        return self.date_fin and self.date_fin < timezone.now().date()

    @property
    def expire_bientot(self):
        if not self.date_fin:
            return False
        return timezone.now().date() <= self.date_fin <= timezone.now().date() + timezone.timedelta(days=30)

    @staticmethod
    def cout_total_annuel():
        polices = AssurancePolice.objects.filter(actif=True)

        total = 0
        for p in polices:
            if p.prime_annuelle:
                total += p.prime_annuelle
            elif p.prime_mensuelle:
                total += p.prime_mensuelle * 12

        return total











class Sinistre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    police = models.ForeignKey(
        'AssurancePolice',
        on_delete=models.CASCADE,
        related_name='sinistres'
    )

    date_sinistre = models.DateField()
    description = models.TextField()

    montant_estime = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    responsable = models.BooleanField(
        default=True,
        verbose_name=_("Responsable")
    )

    cloture = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sinistre']
        verbose_name = _("Sinistre")
        verbose_name_plural = _("Sinistres")

    def __str__(self):
        return f"Sinistre {self.date_sinistre} - {self.police.numero_contrat}"





def cout_total_annuel():
    polices = AssurancePolice.objects.filter(actif=True)

    total = 0
    for p in polices:
        if p.prime_annuelle:
            total += p.prime_annuelle
        elif p.prime_mensuelle:
            total += p.prime_mensuelle * 12
    return total
