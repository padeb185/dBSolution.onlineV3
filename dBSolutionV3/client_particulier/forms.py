from django import forms
from .models import ClientParticulier


class ClientParticulierForm(forms.ModelForm):
    class Meta:
        model = ClientParticulier
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