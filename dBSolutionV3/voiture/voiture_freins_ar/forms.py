from django import forms
from ..voiture_freins_ar.models import VoitureFreinsAR


class VoitureFreinsARForm(forms.ModelForm):
    class Meta:
        model = VoitureFreinsAR
        # Inclut tous les champs sauf 'voiture_exemplaire'
        exclude = ['voitures_exemplaires', 'societe']