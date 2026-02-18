from django import forms
from decimal import Decimal
from .models import Fuel
from django.utils.translation import gettext_lazy as _

class FuelForm(forms.ModelForm):
    # ---------------------------
    # Champs affichés dans le formulaire
    # ---------------------------

    voiture_marque = forms.CharField(label="Marque", required=False, disabled=True)
    voiture_modele = forms.CharField(label="Modèle", required=False, disabled=True)
    taille_reservoir_display = forms.FloatField(label="Volume max (L)", required=False, disabled=True)

    # Taux de TVA
    TVA_PAYS = {
        'BE': Decimal('21.0'),
        'LU': Decimal('17.0'),
        'DE': Decimal('19.0'),
    }

    class Meta:
        model = Fuel
        fields = [
            "immatriculation",
            "voiture_exemplaire",
            "kilometrage_fuel",
            "type_carburant",
            "date",
            "litres",
            "prix_refuelling",
            "pays",
            "validation",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "voiture_exemplaire": forms.HiddenInput(),
        }

    # ---------------------------
    # Initialisation
    # ---------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Récupérer voiture_exemplaire uniquement si elle existe
        voiture = getattr(self.instance, "voiture_exemplaire", None)
        if voiture is not None:
            self.fields["voiture_marque"].initial = voiture.voiture_marque.nom_marque
            self.fields["voiture_modele"].initial = voiture.voiture_modele.nom_modele
            self.fields["taille_reservoir_display"].initial = voiture.voiture_modele.taille_reservoir

            # Initialiser kilometrage_fuel à partir du Fuel existant, sinon voiture
            if getattr(self.instance, "kilometrage_fuel", None) is not None:
                self.fields["kilometrage_fuel"].initial = self.instance.kilometrage_fuel
            else:
                self.fields["kilometrage_fuel"].initial = voiture.kilometres_chassis

    # ---------------------------
    # Save
    # ---------------------------
    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire

        # 1️⃣ Sauvegarder le kilométrage du plein dans Fuel
        instance.kilometrage_fuel = self.cleaned_data["kilometrage_fuel"]

        # 2️⃣ Mettre à jour le kilométrage de la voiture si le plein est plus grand
        if voiture and instance.kilometrage_fuel >= voiture.kilometres_chassis:
            voiture.kilometres_chassis = instance.kilometrage_fuel
            voiture.save()

        # Remplissage automatique des infos voiture
        if voiture:
            instance.voiture_marque = voiture.voiture_marque
            instance.voiture_modele = voiture.voiture_modele
            instance.taille_reservoir = voiture.voiture_modele.taille_reservoir

        # Calcul du prix au litre et TVA
        if instance.litres and instance.prix_refuelling:
            instance.prix_litre = Decimal(instance.prix_refuelling) / Decimal(instance.litres)
            taux_tva = self.TVA_PAYS.get(instance.pays, Decimal('0.0'))
            instance.montant_tva = Decimal(instance.prix_refuelling) * taux_tva / Decimal('100.0')
            instance.montant_ht = Decimal(instance.prix_refuelling) - instance.montant_tva
        else:
            instance.prix_litre = Decimal('0.0')
            instance.montant_tva = Decimal('0.0')
            instance.montant_ht = Decimal('0.0')

        if commit:
            instance.save()

        return instance
