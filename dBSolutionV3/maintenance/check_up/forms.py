# maintenance/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import (
    ControleGeneral, AmortisseurControle, RessortControle,
    ControleBruit, ControleFreins, NettoyageExterieur,
    NettoyageInterieur, JeuPiece, NoteMaintenance,
)
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from ..models import Maintenance


# ---------------------------
# Forms principaux
# ---------------------------


class ControleGeneralForm(ModelForm):
    class Meta:
        model = ControleGeneral
        fields = '__all__'

AmortisseurFormSet = modelformset_factory(AmortisseurControle, fields="__all__", extra=0)
RessortFormSet = modelformset_factory(RessortControle, fields="__all__", extra=0)
BruitFormSet = modelformset_factory(ControleBruit, fields="__all__", extra=0)
JeuxPiecesFormSet = modelformset_factory(JeuPiece, fields="__all__", extra=0)


NettoyageExterieurFormSet = modelformset_factory(NettoyageExterieur, fields= "__all__",extra=0)
NettoyageInterieurFormset = modelformset_factory(NettoyageInterieur, fields= "__all__",extra=0)
NotesFormSet = modelformset_factory(NoteMaintenance, fields="__all__", extra=0)



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

)

JeuPieceFormSet = inlineformset_factory(
    Maintenance,
    JeuPiece,
    form=JeuPieceForm,
    fields='__all__',

)



NettoyageExterieurFormSet = inlineformset_factory(
    Maintenance,
    NettoyageExterieur,
    form=NettoyageExterieurForm,
    fields='__all__',
)

NettoyageInterieurFormset = inlineformset_factory(
    Maintenance,
    NettoyageInterieur,
    form=NettoyageInterieurForm,
    fields='__all__',

)

NoteMaintenanceFormSet = inlineformset_factory(
    Maintenance,
    NoteMaintenance,
    form=NoteMaintenanceForm,
    fields='__all__',
    extra=3
)
