from django import forms
from ..voiture_pneus.models import VoiturePneus



class VoiturePneusForm(forms.ModelForm):

    class Meta:
        model = VoiturePneus
        exclude = ["societe",
                   "voitures_exemplaires",
                   "voitures_modeles",
                   "kilometre_pneus_av",
                   "kilometre_pneus_ar",
                   "date_remplacement",
                   "kilometre_remplacement",
                   "nombre_trains_av",
                   "nombre_trains_ar",
                   "remarques",

                   ]

        widgets = {

            # -------------------------
            # TEXTE
            # -------------------------
            "manufacturier": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Ex: Michelin"
            }),

            "nom_type": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Nom du pneu"
            }),

            "numero_oem": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Numéro OEM"
            }),

            # -------------------------
            # DIMENSIONS
            # -------------------------
            "pneus_largeur": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Ex: 205"
            }),

            "pneus_hauteur": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Ex: 55"
            }),

            "pneus_jante": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Ex: 16"
            }),

            # -------------------------
            # SELECTS
            # -------------------------
            "emplacement": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full"
            }),

            "type_pneus": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full"
            }),

            "indice_vitesse": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full"
            }),

            "indice_charge": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # si tu utilises TextChoices
        self.fields["emplacement"].choices = VoiturePneus.EmplacementPneus.choices
        self.fields["type_pneus"].choices = VoiturePneus.TypePneus.choices
        self.fields["indice_vitesse"].choices = VoiturePneus.IndiceVitesse.choices
        self.fields["indice_charge"].choices = VoiturePneus.IndiceCharge.choices