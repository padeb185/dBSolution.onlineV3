from django import forms
from voiture.voiture_boite.models import VoitureBoite


class VoitureBoiteForm(forms.ModelForm):
    class Meta:
        model = VoitureBoite
        exclude = ['voitures_modeles', 'voitures_exemplaires']