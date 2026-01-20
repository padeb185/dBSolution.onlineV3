# moteur/forms.py
from django import forms
from .models import MoteurVoiture

# forms.py
from django import forms
from .models import MoteurVoiture, TypeMoteur, TypeCarburant

class MoteurVoitureForm(forms.ModelForm):
    class Meta:
        model = MoteurVoiture
        fields = [
            "motoriste", "code_moteur", "type_moteur", "carburant",
            "cylindree_l", "distribution", "nombre_cylindres",
            "puissance_ch", "puissance_tr_min", "couple_nm", "couple_tr_min",
            "qualite_huile", "quantite_huile_l", "intervalle_km_entretien",
        ]
        # Widgets pour styliser les champs
        widgets = {
            "motoriste": forms.TextInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "code_moteur": forms.TextInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "type_moteur": forms.Select(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "carburant": forms.Select(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "cylindree_l": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "distribution": forms.TextInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "nombre_cylindres": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "puissance_ch": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "puissance_tr_min": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "couple_nm": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "couple_tr_min": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "qualite_huile": forms.TextInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "quantite_huile_l": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
            "intervalle_km_entretien": forms.NumberInput(attrs={"class": "border rounded px-3 py-2 w-full text-sm"}),
        }

    # Optionnel : initialiser les choices pour le template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Passe les TextChoices pour le template si nécessaire
        self.fields['type_moteur'].choices = TypeMoteur.choices
        self.fields['carburant'].choices = TypeCarburant.choices
