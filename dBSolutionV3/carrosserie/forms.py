# carrosserie/forms.py
from django import forms
from .models import Carrosserie

class CarrosserieForm(forms.ModelForm):
    class Meta:
        model = Carrosserie
        fields = [
            'nom_societe', 'responsable_nom', 'responsable_prenom',
            'adresse', 'pays', 'telephone', 'email', 'numero_tva'
        ]



