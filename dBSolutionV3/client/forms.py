from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "prenom",
            "nom",
            "adresse",
            "numero_telephone",
            "numero_permis",
            "numero_carte_id",
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "date_naissance",
            "niveau",
            "historique",
            "location",
        ]