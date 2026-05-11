from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ClientPilotage
from societe_cliente.models import SocieteCliente


class ClientPilotageForm(forms.ModelForm):

    # champs ClientParticulier (manuel)
    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    societe_cliente = forms.ModelChoiceField(
        queryset=SocieteCliente.objects.all(),
        label=_("Société cliente"),
        widget=forms.Select(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    email = forms.EmailField(required=False)

    numero_telephone = forms.CharField(required=False)
    numero_carte_id = forms.CharField(required=False)
    numero_compte = forms.CharField(required=False)
    numero_carte_bancaire = forms.CharField(required=False)

    class Meta:
        model = ClientPilotage

        fields = [
            "historique",
            "niveau",
        ]

        widgets = {
            "voitures": forms.SelectMultiple(attrs={
                "class": "border rounded px-4 py-2 w-full",
            }),

            "historique": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 4,
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 4,
            }),
        }