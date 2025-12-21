from django import forms
from .models import VoiturePneusHistorique


class VoiturePneusHistoriqueAdminForm(forms.ModelForm):
    class Meta:
        model = VoiturePneusHistorique
        fields = "__all__"

    def clean_kilometres_effectues(self):
        km = self.cleaned_data.get("kilometres_effectues")
        if km is not None and km <= 0:
            raise forms.ValidationError(
                "Le nombre de kilomètres effectués doit être supérieur à 0."
            )
        return km

    def clean_numero_remplacement(self):
        numero = self.cleaned_data.get("numero_remplacement")
        if numero is not None and numero <= 0:
            raise forms.ValidationError(
                "Le numéro de remplacement doit être supérieur à 0."
            )
        return numero
