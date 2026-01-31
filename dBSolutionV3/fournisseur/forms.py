from django import forms
from .models import Fournisseur


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = "__all__"
        widgets = {
            "taux_tva": forms.NumberInput(attrs={"step": "0.01"}),
            "country_code": forms.TextInput(attrs={"maxlength": 2}),
        }
