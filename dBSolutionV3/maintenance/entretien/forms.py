from django import forms
from .models import Entretien, EntretienOperation, EntretienFluide

class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = [
            "voiture_exemplaire",
            "kilometrage_prevu",
            "date_prevue",
            "alerte_avant_km",
        ]
        widgets = {
            "date_prevue": forms.DateInput(attrs={"type": "date"}),
        }


class EntretienOperationForm(forms.ModelForm):
    class Meta:
        model = EntretienOperation
        fields = [
            "type_operation",
            "piece",
            "quantite",
        ]


class EntretienFluideForm(forms.ModelForm):
    class Meta:
        model = EntretienFluide
        fields = [
            "piece_fluide",
            "quantite",
        ]