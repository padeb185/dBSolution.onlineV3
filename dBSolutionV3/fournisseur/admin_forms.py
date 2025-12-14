from django import forms
from .models import Fournisseur, Facture

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__'

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = '__all__'
        widgets = {
            'date_facture': forms.DateInput(attrs={'type': 'date'})
        }
