from django import forms
from .models import VoitureExemplaire

class VoitureExemplaireForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = '__all__'  # inclut tous les champs

        widgets = {
            "annee_production": forms.NumberInput(attrs={"min": 1900, "max": 2100, "class": "w-full border border-gray-300 rounded-lg px-4 py-3 text-base"}),
            "mois_production": forms.NumberInput(attrs={"min": 1, "max": 12, "class": "w-full border border-gray-300 rounded-lg px-4 py-3 text-base"}),
            "date_mise_en_circulation": forms.DateInput(attrs={"type": "date", "class": "w-full border border-gray-300 rounded-lg px-4 py-3 text-base"}),
            # tu peux ajouter des widgets similaires pour d'autres champs si tu veux
        }
