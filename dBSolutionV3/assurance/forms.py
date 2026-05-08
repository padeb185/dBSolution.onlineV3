from django import forms
from .models import Assurance
from django.utils.translation import gettext_lazy as _



class AssuranceForm(forms.ModelForm):

    # -------------------------
    # CHAMPS ADRESSE (FK)
    # -------------------------
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
        model = Assurance

        fields = [
            # -------------------------
            # ASSURANCE
            # -------------------------
            "nom_compagnie",
            "peppol_id",
            "email",
            "telephone",
            "courtier_nom",
            "courtier_prenom",

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
            # COMPAGNIE
            # -------------------------
            "nom_compagnie": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Nom de l'assurance")
            }),


            "peppol_id": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "0208:BE0123456789"
            }),

            # -------------------------
            # CONTACT
            # -------------------------
            "email": forms.EmailInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("contact@assurance.be")
            }),

            "telephone": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("+32 4 123 45 67")
            }),

            # -------------------------
            # RESPONSABLE
            # -------------------------
            "courtier_nom": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Nom du courtier")
            }),

            "courtier_prenom": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Prénom du courtier")
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # -------------------------
        # LABELS
        # -------------------------
        self.fields["nom_compagnie"].label = _("Compagnie")
        self.fields["peppol_id"].label = _("Peppol ID")
        self.fields["telephone"].label = _("Téléphone")
        self.fields["courtier_nom"].label = _("Nom du courier")
        self.fields["courtier_prenom"].label = _("Prénom du courtier")

        # -------------------------
        # SI MODIFICATION
        # -------------------------
        if self.instance and self.instance.adresse:

            self.fields["rue"].initial = self.instance.adresse.rue
            self.fields["numero"].initial = self.instance.adresse.numero
            self.fields["boite"].initial = self.instance.adresse.boite
            self.fields["code_postal"].initial = self.instance.adresse.code_postal
            self.fields["ville"].initial = self.instance.adresse.ville
            self.fields["pays"].initial = self.instance.adresse.pays
            self.fields["code_pays"].initial = self.instance.adresse.code_pays
