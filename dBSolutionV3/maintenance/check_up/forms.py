# maintenance/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (
    ControleGeneral, AmortisseurControle, RessortControle,
    ControleBruit, ControleFreins, NettoyageExterieur,
    NettoyageInterieur, JeuPiece, NoteMaintenance
)
from ..models import Maintenance


# ---------------------------
# Forms principaux
# ---------------------------
class ControleGeneralForm(forms.ModelForm):
    class Meta:
        model = ControleGeneral
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
        }

class ControleFreinsForm(forms.ModelForm):
    class Meta:
        model = ControleFreins
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
        }

class NettoyageExterieurForm(forms.ModelForm):
    class Meta:
        model = NettoyageExterieur
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
            'voiture_exemplaire': forms.HiddenInput(),
            'mecanicien': forms.HiddenInput(),
        }

class NettoyageInterieurForm(forms.ModelForm):
    class Meta:
        model = NettoyageInterieur
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
            'voiture_exemplaire': forms.HiddenInput(),
            'mecanicien': forms.HiddenInput(),
        }

class JeuPieceForm(forms.ModelForm):
    class Meta:
        model = JeuPiece
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
            'vehicle': forms.HiddenInput(),
        }

class NoteMaintenanceForm(forms.ModelForm):
    class Meta:
        model = NoteMaintenance
        fields = '__all__'
        widgets = {
            'maintenance': forms.HiddenInput(),
            'auteur': forms.HiddenInput(),
        }

# ---------------------------
# Formsets pour éléments multiples
# ---------------------------
AmortisseurFormSet = inlineformset_factory(
    ControleGeneral,
    AmortisseurControle,
    fields='__all__',
    extra=4  # 4 amortisseurs par exemple
)

RessortFormSet = inlineformset_factory(
    ControleGeneral,
    RessortControle,
    fields='__all__',
    extra=4
)

BruitFormSet = inlineformset_factory(
    ControleGeneral,
    ControleBruit,
    fields='__all__',
    extra=3
)

JeuPieceFormSet = inlineformset_factory(
    Maintenance,
    JeuPiece,
    form=JeuPieceForm,
    fields='__all__',
    extra=5
)

NoteMaintenanceFormSet = inlineformset_factory(
    Maintenance,
    NoteMaintenance,
    form=NoteMaintenanceForm,
    fields='__all__',
    extra=3
)