from stdnum import iban
from django import forms
from django.utils.translation import gettext_lazy as _
from client_particulier.forms import luhn_check
from .models import ClientAtelier






class ClientAtelierForm(forms.ModelForm):
    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    email = forms.EmailField(required=False)

    numero_telephone = forms.CharField(
        required=False,
        label = _("Numéro de téléphone"),
        widget = forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
                                       )
    numero_carte_id = forms.CharField(
        required=False,
        label = _("Numéro de carte bancaire"),
        widget = forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
        )

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
    boite = forms.CharField(
        required=False,
        label=_("Boîte"),
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
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234 56"
            }),

            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "5389 3456 7890 1234"
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

        if self.instance and self.instance.pk:

            cp = self.instance.client_particulier

            if cp:
                self.fields["prenom"].initial = cp.prenom
                self.fields["nom"].initial = cp.nom
                self.fields["email"].initial = cp.email
                self.fields["numero_telephone"].initial = cp.numero_telephone
                self.fields["numero_carte_id"].initial = cp.numero_carte_id
                self.fields["numero_compte"].initial = cp.numero_compte
                self.fields["numero_carte_bancaire"].initial = cp.numero_carte_bancaire

                if cp.date_naissance:
                    self.fields["date_naissance"].initial = cp.date_naissance.strftime("%Y-%m-%d")

                if "age" in self.fields:
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