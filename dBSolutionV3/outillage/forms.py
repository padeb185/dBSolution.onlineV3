from django import forms
from .models import Outillage
from django.utils.translation import gettext_lazy as _

class OutillageForm(forms.ModelForm):

    class Meta:
        model = Outillage

        fields = [
            "fournisseur",
            "libelle",
            "reference",
            "quantite",
            "prix_htva",
            "taux_tva",
        ]

        labels = {
            "fournisseur": _("Fournisseur"),
            "libelle": _("Libellé"),
            "reference": _("Référence"),
            "quantite": _("Quantité"),
            "prix_htva": _("Prix HTVA"),
            "taux_tva": _("Taux TVA (%)"),
        }

        widgets = {

            # -------------------------
            # FOURNISSEUR
            # -------------------------
            "fournisseur": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            # -------------------------
            # LIBELLÉ
            # -------------------------
            "libelle": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Nom de l'outillage")
            }),

            # -------------------------
            # RÉFÉRENCE
            # -------------------------
            "reference": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Référence produit")
            }),

            # -------------------------
            # QUANTITÉ
            # -------------------------
            "quantite": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Quantité"),
                "min": 1
            }),

            # -------------------------
            # PRIX HTVA
            # -------------------------
            "prix_htva": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "0.00",
                "step": "0.01"
            }),

            # -------------------------
            # TVA
            # -------------------------
            "taux_tva": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "21",
                "step": "0.01"
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Optionnel : texte vide dans select fournisseur
        self.fields["fournisseur"].empty_label = _("Sélectionner un fournisseur")

    def clean_quantite(self):

        quantite = self.cleaned_data.get("quantite")

        if quantite is not None and quantite < 1:
            raise forms.ValidationError(
                _("La quantité doit être au moins égale à 1.")
            )

        return quantite