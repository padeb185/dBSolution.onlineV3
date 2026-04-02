from django import forms
from ..voiture_freins.models import VoitureFreins


class VoitureFreinsForm(forms.ModelForm):
    class Meta:
        model = VoitureFreins
        # Inclut tous les champs sauf 'voiture_exemplaire'
        exclude = ['voitures_exemplaires', 'societe']