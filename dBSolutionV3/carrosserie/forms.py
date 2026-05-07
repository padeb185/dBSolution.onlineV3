from django import forms
from .models import Carrosserie


from django import forms
from .models import Carrosserie


class CarrosserieForm(forms.ModelForm):

    class Meta:
        model = Carrosserie
        fields = [
            "nom_societe",
            "responsable_nom",
            "responsable_prenom",
            "numero_tva",
            "peppol_id",
            "email",
            "telephone",

        ]

        widgets = {

            # -------------------------
            # SOCIETE
            # -------------------------
            "nom_societe": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Nom de la carrosserie"
            }),

            "numero_tva": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "BE0123456789"
            }),

            "peppol_id": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "0208:0630675588"
            }),

            "email": forms.EmailInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "contact@carrosserie.be"
            }),

            "telephone": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "+32 4 123 45 67"
            }),

            # -------------------------
            # RESPONSABLE
            # -------------------------
            "responsable_nom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Nom du responsable"
            }),

            "responsable_prenom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Prénom du responsable"
            }),


        }