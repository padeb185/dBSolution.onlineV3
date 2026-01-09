from django import forms
from .models import VoitureExemplaire

class VoitureExemplaireForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = [
            "immatriculation",
            "numero_vin",
            "type_utilisation",
            "kilometres_total",
            "couleur",
            "code_couleur",
            "annee_production",
            "mois_production",
            "date_mise_en_circulation",
        ]
        widgets = {
            "annee_production": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
            "mois_production": forms.NumberInput(attrs={"min": 1, "max": 12}),
            "date_mise_en_circulation": forms.DateInput(attrs={"type": "date"}),
        }
