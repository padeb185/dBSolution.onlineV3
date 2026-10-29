from django import forms
from .models import Outillage
from django.utils.translation import gettext_lazy as _
from achat_mds.documents import appliquer_choix_documents

class OutillageForm(forms.ModelForm):

    class Meta:
        model = Outillage

        fields = [
            "type_document",
            "document_origine",
            "motif",
            "fournisseur",
            "libelle",
            "reference",
            "quantite",
            "prix_htva",
            "taux_tva",
            "transport_montant_htva",
            "transport_tva",
            "reference_facture",
            "date_facture",
            "date_paiement",
        ]

        labels = {
            "type_document": _("Type de document"),
            "document_origine": _("Facture d'origine"),
            "motif": _("Motif de la note"),
            "fournisseur": _("Fournisseur"),
            "libelle": _("Libellé"),
            "reference": _("Référence"),
            "quantite": _("Quantité"),
            "prix_htva": _("Prix HTVA"),
            "taux_tva": _("Taux TVA (%)"),
            "date_facture": _("Date de la facture"),
            "reference_facture": _("Référence facture"),
            "transport_montant_htva": _("Montant transport HTVA"),
            "transport_tva": _("TVA du transport (%)"),
            "date_paiement": _("Date de paiement"),
        }

        widgets = {
            "type_document": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "data-type-document": "1",
            }),
            "document_origine": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full",
            }),
            "motif": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 2,
                "placeholder": _("Ex: retour d'outillage, erreur de prix, remise accordée…"),
            }),

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

            # -------------------------
            # FACTURE FOURNISSEUR (comme les achats MDS)
            # -------------------------
            "reference_facture": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": _("Ex: FAC-2026-001")
            }),
            "transport_montant_htva": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full", "placeholder": "0.00", "step": "0.01", "min": "0"
            }),
            "transport_tva": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full", "placeholder": _("Même taux que l'achat"), "step": "0.01", "min": "0"
            }),
            "date_paiement": forms.DateInput(format="%Y-%m-%d", attrs={
                "class": "border rounded px-4 py-2 w-full", "type": "date"
            }),

            # -------------------------
            # DATE DE FACTURE
            # -------------------------
            "date_facture": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "class": "border rounded px-4 py-2 w-full",
                    "type": "date"
                }
            ),
        }

    def __init__(self, *args, societe=None, **kwargs):

        super().__init__(*args, **kwargs)

        appliquer_choix_documents(self, societe, self.instance)

        # Optionnel : texte vide dans select fournisseur
        self.fields["fournisseur"].empty_label = _("Sélectionner un fournisseur")

    def clean_quantite(self):

        quantite = self.cleaned_data.get("quantite")

        if quantite is not None and quantite < 1:
            raise forms.ValidationError(
                _("La quantité doit être au moins égale à 1.")
            )

        return quantite