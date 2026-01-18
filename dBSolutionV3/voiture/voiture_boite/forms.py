from django import forms
from voiture.voiture_boite.models import VoitureBoite


class VoitureBoiteForm(forms.ModelForm):
    class Meta:
        model = VoitureBoite
        fields = '__all__'