from django import forms
from ..voiture_freins_ar.models import VoitureFreinsAR


class VoitureFreinsForm(forms.ModelForm):
    class Meta:
        model = VoitureFreinsAR
        fields = '__all__'