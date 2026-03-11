from django import forms
from .models import Outillage

class OutillageForm(forms.ModelForm):
    class Meta:
        model = Outillage
        # Champs que l'utilisateur pourra remplir
        fields = [
            'societe',
            'fournisseur',
            'libelle',
            'reference',
            'quantite',
            'prix_htva',
            'taux_tva',
        ]
        labels = {
            'societe': "Société",
            'fournisseur': "Fournisseur",
            'libelle': "Libellé",
            'reference': "Référence",
            'quantite': "Quantité",
            'prix_htva': "Prix HTVA",
            'taux_tva': "Taux de TVA (%)",
        }
        widgets = {
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'prix_htva': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'fournisseur': forms.Select(attrs={'class': 'form-select'}),
            'societe': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')
        if quantite < 1:
            raise forms.ValidationError("La quantité doit être au moins égale à 1.")
        return quantite