from django import forms
from django.utils.translation import gettext_lazy as _
from stdnum import iban

from .models import ClientParticulier



def luhn_check(card_number: str) -> bool:
    """Vérifie si un numéro de carte est valide selon Luhn"""
    # Nettoyage
    card_number = card_number.replace(" ", "").replace("-", "")
    if not card_number.isdigit() or len(card_number) < 12:
        return False

    digits = [int(d) for d in card_number]
    check_digit = digits.pop()
    digits.reverse()

    for i in range(len(digits)):
        if i % 2 == 0:
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

    total = sum(digits) + check_digit
    return total % 10 == 0


class ClientParticulierForm(forms.ModelForm):


    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )


    email = forms.EmailField(required=False)

    numero_telephone = forms.CharField(required=False)
    numero_carte_id = forms.CharField(required=False)

    numero_compte = forms.CharField(
        required=False,
        label=_("Numéro de compte bancaire"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": "BE12 3456 7890 1234 56"
        })
    )

    numero_carte_bancaire = forms.CharField(
        required=False,
        label=_("Numéro de carte bancaire"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": "5389 3456 7890 1234"
        })
    )

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
        label="Âge",
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
        model = ClientParticulier
        fields = [
            "prenom",
            "nom",
            "numero_telephone",
            "numero_permis",
            "numero_carte_id",
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "date_naissance",
            "age",
            "rue",
            "numero",
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
            "remarques",
        ]

        widgets = {
            "prenom": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "nom": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "numero_telephone": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "numero_permis": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "numero_carte_id": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),

            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234 56"
            }),

            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "5389 3456 7890 1234"
            }),

            "email": forms.EmailInput(attrs={"class": "border rounded px-4 py-2 w-full"}),

            "date_naissance": forms.DateInput(
                attrs={"type": "date", "class": "border rounded px-4 py-2 w-full"}
            ),

            "rue": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "numero": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "code_postal": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "ville": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),

            "pays": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),
            "code_pays": forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"}),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            cp = self.instance.client_particulier

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