from django import forms
from voiture.voiture_freins.models import VoitureFreins


class VoitureFreinsForm(forms.ModelForm):
    class Meta:
        model = VoitureFreins
        fields = '__all__'