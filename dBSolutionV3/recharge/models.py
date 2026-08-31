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
        ('AT', _("Autriche")),
        ('BE', _("Belgique")),
        ('BG', _("Bulgarie")),
        ('HR', _("Croatie")),
        ('CY', _("Chypre")),
        ('CZ', _("Tchéquie")),
        ('DK', _("Danemark")),
        ('EE', _("Estonie")),
        ('FI', _("Finlande")),
        ('FR', _("France")),
        ('DE', _("Allemagne")),
        ('GR', _("Grèce")),
        ('HU', _("Hongrie")),
        ('IE', _("Irlande")),
        ('IT', _("Italie")),
        ('LV', _("Lettonie")),
        ('LT', _("Lituanie")),
        ('LU', _("Luxembourg")),
        ('MT', _("Malte")),
        ('NL', _("Pays-Bas")),
        ('PL', _("Pologne")),
        ('PT', _("Portugal")),
        ('RO', _("Roumanie")),
        ('SK', _("Slovaquie")),
        ('SI', _("Slovénie")),
        ('ES', _("Espagne")),
        ('SE', _("Suède")),
        ('GB', _("Royaume-Uni")),
    ]

    # Mapping pays → TVA électricité
    TVA_ELECTRICITE = {
        'AT': 20,
        'BE': 21,
        'BG': 20,
        'HR': 25,
        'CY': 19,
        'CZ': 21,
        'DK': 25,
        'EE': 24,
        'FI': 25.5,
        'FR': 20,
        'DE': 19,
        'GR': 24,
        'HU': 27,
        'IE': 23,
        'IT': 22,
        'LV': 21,
        'LT': 21,
        'LU': 17,
        'MT': 18,
        'NL': 21,
        'PL': 23,
        'PT': 23,
        'RO': 21,
        'SK': 23,
        'SI': 22,
        'ES': 21,
        'SE': 25,
        'GB': 20,
    }


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
        default=TypeCarburant.ELECTRICITE,
        verbose_name=_("Type de carburant"),

    )

    date = models.DateField(default=timezone.now, verbose_name=_("Date de la recharge"))
    taille_batterie = models.FloatField(verbose_name= _("Capacité en KW"), null=True, blank=True)
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

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )

    kilometrage_electricite = models.IntegerField(
        _("Kilométrage recharge"),
        null=True,
        blank=True
    )
    kilometrage_variation = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_("Variation du kilométrage"),
    )

    validation = models.BooleanField(default=True, verbose_name=_("Validation"))

    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant HT"))

    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("TVA"), blank=True, null=True)


    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


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

        # Calcul du prix au kW
        if self.kW and (not self.prix_watt or self.prix_watt == 0):
            self.prix_watt = (Decimal(self.prix_recharge) / Decimal(self.kW)).quantize(
                Decimal('0.0001'), rounding=ROUND_HALF_UP
            )

        # Calcul HT et TVA
        tva_percent = RechargeCarburant.TVA_ELECTRICITE.get(self.pays or 'BE', 0)
        tva_decimal = Decimal(tva_percent) / Decimal('100')
        if self.prix_recharge:
            self.montant_ht = (Decimal(self.prix_recharge) / (Decimal('1') + tva_decimal)).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            self.montant_tva = (Decimal(self.prix_recharge) - self.montant_ht).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
        else:
            self.montant_ht = Decimal('0.00')
            self.montant_tva = Decimal('0.00')

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





    @classmethod
    def total_kW_mois_exemplaire(cls, exemplaire, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_kW_an_exemplaire(cls, exemplaire, year=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_KW_all_exemplaire(cls, exemplaire):
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('kW'))['total'] or 0

    @classmethod
    def total_prix_mois_exemplaire(cls, exemplaire, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('prix_recharge'))['total'] or 0

    @classmethod
    def total_prix_an_exemplaire(cls, exemplaire, year=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('prix_recharge'))['total'] or 0

    @classmethod
    def total_prix_all_exemplaire(cls, exemplaire):
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('prix_recharge'))['total'] or 0

    @classmethod
    def total_tva_mois_exemplaire(cls, exemplaire, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')

    @classmethod
    def total_tva_an_exemplaire(cls, exemplaire, year=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')

    @classmethod
    def total_tva_par_pays_exemplaire(cls, exemplaire, year=None, month=None):
        """
        Retourne un dictionnaire {pays: total_tva} pour le mois ou l'année si spécifié,
        mais uniquement pour un exemplaire spécifique.
        """
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)

        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        result = {}
        for code, nom in RechargeCarburant.PAYS_CHOICES:
            total = qs.filter(pays=code).aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')
            result[code] = total
        return result

    @classmethod
    def total_tva_all_exemplaire(cls, exemplaire):
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('montant_tva'))[
            'total'] or Decimal('0.00')

    @classmethod
    def total_tva_global_exemplaire(cls, year=None, month=None):
        """
        Retourne le total TVA pour tous les pays combinés.
        """
        qs = cls.objects.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        return qs.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')


