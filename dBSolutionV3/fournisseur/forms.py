from django import forms
from stdnum import iban

from .models import Fournisseur
from achat_mds.models import AchatMds
from django.utils.translation import gettext_lazy as _



class FournisseurForm(forms.ModelForm):
    rue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Rue")
        })
    )

    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Numéro")
        })
    )
    boite = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Boite")
        })
    )

    code_postal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Code postal")
        })
    )

    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Ville")
        })
    )

    pays = forms.CharField(
        required=False,
        initial=_("Belgique"),
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Pays")
        })
    )

    code_pays = forms.CharField(
        required=False,
        initial="BE",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("Code pays")
        })
    )

    class Meta:
        model = Fournisseur
        fields = [
            # -------------------------
            # FOURNISSEUR
            # -------------------------
            "nom",
            "numero_tva",
            "peppol_id",
            "email",
            "telephone_fixe",
            "gsm",
            "numero_compte",

            # -------------------------
            # ADRESSE
            # -------------------------
            "rue",
            "numero",
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
        ]


        widgets = {

            # -------------------------
            # FOURNISSEUR
            # -------------------------
            "fournisseur": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "Nom du fournisseur"
            }),

            # -------------------------
            # TVA
            # -------------------------
            "numero_tva": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE0123456789"
            }),

            # -------------------------
            # PEPPOL
            # -------------------------
            "peppol_id": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "0208:0630675588"
            }),

            # -------------------------
            # EMAIL
            # -------------------------
            "email": forms.EmailInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "contact@fournisseur.be"
            }),

            # -------------------------
            # TELEPHONE / GSM
            # -------------------------
            "gsm": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "+32 4 123 45 67"
            }),

            "telephone_fixe": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "+32 2 123 45 67"
            }),

            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234"
            }),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            cp = self.instance

            self.fields["nom"].initial = cp.nom
            self.fields["numero_tva"].initial = cp.numero_tva
            self.fields["peppol_id"].initial = cp.peppol_id
            self.fields["email"].initial = cp.email
            self.fields["telephone_fixe"].initial = cp.telephone_fixe
            self.fields["gsm"].initial = cp.gsm
            self.fields["numero_compte"].initial = cp.numero_compte

            if hasattr(self.instance, "adresse"):
                adresse = self.instance.adresse

                self.fields["rue"].initial = adresse.rue
                self.fields["numero"].initial = adresse.numero
                self.fields["boite"].initial = adresse.boite
                self.fields["code_postal"].initial = adresse.code_postal
                self.fields["ville"].initial = adresse.ville
                self.fields["pays"].initial = adresse.pays
                self.fields["code_pays"].initial = adresse.code_pays

        for field in self.fields.values():
            field.help_text = None

            if "placeholder" in field.widget.attrs:
                field.widget.attrs.pop("placeholder")


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