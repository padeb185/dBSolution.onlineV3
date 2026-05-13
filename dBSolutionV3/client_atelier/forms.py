from adresse.models import Adresse
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ClientAtelier
from adresse.models import Adresse



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


class ClientAtelierForm(forms.ModelForm):

    # -------------------------
    # 🔹 CHAMPS ADRESSE (hors modèle)
    # -------------------------
    rue = forms.CharField(
        required=False,
        label=_("Rue"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    numero = forms.CharField(
        required=False,
        label=_("Numéro"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    code_postal = forms.CharField(
        required=False,
        label=_("Code postal"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    ville = forms.CharField(
        required=False,
        label=_("Ville"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    pays = forms.CharField(
        required=False,
        label=_("Pays"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    code_pays = forms.CharField(
        required=False,
        label=_("Code pays"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm"
        })
    )

    class Meta:
        model = ClientAtelier

        fields = [
            "prenom",
            "nom",
            "societe_cliente",
            "numero_telephone",
            "numero_carte_id",
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "voitures",
            "remarques",
        ]

        labels = {
            "prenom": _("Prénom"),
            "nom": _("Nom"),
            "societe_cliente": _("Société cliente"),
            "numero_telephone": _("Téléphone"),
            "numero_carte_id": _("Carte d'identité"),
            "numero_compte": _("Compte bancaire"),
            "numero_carte_bancaire": _("Carte bancaire"),
            "email": _("Email"),
            "voitures": _("Voitures"),
            "remarques": _("Remarques"),
        }

        widgets = {
            "prenom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Prénom")
            }),

            "nom": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Nom")
            }),

            "societe_cliente": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "numero_telephone": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("+32 ...")
            }),

            "numero_carte_id": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "BE12 3456 7890 1234"
            }),

            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "1234 5678 9012 3456"
            }),

            "email": forms.EmailInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "email@domain.com"
            }),

            "voitures": forms.SelectMultiple(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "rows": 4
            }),
        }

    # -------------------------
    # INIT (remplir adresse)
    # -------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.adresse:
            a = self.instance.adresse
            self.fields["rue"].initial = a.rue
            self.fields["numero"].initial = a.numero
            self.fields["code_postal"].initial = a.code_postal
            self.fields["ville"].initial = a.ville
            self.fields["pays"].initial = a.pays
            self.fields["code_pays"].initial = a.code_pays

    # -------------------------
    # SAVE (gestion adresse propre)
    # -------------------------
    def save(self, commit=True):
        instance = super().save(commit=False)

        adresse = instance.adresse or Adresse()

        adresse.rue = self.cleaned_data.get("rue")
        adresse.numero = self.cleaned_data.get("numero")
        adresse.code_postal = self.cleaned_data.get("code_postal")
        adresse.ville = self.cleaned_data.get("ville")
        adresse.pays = self.cleaned_data.get("pays") or "Belgique"
        adresse.code_pays = self.cleaned_data.get("code_pays") or "BE"

        if commit:
            adresse.save()
            instance.adresse = adresse
            instance.save()
            self.save_m2m()

        return instance


    # -------------------------
    # VALIDATION CARTE
    # ------------------------

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
