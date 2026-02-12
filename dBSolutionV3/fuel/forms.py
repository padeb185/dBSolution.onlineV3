from django import forms
from decimal import Decimal
from .models import Fuel

class FuelForm(forms.ModelForm):
    # Champs readonly
    voiture_marque = forms.CharField(disabled=True, required=False)
    voiture_modele = forms.CharField(disabled=True, required=False)
    taille_reservoir = forms.FloatField(disabled=True, required=False)
    type_carburant = forms.CharField(disabled=True, required=False)

    class Meta:
        model = Fuel
        fields = [
            "immatriculation",
            "voiture_exemplaire",
            "voiture_marque",
            "voiture_modele",
            "taille_reservoir",
            "type_carburant",
            "date",
            "litres",
            "prix_refuelling",
            "validation",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "voiture_exemplaire": forms.HiddenInput(),  # on cache le FK
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si instance existante, remplir les champs readonly
        if self.instance and self.instance.voiture_exemplaire:
            self.fields['voiture_marque'].initial = self.instance.voiture_exemplaire.voiture_marque.nom
            self.fields['voiture_modele'].initial = self.instance.voiture_exemplaire.voiture_modele.nom
            self.fields['taille_reservoir'].initial = self.instance.voiture_exemplaire.voiture_modele.taille_reservoir
            self.fields['type_carburant'].initial = self.instance.voiture_exemplaire.type_carburant

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.voiture_exemplaire:
            instance.voiture_marque = instance.voiture_exemplaire.voiture_marque
            instance.voiture_modele = instance.voiture_exemplaire.voiture_modele
            instance.taille_reservoir = instance.voiture_exemplaire.voiture_modele.taille_reservoir
            instance.type_carburant = instance.voiture_exemplaire.type_carburant

        # Calcul du prix au litre
        if instance.litres and instance.prix_refuelling:
            instance.prix_litre = Decimal(instance.prix_refuelling) / Decimal(instance.litres)

        if commit:
            instance.save()
        return instance
