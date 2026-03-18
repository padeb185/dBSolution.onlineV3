from django import forms
from django.forms import ModelForm
from .models import ControleGeneral
from django.utils.translation import gettext_lazy as _

# ---------------------------
# Form principal unique
# ---------------------------
class ControleGeneralForm(ModelForm):
    kilometres_maintenance = forms.FloatField(
        required=False,
        label=_("Kilométrage actuel")
    )
    class Meta:
        model = ControleGeneral
        fields = '__all__'
        widgets = {
            # si tu veux cacher certains champs comme maintenance
            'maintenance': forms.HiddenInput(),
        }