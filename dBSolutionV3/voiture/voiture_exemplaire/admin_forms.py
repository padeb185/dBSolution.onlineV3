from django import forms
from .models import VoitureExemplaire


class VoitureExemplaireAdminForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        km_total = cleaned_data.get("kilometres_total")
        km_chassis = cleaned_data.get("kilometres_chassis")
        km_last = cleaned_data.get("kilometres_derniere_intervention")

        if km_total is not None and km_chassis is not None:
            if km_total < km_chassis:
                raise forms.ValidationError(
                    "Les kilomètres totaux ne peuvent pas être inférieurs aux kilomètres châssis."
                )

        if km_last is not None and km_total is not None:
            if km_last > km_total:
                raise forms.ValidationError(
                    "Les kilomètres de la dernière intervention ne peuvent pas dépasser le kilométrage total."
                )

        return cleaned_data
