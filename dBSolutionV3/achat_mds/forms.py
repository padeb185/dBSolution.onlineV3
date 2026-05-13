from django import forms
from django.db.models import ExpressionWrapper, DecimalField, F
from django.utils.translation import gettext_lazy as _
from achat_mds.models import AchatMds
from fournisseur.models import Fournisseur


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
            "fournisseur",
            "libelle_facture",
            "reference_facture",
            "achat_montant_htva",
            "transport_montant_htva",
            "achat_tva",
            "date_facture",
            "date_paiement",
        ]

        labels = {
            "libelle_facture": _("Libellé facture"),
            "reference_facture": _("Référence facture"),
            "achat_montant_htva": _("Montant achat HTVA"),
            "transport_montant_htva": _("Montant transport HTVA"),
            "achat_tva": _("TVA (%)"),
            "date_facture": _("Date facture"),
            "date_paiement": _("Date paiement"),
        }

        widgets = {

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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["fournisseur"].queryset = Fournisseur.objects.all().order_by("nom")

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