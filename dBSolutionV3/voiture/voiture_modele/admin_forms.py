from django import forms
from .models import VoitureModele


class VoitureModeleAdminForm(forms.ModelForm):
    class Meta:
        model = VoitureModele
        fields = "__all__"

    def clean_taille_reservoir(self):
        taille = self.cleaned_data.get("taille_reservoir")
        if taille is not None and taille <= 0:
            raise forms.ValidationError("La taille du réservoir doit être supérieure à 0 litre.")
        return taille

    def clean_nbre_places(self):
        places = self.cleaned_data.get("nbre_places")
        if places is not None and places <= 0:
            raise forms.ValidationError("Le nombre de places doit être supérieur à 0.")
        return places
