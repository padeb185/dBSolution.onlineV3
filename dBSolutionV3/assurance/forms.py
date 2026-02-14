# carrosserie/forms.py
from django import forms
from .models import Assurance

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = [
            'nom_compagnie', 'courtier_nom', 'courtier_prenom',
            'telephone', 'email', 'peppol_id', 'numero_iban', 'adresse'
        ]
        widgets = {
            'nom_compagnie': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Nom de la compagnie',
                'required': True,
            }),
            'courtier_nom': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Nom du courtier',
            }),
            'courtier_prenom': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Prénom du courtier',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Téléphone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Email',
            }),
            'peppol_id': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Numéro Peppol',
            }),

            'numero_iban': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Numéro IBAN',
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'border rounded px-4 py-2 w-full',
                'placeholder': 'Adresse',
            }),

        }
