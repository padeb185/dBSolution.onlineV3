from django import forms
from .models import VoitureExemplaire

class VoitureExemplaireForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = "__all__"

