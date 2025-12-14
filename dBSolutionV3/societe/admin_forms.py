from django import forms
from .models import Societe

class SocieteAdminForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = '__all__'

    # Validation supplémentaire côté admin
    def clean_nom(self):
        nom = self.cleaned_data.get('nom', '').strip()
        if not nom:
            raise forms.ValidationError("Le nom de la société ne peut pas être vide.")
        return nom

    def clean_numero_tva(self):
        numero_tva = self.cleaned_data.get('numero_tva', '').strip()
        if not numero_tva:
            raise forms.ValidationError("Le numéro de TVA ne peut pas être vide.")
        return numero_tva
