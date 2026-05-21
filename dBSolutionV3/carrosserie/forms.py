from django import forms
from .models import Carrosserie
from django.utils.translation import gettext_lazy as _



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
            "numero_iban",

        ]

        widgets = {

            # -------------------------
            # SOCIETE
            # -------------------------
            "nom_societe": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Nom de la carrosserie")
            }),

            "numero_tva": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("BE0123456789")
            }),

            "peppol_id": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("0208:0630675588")
            }),

            "email": forms.EmailInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("contact@...")
            }),

            "telephone": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("+32 4 123 45 67")
            }),

            # -------------------------
            # RESPONSABLE
            # -------------------------
            "responsable_nom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Nom du responsable")
            }),

            "responsable_prenom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Prénom du responsable")
            }),

            "numero_iban": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "BE68 5390 0754 7034"
            }),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = False

    def clean_numero_iban(self):
        value = self.cleaned_data.get("numero_iban")

        if not value:
            return value

        return value.replace(" ", "").upper()