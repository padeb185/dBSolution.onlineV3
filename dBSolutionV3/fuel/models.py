from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP
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

class RechargeCarburant(models.Model):
    # Choix des pays
    PAYS_CHOICES = [
        ('BE', _("Belgique")),
        ('LU', _("Luxembourg")),
        ('DE', _("Allemagne")),
    ]

    # Mapping pays → TVA carburant
    TVA_CARBURANT = {
        'BE': 21,
        'LU': 17,
        'DE': 19,
    }



class Fuel(models.Model):
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
        on_delete=models.CASCADE,
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

    kilometres_chassis = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )

    kilometrage_fuel = models.IntegerField(
        _("Kilométrage au plein"),
        null=True,
        blank=True
    )

    nom_station = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    date = models.DateField(default=timezone.now, verbose_name=_("Date du plein"))
    litres = models.DecimalField(max_digits = 10 , decimal_places = 2, verbose_name=_("Litres"))

    prix_refuelling = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix du plein (€)"))

    prix_litre = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Prix au litre (€)")


    pays = models.CharField(
        max_length=25,
        choices=RechargeCarburant.PAYS_CHOICES,
        verbose_name=_("Pays de la station")
    )

    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Montant HT"))

    montant_tva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("TVA"), blank=True, null=True)




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
        tva_percent = RechargeCarburant.TVA_CARBURANT.get(self.pays, 0)
        tva_decimal = Decimal(tva_percent) / Decimal('100')
        self.montant_ht = (self.prix_refuelling / (Decimal('1') + tva_decimal)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        self.montant_tva = (self.prix_refuelling - self.montant_ht).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
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
        """
        Retourne un dictionnaire {pays: total_tva} pour le mois ou l'année si spécifié.
        """
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
        """
        Retourne le total TVA pour tous les pays combinés.
        """
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
        return cls.objects.filter(voiture_exemplaire=exemplaire).aggregate(total=Sum('montant_tva'))['total'] or Decimal('0.00')

