from django import forms
from .models import ClientPilotage
from django.utils.translation import gettext_lazy as _


class ClientPilotageForm(forms.ModelForm):
    class Meta:
        model = ClientPilotage
        fields = [
            "client_particulier",
            "niveau",
            "historique",

        ]
        widgets = {
            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "5389 3456 7890 1234"
            }),
            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234 56"  # exemple format belge
            }),

        }
