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
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
        ]
        labels = {
            "rue": _("Rue"),
            "numero": _("Numéro"),
            "boite": _("Boite"),
            "code_postal": _("Code postal"),
            "ville": _("Ville"),
            "pays": _("Pays"),
            "code_pays": _("Code pays"),
        }

