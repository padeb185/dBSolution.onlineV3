from django import forms
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from .models import Fuel


class FuelForm(forms.ModelForm):

    class Meta:
        model = Fuel
        fields = [
            "immatriculation",
            "voiture_marque",
            "voiture_modele",
            "voiture_exemplaire",
            "volume_max",
            "date",
            "litres",
            "prix_refuelling",
            "validation",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        litres = cleaned_data.get("litres")
        volume_max = cleaned_data.get("volume_max")
        prix_refuelling = cleaned_data.get("prix_refuelling")

        # 🔹 Vérification volume max
        if litres and volume_max:
            if litres > volume_max:
                raise forms.ValidationError(
                    _("Le nombre de litres ne peut pas dépasser le volume maximum du réservoir.")
                )

        # 🔹 Vérification prix positif
        if prix_refuelling and prix_refuelling <= 0:
            raise forms.ValidationError(
                _("Le prix du plein doit être supérieur à 0.")
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # 🔹 Calcul automatique du prix au litre
        if instance.litres and instance.prix_refuelling:
            instance.prix_litre = Decimal(instance.prix_refuelling) / Decimal(instance.litres)

        # 🔹 Récupération automatique du type carburant depuis le modèle véhicule
        if instance.voiture_exemplaire:
            instance.type_carburant = instance.voiture_exemplaire.type_carburant

        if commit:
            instance.save()

        return instance
