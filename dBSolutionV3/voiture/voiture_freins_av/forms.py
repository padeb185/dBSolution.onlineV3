from django import forms
from ..voiture_freins_av.models import VoitureFreinsAV


class VoitureFreinsAVForm(forms.ModelForm):
    class Meta:
        model = VoitureFreinsAV
        # Inclut tous les champs sauf 'voiture_exemplaire'
        exclude = ['voitures_exemplaires', 'societe']