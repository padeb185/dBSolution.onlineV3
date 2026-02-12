from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
from utilisateurs.models import Utilisateur
from societe.models import Societe
from voiture.voiture_moteur.models import TypeCarburant




class TypeCarburant(models.TextChoices):
    ESSENCE = "ESSENCE", _("Essence")
    DIESEL = "DIESEL", _("Diesel")
    HYDROGENE = "HYDROGENE", _("Hydrogène")
    LPG = "LPG", _("LPG")
    CNG = "CNG", _("CNG")
    ETHANOL = "ETHANOL", _("Ethanol")

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




    type_carburant = models.CharField(
        max_length=10,
        choices=TypeCarburant.choices,
        verbose_name=_("Type de carburant"),

    )
    immatriculation = models.CharField(
        max_length=20,
        verbose_name=_("Immatriculation"),
        blank=True,
    )

    date = models.DateField(default=timezone.now, verbose_name=_("Date du plein"))
    litres = models.DecimalField(max_digits = 10 , decimal_places = 2, verbose_name=_("Litres"))
    prix_litre = models.DecimalField(max_digits=6, decimal_places=3, verbose_name=_("Prix au litre (€)"))
    prix_refuelling = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Prix du plein (€)"))

    validation = models.BooleanField(default=True, verbose_name=_("Validation"))

    class Meta:
        verbose_name = _("Carburant")
        verbose_name_plural = _("Carburants")
        ordering = ['-date']

    def __str__(self):
        return f"{self.voiture_exemplaire} – {self.date} – {self.litres} L"

    def save(self, *args, **kwargs):
        # Calcul automatique du prix au litre si non renseigné
        if not self.prix_litre is None and self.litres:
            self.prix_litre = Decimal(self.prix_refuelling) / Decimal(self.litres)
        super().save(*args, **kwargs)

    @classmethod
    def total_litres_mois(cls, vehicule, year=None, month=None):
        qs = cls.objects.filter(voiture_exemplaire=vehicule)
        if year and month:
            qs = qs.filter(date__year=year, date__month=month)
        return qs.aggregate(total=Sum('litres'))['total'] or 0

    @classmethod
    def total_litres_an(cls, vehicule, year=None):
        qs = cls.objects.filter(vehicule=vehicule)
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
