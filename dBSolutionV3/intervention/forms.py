from django import forms
from django.forms import inlineformset_factory
from .models import Intervention, MainOeuvre, Peinture, InterventionItem


from django import forms
from .models import Intervention, InterventionItem, MainOeuvre, Peinture, TypePieceCarrosserie


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = [
            "societe",
            "voiture_exemplaire",
        ]
        widgets = {
            "societe": forms.Select(attrs={"class": "form-select"}),
            "voiture_exemplaire": forms.Select(attrs={"class": "form-select"}),
        }


class InterventionItemForm(forms.ModelForm):
    class Meta:
        model = InterventionItem
        fields = [
            "type",
            "reference",
            "quantite",
            "prix_unitaire",
            "taux_tva",
        ]
        widgets = {
            "type": forms.Select(choices=TypePieceCarrosserie.choices, attrs={"class": "form-select"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
            "quantite": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "prix_unitaire": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "taux_tva": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class MainOeuvreForm(forms.ModelForm):
    class Meta:
        model = MainOeuvre
        fields = [
            "description",
            "heures",
            "taux_horaire",
        ]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "heures": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "taux_horaire": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class PeintureForm(forms.ModelForm):
    class Meta:
        model = Peinture
        fields = [
            "zone",
            "prix",
        ]
        widgets = {
            "zone": forms.TextInput(attrs={"class": "form-control"}),
            "prix": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }

# Formsets
InterventionItemFormSet = inlineformset_factory(
    Intervention,
    InterventionItem,
    form=InterventionItemForm,
    extra=1,
    can_delete=True
)

MainOeuvreFormSet = inlineformset_factory(
    Intervention,
    MainOeuvre,
    form=MainOeuvreForm,
    extra=1,
    can_delete=True
)

PeintureFormSet = inlineformset_factory(
    Intervention,
    Peinture,
    form=PeintureForm,
    extra=1,
    can_delete=True
)


