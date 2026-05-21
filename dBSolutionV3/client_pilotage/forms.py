from django import forms
from django.utils.translation import gettext_lazy as _
from stdnum.be import iban

from client_particulier.forms import luhn_check
from .models import ClientPilotage
from societe_cliente.models import SocieteCliente


class ClientPilotageForm(forms.ModelForm):

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
        widget=forms.Select(attrs={"class": "border rounded px-4 py-2 w-full"}),
        required=False,
    )

    email = forms.EmailField(required=False)

    numero_telephone = forms.CharField(required=False)
    numero_carte_id = forms.CharField(required=False)
    numero_compte = forms.CharField(required=False)
    numero_carte_bancaire = forms.CharField(required=False)

    date_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "border rounded px-4 py-2 w-full",
            }
        )
    )

    age = forms.IntegerField(
        label=_("Âge"),
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={
            "class": "border rounded px-4 py-2 w-full bg-gray-100"
        })
    )


    rue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    boite = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_postal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    pays = forms.CharField(
        required=False,
        initial="Belgique",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_pays = forms.CharField(
        required=False,
        initial="BE",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    class Meta:
        model = ClientPilotage
        fields = ["historique", "niveau"]
        widgets = {
            "niveau": forms.Select(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "historique": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            cp = self.instance.client_pilotage

            self.fields["prenom"].initial = cp.prenom
            self.fields["nom"].initial = cp.nom
            self.fields["email"].initial = cp.email
            self.fields["numero_telephone"].initial = cp.numero_telephone
            self.fields["numero_carte_id"].initial = cp.numero_carte_id
            self.fields["numero_compte"].initial = cp.numero_compte
            self.fields["numero_carte_bancaire"].initial = cp.numero_carte_bancaire
            self.fields["date_naissance"].initial = cp.date_naissance
            self.fields["age"].initial = cp.age

            if self.instance.adresse:
                adresse = self.instance.adresse

                self.fields["rue"].initial = adresse.rue
                self.fields["numero"].initial = adresse.numero
                self.fields["boite"].initial = adresse.boite
                self.fields["code_postal"].initial = adresse.code_postal
                self.fields["ville"].initial = adresse.ville
                self.fields["pays"].initial = adresse.pays
                self.fields["code_pays"].initial = adresse.code_pays

            # 👉 ordre FINAL du formulaire

            ordered_fields = [
                "prenom",
                "nom",
                "date_naissance",
                "age",
                "societe_cliente",
                "email",
                "numero_telephone",
                "numero_carte_id",
                "numero_compte",
                "numero_carte_bancaire",
                "rue",
                "numero",
                "boite",
                "code_postal",
                "ville",
                "pays",
                "code_pays",

                # EN BAS
                "niveau",
                "historique",
            ]

            self.fields = {
                field: self.fields[field]
                for field in ordered_fields
                if field in self.fields
            }

    def clean_numero_carte_bancaire(self):
        value = self.cleaned_data.get("numero_carte_bancaire")

        if not value:
            return None

        value = str(value).replace(" ", "").replace("-", "")

        if not value.isdigit():
            raise forms.ValidationError("Numéro de carte invalide")

        if not luhn_check(value):
            raise forms.ValidationError("Numéro de carte invalide (Luhn)")

        return value

    def clean_numero_compte(self):
        value = self.cleaned_data.get("numero_compte")

        if not value:
            return None

        # nettoyage
        value = value.replace(" ", "").upper()

        # validation IBAN
        if not iban.is_valid(value):
            raise forms.ValidationError(
                _("Numéro de compte IBAN invalide")
            )

        return value