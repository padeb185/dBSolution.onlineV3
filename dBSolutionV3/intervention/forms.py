from django import forms
from django.forms import inlineformset_factory
from .models import Intervention, MainOeuvre, Peinture, InterventionItem


class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = ["societe", "voiture_exemplaire"]


class InterventionItemForm(forms.ModelForm):
    class Meta:
        model = InterventionItem
        fields = ["type", "reference", "quantite", "prix_unitaire", "taux_tva"]


class MainOeuvreForm(forms.ModelForm):
    class Meta:
        model = MainOeuvre
        fields = ["description", "heures", "taux_horaire"]


class PeintureForm(forms.ModelForm):
    class Meta:
        model = Peinture
        fields = ["zone", "prix"]


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


