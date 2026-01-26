from django import forms
from ..voiture_freins_ar.models import VoitureFreinsAR


class VoitureFreinsARForm(forms.ModelForm):
    class Meta:
        model = VoitureFreinsAR
        fields = '__all__'