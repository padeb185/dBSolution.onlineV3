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
        fields = [
            "societe",
            "nom",
            "adresse",
            "directeur",
            "numero_tva",
            "site",
            "peppol_id",
            "code_pays",
            "numero_telephone",
            "email",
            "is_active",
        ]
        widgets = {
            "societe": forms.Select(attrs={"class": "form-select"}),
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.Select(attrs={"class": "form-select"}),
            "directeur": forms.TextInput(attrs={"class": "form-control"}),
            "numero_tva": forms.TextInput(attrs={"class": "form-control"}),
            "site": forms.URLInput(attrs={"class": "form-control"}),
            "peppol_id": forms.TextInput(attrs={"class": "form-control"}),
            "code_pays": forms.TextInput(attrs={"class": "form-control"}),
            "numero_telephone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(),
        }

    def clean_numero_tva(self):
        tva = self.cleaned_data.get('numero_tva', '').upper().replace(' ', '')
        if len(tva) < 2 or tva[:2] not in EU_VAT_PREFIXES:
            raise forms.ValidationError(
                "Le numéro de TVA doit commencer par un code pays européen valide (ex: BE, FR, DE...).")

        return tva
