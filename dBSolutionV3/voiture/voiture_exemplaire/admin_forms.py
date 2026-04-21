from django import forms
from .models import VoitureExemplaire


class VoitureExemplaireAdminForm(forms.ModelForm):

    class Meta:
        model = VoitureExemplaire
        fields = "__all__"

    def clean_immatriculation(self):
        immat = self.cleaned_data.get("immatriculation")
        if immat:
            return immat.upper()
        return immat

    def clean(self):
        cleaned_data = super().clean()

        km_chassis = cleaned_data.get("kilometres_chassis") or 0
        km_moteur = cleaned_data.get("kilometres_moteur") or 0

        # ⚠️ Exemple de règle métier utile
        if km_moteur > km_chassis:
            self.add_error(
                "kilometres_moteur",
                "Le kilométrage moteur ne peut pas dépasser le kilométrage châssis."
            )

        return cleaned_data