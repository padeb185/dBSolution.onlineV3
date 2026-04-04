import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP
from utilisateurs.models import Utilisateur


class TypeCarburant(models.TextChoices):
    ELECTRICITE = "ELECTRICITE", _("Electricite")

class RechargeCarburant(models.Model):
    # Choix des pays
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

class Electricite(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    societe = models.ForeignKey(
        "societe.Societe",
        on_delete=models.CASCADE,
        related_name="recharge",
        null=True,
        blank=True,
    )


    utilisateur = models.ForeignKey(
        Utilisateur,  # FK vers ton modèle concret
        on_delete=models.CASCADE,
        related_name="recharge",
        verbose_name=_("Utilisateur"),
        null=True,
        blank=True,
    )

    voiture_marque = models.ForeignKey(
        "voiture_marque.VoitureMarque",
        on_delete=models.CASCADE,
        related_name="electricite",
        verbose_name=_("Marque")
    )
    voiture_modele = models.ForeignKey(
        "voiture_modele.VoitureModele",
        on_delete=models.CASCADE,
        related_name="electricite",
        verbose_name=_("Modèle")
    )
    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="electricite",
        verbose_name=_("Véhicule")
    )

    immatriculation = models.CharField(max_length=20, verbose_name=_("Immatriculation"))
    type_carburant = models.CharField(
        max_length=15,
        choices=TypeCarburant.choices,
        verbose_name=_("Type de carburant"),

    )
    volume_max = models.FloatField(verbose_name=_("Kilos Watt max"))
    date = models.DateField(default=timezone.now, verbose_name=_("Date de la recharge"))
    kW = models.FloatField(verbose_name=_("Kilos Watt"))
    prix_recharge = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix de la recharge (€)"))
    prix_watt = models.DecimalField(max_digits=6, decimal_places=4, verbose_name=_("Prix au kilo Watt (€)"))
    date_recharge = models.DateField(default=timezone.now, verbose_name=_("Date de la recharge"), null=True, blank=True)
    temps_recharge = models.DurationField(
        verbose_name=_("Temps de recharge"),
        null=True, blank=True
    )

    pays = models.CharField(
        max_length=2,
        choices=RechargeCarburant.PAYS_CHOICES,
        verbose_name=_("Pays de la recharge")
    )

    kilometrage_electricite = models.IntegerField(
        _("Kilométrage recharge"),
        null=True,
        blank=True
    )

    validation = models.BooleanField(default=True, verbose_name=_("Validation"))

    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant HT"))

    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("TVA"), blank=True, null=True)

    nom_station = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("Electricite")
        verbose_name_plural = _("Electricites")
        ordering = ['-date']

    def __str__(self):
        voiture = self.voiture_exemplaire if self.voiture_exemplaire_id else "N/A"
        return f"{voiture} – {self.date} – {self.kW} kW"



    def save(self, *args, **kwargs):
        # type carburant automatique
        self.type_carburant = TypeCarburant.ELECTRICITE

        # Calcul du prix au kW si nécessaire
        if self.kW and (not self.prix_watt or self.prix_watt == 0):
            self.prix_watt = (Decimal(self.prix_recharge) / Decimal(self.kW)).quantize(
                Decimal('0.0001'), rounding=ROUND_HALF_UP
            )

        # Calcul du montant HT et TVA si pays défini et prix_recharge présent
        if self.prix_recharge and hasattr(RechargeCarburant, "TVA_CARBURANT"):
            tva_percent = RechargeCarburant.TVA_CARBURANT.get(self.pays, 0)
            tva_decimal = Decimal(tva_percent) / Decimal('100')
            self.montant_ht = (Decimal(self.prix_recharge) / (Decimal('1') + tva_decimal)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            self.montant_tva = (Decimal(self.prix_recharge) - self.montant_ht).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )

        super().save(*args, **kwargs)

    @classmethod
    def total_kW_mois(cls, vehicule, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_kW_an(cls, vehicule, year=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_kW_all(cls, vehicule):
        return cls.objects.filter(voiture_exemplaire=vehicule).aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_prix_mois(cls, vehicule, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('prix_recharge'))['total'] or 0

    @classmethod
    def total_prix_an(cls, vehicule, year=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('prix_recharge'))['total'] or 0

    @classmethod
    def total_prix_all(cls, vehicule):
        return cls.objects.filter(voiture_exemplaire=vehicule).aggregate(total=Sum('prix_recharge'))['total'] or 0
