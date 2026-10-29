from django import forms
from django.db.models import ExpressionWrapper, DecimalField, F
from django.utils.translation import gettext_lazy as _
from achat_mds.models import AchatMds
from fournisseur.models import Fournisseur
from achat_mds.documents import appliquer_choix_documents


class AchatForm(forms.ModelForm):

    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseur.objects.all(),
        label=_("Fournisseur"),
        widget=forms.Select(attrs={
            "class": "border rounded px-3 py-2 w-full text-sm h-10"
        })
    )

    class Meta:
        model = AchatMds

        fields = [
            "type_document",
            "document_origine",
            "motif",
            "fournisseur",
            "libelle_facture",
            "reference_facture",
            "achat_montant_htva",
            "transport_montant_htva",
            "achat_tva",
            "transport_tva",
            "date_facture",
            "date_paiement",
        ]

        labels = {
            "type_document": _("Type de document"),
            "document_origine": _("Facture d'origine"),
            "motif": _("Motif de la note"),
            "libelle_facture": _("Libellé facture"),
            "reference_facture": _("Référence facture"),
            "achat_montant_htva": _("Montant achat HTVA"),
            "transport_montant_htva": _("Montant transport HTVA"),
            "achat_tva": _("TVA (%)"),
            "transport_tva": _("TVA du transport (%)"),
            "date_facture": _("Date de la facture"),
            "date_paiement": _("Date de paiement"),
        }

        widgets = {
            "type_document": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm h-10",
                "data-type-document": "1",
            }),
            "document_origine": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm h-10",
            }),
            "motif": forms.Textarea(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "rows": 2,
                "placeholder": _("Ex: retour de pièces, erreur de prix, remise accordée…"),
            }),

            # -------------------------
            # TEXTE
            # -------------------------
            "libelle_facture": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex: Achat pièces moteur")
            }),

            "reference_facture": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex: FAC-2026-001")
            }),

            # -------------------------
            # MONTANTS
            # -------------------------
            "achat_montant_htva": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("0.00"),
                "step": "0.01",
                "min": "0"
            }),

            "transport_montant_htva": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("0.00"),
                "step": "0.01",
                "min": "0"
            }),

            "transport_tva": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Même taux que l'achat"),
                "step": "0.01",
                "min": "0"
            }),

            "achat_tva": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("21"),
                "step": "0.01",
                "min": "0"
            }),

            # -------------------------
            # DATES
            # -------------------------
            "date_facture": forms.DateInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "type": "date"
            }),

            "date_paiement": forms.DateInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "type": "date"
            }),
        }

    def __init__(self, *args, societe=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["fournisseur"].queryset = Fournisseur.objects.all().order_by("nom")
        appliquer_choix_documents(self, societe, self.instance)

    def get_queryset(self):
        return super().get_queryset().annotate(

            montant_tva_calc=ExpressionWrapper(
                F("achat_montant_htva") * F("achat_tva") / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),

            montant_tva_transport_calc=ExpressionWrapper(
                F("transport_montant_htva") * F("achat_tva") / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),

            total_tvac_calc=ExpressionWrapper(
                (
                    F("achat_montant_htva") +
                    F("transport_montant_htva")
                ) * (1 + F("achat_tva") / 100),

                output_field=DecimalField(
                    max_digits=10,
                    decimal_places=2
                )
            )
        )