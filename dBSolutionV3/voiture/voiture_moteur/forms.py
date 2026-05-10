from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (
    MoteurVoiture,
    TypeMoteur,
    TypeCarburant
)


class MoteurVoitureForm(forms.ModelForm):

    class Meta:
        model = MoteurVoiture
        exclude = ("voitures_modeles",
                   "voitures_exemplaires",
                   "boite",
                   "kilometres_chassis",
                   "numero_moteurs",
                   )

        labels = {
            "motoriste": _("Motoriste"),
            "code_moteur": _("Code moteur"),
            "distribution": _("Distribution"),
            "qualite_huile": _("Qualité huile"),

            "type_moteur": _("Type moteur"),
            "carburant": _("Carburant"),

            "cylindree_l": _("Cylindrée (L)"),
            "nombre_cylindres": _("Nombre de cylindres"),
            "puissance_ch": _("Puissance (ch)"),
            "puissance_tr_min": _("Régime puissance (tr/min)"),
            "couple_nm": _("Couple (Nm)"),
            "couple_tr_min": _("Régime couple (tr/min)"),
            "quantite_huile_l": _("Quantité d'huile (L)"),
            "intervalle_km_entretien": _("Intervalle entretien (km)"),
        }

        widgets = {

            # -------------------------
            # TEXTE
            # -------------------------
            "motoriste": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Nom du motoriste")
            }),

            "code_moteur": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex: S14B23")
            }),

            "distribution": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Chaîne ou courroie")
            }),

            "qualite_huile": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("0W30")
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
                "placeholder": _("Ex: 2.3"),
                "step": "0.01"
            }),

            "nombre_cylindres": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex: 4"),
                "min": "1"
            }),

            "puissance_ch": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("120")
            }),

            "puissance_tr_min": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("3000")
            }),

            "couple_nm": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("300")
            }),

            "couple_tr_min": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("4000")
            }),

            "quantite_huile_l": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("6.50"),
                "step": "0.01",
                "min": "0"
            }),

            "intervalle_km_entretien": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("10000")
            }),
            'remarques': forms.Textarea(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["type_moteur"].choices = TypeMoteur.choices
        self.fields["carburant"].choices = TypeCarburant.choices