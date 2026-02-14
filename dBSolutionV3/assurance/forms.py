# carrosserie/forms.py
from django import forms
from .models import Assurance

class AssuranceForm(forms.ModelForm):
    class Meta:
        model = Assurance
        fields = [
            'nom_compagnie', 'courtier_nom', 'courtier_prenom',
            'adresse', 'telephone', 'email',
        ]

