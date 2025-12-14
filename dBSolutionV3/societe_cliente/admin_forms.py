from django import forms
from .models import SocieteCliente

EU_VAT_PREFIXES = [
    "AT", "BE", "BG", "CY", "CZ", "DE", "DK", "EE", "EL", "ES",
    "FI", "FR", "HR", "HU", "IE", "IT", "LT", "LU", "LV", "MT",
    "NL", "PL", "PT", "RO", "SE", "SI", "SK"
]


class SocieteClienteForm(forms.ModelForm):
    class Meta:
        model = SocieteCliente
        fields = '__all__'  # ou liste des champs spécifiques
        widgets = {
            'numero_tva': forms.TextInput(attrs={'placeholder': 'BE0123456789'}),
            'site': forms.URLInput(attrs={'placeholder': 'https://www.example.com'}),
        }

    def clean_numero_tva(self):
        tva = self.cleaned_data.get('numero_tva', '').upper().replace(' ', '')
        if len(tva) < 2 or tva[:2] not in EU_VAT_PREFIXES:
            raise forms.ValidationError(
                "Le numéro de TVA doit commencer par un code pays européen valide (ex: BE, FR, DE...).")

        return tva