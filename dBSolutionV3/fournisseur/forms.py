
from django import forms
from django.db.models import ExpressionWrapper, DecimalField, F

from .models import Fournisseur, Achat


class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = "__all__"
        exclude = ("is_active", "societe",)
        widgets = {
            "peppol_id": forms.TextInput(attrs={
                "placeholder": "0208:BE0123456789"
            }),
            "country_code": forms.TextInput(attrs={
                "placeholder": "BE"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "contact@fournisseur.be"
            }),
            "telephone_fixe": forms.TextInput(attrs={
                "placeholder": "+32 2 123 45 67"
            }),
            "gsm": forms.TextInput(attrs={
                "placeholder": "+32 4 123 45 67"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👉 SI on est en modification
        if self.instance and self.instance.pk:
            for field in self.fields.values():
                # Supprimer les help_text
                field.help_text = None

                # Supprimer les placeholders
                if "placeholder" in field.widget.attrs:
                    field.widget.attrs.pop("placeholder")



class AchatForm(forms.ModelForm):

    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all())


    class Meta:
        model = Achat
        fields = [
            "fournisseur",
            "achat_montant_htva",
            "achat_tva",
            "date_facture",
            "date_paiement",
        ]

    def get_queryset(self):
        return super().get_queryset().annotate(
            montant_tva_calc=ExpressionWrapper(
                F("achat_montant_htva") * F("achat_tva") / 100,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            total_tvac_calc=ExpressionWrapper(
                F("achat_montant_htva") + (
                        F("achat_montant_htva") * F("achat_tva") / 100
                ),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )