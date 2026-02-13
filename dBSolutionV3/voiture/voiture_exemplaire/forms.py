from django import forms
from .models import VoitureExemplaire


class VoitureExemplaireForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = '__all__'
        widgets = {
            "numero_vin": forms.TextInput(attrs={"maxlength": 17, "class": "w-full border rounded px-4 py-2"}),
            "annee_production": forms.NumberInput(attrs={
                "min": 1900,
                "max": 2100,
                "readonly": True,  # rend le champ non éditable
                "class": "w-full border rounded px-4 py-2",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        numero_vin = cleaned_data.get("numero_vin")
        if numero_vin and len(numero_vin) == 17:
            dixieme = numero_vin[9]
            from .utils_vin import get_vin_year
            cleaned_data["annee_production"] = get_vin_year(dixieme, after_2010=True)
        return cleaned_data
