from django import forms
from .models import SocieteCliente



class SocieteClienteForm(forms.ModelForm):

    class Meta:
        model = SocieteCliente
        fields = '__all__'



    def clean_numero_tva(self):
        tva = self.cleaned_data.get('numero_tva', '').upper().replace(' ', '')
        if len(tva) < 2 or tva[:2] not in EU_VAT_PREFIXES:
            raise forms.ValidationError(
                "Le numéro de TVA doit commencer par un code pays européen valide (ex: BE, FR, DE...).")

        return tva
