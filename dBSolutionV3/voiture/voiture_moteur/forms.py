from django import forms
from .models import (
    MoteurVoiture,
    TypeMoteur,
    TypeCarburant
)


class MoteurVoitureForm(forms.ModelForm):

    class Meta:
        model = MoteurVoiture

        fields = [
            "motoriste",
            "code_moteur",
            "type_moteur",
            "carburant",
            "cylindree_l",
            "distribution",
            "nombre_cylindres",
            "puissance_ch",
            "puissance_tr_min",
            "couple_nm",
            "couple_tr_min",
            "qualite_huile",
            "quantite_huile_l",
            "intervalle_km_entretien",
        ]

        widgets = {

            # -------------------------
            # TEXTE
            # -------------------------
            "motoriste": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Nom du motoriste"
            }),

            "code_moteur": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: S14B23"
            }),

            "distribution": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Chaîne ou courroie"
            }),

            "qualite_huile": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "0W30"
            }),

            # -------------------------
            # SELECT
            # -------------------------
            "type_moteur": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm h-10"
            }),

            "carburant": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm h-10"
            }),

            # -------------------------
            # NUMBERS
            # -------------------------
            "cylindree_l": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: 2.3",
                "step": "0.01"
            }),

            "nombre_cylindres": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: 4",
                "min": "1"
            }),

            "puissance_ch": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "120"
            }),

            "puissance_tr_min": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "3000"
            }),

            "couple_nm": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "300"
            }),

            "couple_tr_min": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "4000"
            }),

            "quantite_huile_l": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "6.50",
                "step": "0.01",
                "min": "0"
            }),

            "intervalle_km_entretien": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "10000"
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["type_moteur"].choices = TypeMoteur.choices
        self.fields["carburant"].choices = TypeCarburant.choices