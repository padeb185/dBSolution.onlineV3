from django import forms
from django.db.models import ExpressionWrapper, DecimalField, F
from achat_mds.models import AchatMds
from fournisseur.models import Fournisseur




class AchatForm(forms.ModelForm):

    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all())


    class Meta:
        model = AchatMds
        fields = [
            "fournisseur",
            "libelle_facture",
            "reference_facture",
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