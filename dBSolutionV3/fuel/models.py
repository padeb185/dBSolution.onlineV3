from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP

from recharge.models import RechargeCarburant
from utilisateurs.models import Utilisateur
from societe.models import Societe



class TypeCarburant(models.TextChoices):
    ESSENCE98 = "ESSENCE98", _("Essence 98")
    ESSENCE95 = "ESSENCE95", _("Essence 95")
    DIESEL = "DIESEL", _("Diesel")
    DIESELPLUS = "DIESELPLUS", _("Diesel +")
    HYDROGENE = "HYDROGENE", _("Hydrogène")
    LPG = "LPG", _("LPG")
    CNG = "CNG", _("CNG")
    ETHANOL = "ETHANOL", _("Ethanol")



class Fuel(models.Model):
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

    # Taux de TVA sur le carburant
    TVA_CARBURANT = {
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


    id = models.AutoField(primary_key=True)

    societe = models.ForeignKey(
        Societe,
        on_delete=models.CASCADE,
        related_name="fuel",
        verbose_name=_("Societe"),
        null=True,
        blank=True,
    )

    utilisateur = models.ForeignKey(
        Utilisateur,  # FK vers ton modèle concret
        on_delete=models.SET_NULL,
        related_name="fuels",
        verbose_name=_("Utilisateur"),
        null=True,
        blank=True,
    )


    voiture_exemplaire = models.ForeignKey(
        "voiture_exemplaire.VoitureExemplaire",
        on_delete=models.CASCADE,
        related_name="fuels",
        verbose_name=_("Véhicule")
    )
    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("Kilomètres chassis")
    )


    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )

    type_carburant = models.CharField(
        max_length=10,
        choices=TypeCarburant.choices,
        default=TypeCarburant.ESSENCE98,
        verbose_name=_("Type de carburant"),

    )


    kilometrage_fuel = models.IntegerField(
        _("Kilométrage au plein"),
    )

    nom_station = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    date = models.DateTimeField(default=timezone.now, verbose_name=_("Date du plein"))
    litres = models.DecimalField(max_digits = 10 , decimal_places = 2, verbose_name=_("Litres"))

    prix_refuelling = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix du plein (€)"))

    prix_litre = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Prix au litre (€)")


    pays = models.CharField(
        max_length=25,
        choices=PAYS_CHOICES,
        verbose_name=_("Pays de la station")
    )

    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant HT"))

    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("TVA"), blank=True, null=True)


    remarques = models.TextField(null=True, blank=True, verbose_name=_("Remarques"))

    validation = models.BooleanField(default=True, verbose_name=_("Validation"))


    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(_("Mis à jour le"), auto_now=True, blank=True, null=True)


    class Meta:
        verbose_name = _("Carburant")
        verbose_name_plural = _("Carburants")
        ordering = ['-date']

    def __str__(self):
        voiture = getattr(self, "voiture_exemplaire", None)
        immat = str(voiture) if voiture else "N/A"
        date = self.date if self.date else "N/A"
        litres = f"{self.litres} L" if self.litres else "N/A"
        return f"{immat} – {date} – {litres}"

    def save(self, *args, **kwargs):
        tva_percent = self.TVA_CARBURANT.get(self.pays, 0)

        tva_decimal = Decimal(str(tva_percent)) / Decimal("100")

        prix_refuelling = self.prix_refuelling or Decimal("0.00")

        self.montant_ht = (
                prix_refuelling / (Decimal("1") + tva_decimal)
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        self.montant_tva = (
                prix_refuelling - self.montant_ht
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )

        super().save(*args, **kwargs)

    @classmethod
    def total_litres_mois(cls, vehicule, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('litres'))['total'] or 0



    @classmethod
    def total_litres_an(cls, vehicule, year=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('litres'))['total'] or 0




    @classmethod
    def total_litres_all(cls, vehicule):
        return cls.objects.filter(vehicule=vehicule).aggregate(total=Sum('litres'))['total'] or 0



    @classmethod
    def total_prix_mois(cls, vehicule, year=None, month=None):
        qs = cls.objects.filter(vehicule=vehicule)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('prix_refuelling'))['total'] or 0


    @classmethod
    def total_prix_an(cls, vehicule, year=None):
        qs = cls.objects.filter(vehicule=vehicule)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('prix_refuelling'))['total'] or 0

    @classmethod
    def total_prix_all(cls, vehicule):
        return cls.objects.filter(vehicule=vehicule).aggregate(total=Sum('prix_refuelling'))['total'] or 0

    @classmethod
    def total_tva_par_pays(cls, year=None, month=None):

        qs = cls.objects.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        result = {}
        for code, nom in cls.RechargeCarburant.PAYS_CHOICES:
            total = qs.filter(pays=code).aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')
            result[code] = total
        return result


    @classmethod
    def total_tva_global(cls, year=None, month=None):

        qs = cls.objects.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        return qs.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')



 # Totaux par exemplaire

    @classmethod
    def total_litres_mois_exemplaire(cls, exemplaire, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('litres'))['total'] or 0


    @classmethod
    def total_litres_an_exemplaire(cls, exemplaire, year=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('litres'))['total'] or 0


    @classmethod
    def total_litres_all_exemplaire(cls, exemplaire):
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('litres'))['total'] or 0


    @classmethod
    def total_prix_mois_exemplaire(cls, exemplaire, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('prix_refuelling'))['total'] or 0


    @classmethod
    def total_prix_an_exemplaire(cls, exemplaire, year=None):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire)
        if year:
            qs = qs.filter(date__year=year)
        return qs.aggregate(total=Sum('prix_refuelling'))['total'] or 0


    @classmethod
    def total_prix_all_exemplaire(cls, exemplaire):
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('prix_refuelling'))['total'] or 0


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
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')


    @classmethod
    def total_tva_global_exemplaire(cls, year=None, month=None):

        qs = cls.objects.all()
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        elif year:
            qs = qs.filter(date__year=year)

        return qs.aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')


    @classmethod
    def consommation_moyenne_all(cls, exemplaire):
        qs = cls.objects.filter(voiture_exemplaire=exemplaire).order_by('date')
        if qs.count() < 2:
            return Decimal('0.0')

        total_distance = qs.last().kilometrage_fuel - qs.first().kilometrage_fuel
        total_litres = sum(f.litres for f in qs[:-1])

        if total_distance == 0:
            return Decimal('0.0')

        consommation = (Decimal(total_litres) / Decimal(total_distance)) * 100
        return consommation.quantize(Decimal('0.01'))



    @classmethod
    def consommation_moyenne_mois(cls, vehicule, year, month):
        qs = cls.objects.filter(voiture_exemplaire=vehicule, date__year=year, date__month=month).order_by('date')
        if qs.count() < 2:
            return Decimal('0.0')  # pas assez de données

        total_distance = qs.last().kilometrage_fuel - qs.first().kilometrage_fuel
        total_litres = sum(f.litres for f in qs[:-1])  # on ignore le dernier plein
        if total_distance == 0:
            return Decimal('0.0')

        consommation = (Decimal(total_litres) / Decimal(total_distance)) * 100
        return consommation.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


    @classmethod
    def consommation_moyenne_an(cls, vehicule, year):
        qs = cls.objects.filter(voiture_exemplaire=vehicule, date__year=year).order_by('date')
        if qs.count() < 2:
            return Decimal('0.0')  # pas assez de données

        total_distance = qs.last().kilometrage_fuel - qs.first().kilometrage_fuel
        total_litres = sum(f.litres for f in qs[:-1])  # on ignore le dernier plein
        if total_distance == 0:
            return Decimal('0.0')

        consommation = (Decimal(total_litres) / Decimal(total_distance)) * 100
        return consommation.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)