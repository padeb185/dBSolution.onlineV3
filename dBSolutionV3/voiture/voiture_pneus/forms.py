from django import forms
from ..voiture_pneus.models import VoiturePneus


class VoiturePneusForm(forms.ModelForm):
    class Meta:
        model = VoiturePneus
        fields = '__all__'