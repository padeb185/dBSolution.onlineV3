from django import forms
from .models import Voiture, ProprietairePart

class ProprietairePartForm(forms.ModelForm):
    class Meta:
        model = ProprietairePart
        fields = ['nom_proprietaire', 'part_proprietaire_pourcent']
        widgets = {
            'part_proprietaire_pourcent': forms.NumberInput(attrs={'step': 0.01, 'min': 0, 'max': 100}),
        }

ProprietairePartFormSet = forms.inlineformset_factory(
    Voiture,
    ProprietairePart,
    form=ProprietairePartForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True
)
