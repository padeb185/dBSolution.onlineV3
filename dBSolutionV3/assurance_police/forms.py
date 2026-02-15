from django import forms
from .models import AssurancePolice


class AssurancePoliceForm(forms.ModelForm):
    class Meta:
        model = AssurancePolice
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'remarques': forms.Textarea(attrs={'rows': 3}),
        }
