from django import forms
from django.forms import ModelForm
from .models import ControleGeneral

# ---------------------------
# Form principal unique
# ---------------------------
class ControleGeneralForm(ModelForm):
    class Meta:
        model = ControleGeneral
        fields = '__all__'
        widgets = {
            # si tu veux cacher certains champs comme maintenance
            'maintenance': forms.HiddenInput(),
        }