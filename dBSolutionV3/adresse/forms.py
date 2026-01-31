# adresse/forms.py
from django import forms
from .models import Adresse
from django.utils.translation import gettext_lazy as _

class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = [
            "rue",
            "numero",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
        ]
        labels = {
            "rue": _("Rue"),
            "numero": _("Numéro"),
            "code_postal": _("Code postal"),
            "ville": _("Ville"),
            "pays": _("Pays"),
            "code_pays": _("Code pays"),
        }
        widgets = {
            "rue": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "numero": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "code_postal": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "ville": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "pays": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "code_pays": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
        }
