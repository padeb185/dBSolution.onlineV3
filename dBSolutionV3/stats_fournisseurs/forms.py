from django import forms
from django.utils.translation import gettext_lazy as _
from .models import StatsFournisseur


class StatsFournisseurForm(forms.ModelForm):
    """
    Formulaire de filtrage / consultation des statistiques fournisseur
    """

    annee = forms.IntegerField(
        label=_("Année"),
        required=False,
        min_value=2000,
        max_value=2100,
        widget=forms.NumberInput(attrs={
            "class": "border rounded px-4 py-2 w-full",
            "placeholder": _("2026")
        })
    )

    mois = forms.ChoiceField(
        label=_("Mois"),
        required=False,
        choices=[
            ("", _("Tous les mois")),
            (1, _("Janvier")),
            (2, _("Février")),
            (3, _("Mars")),
            (4, _("Avril")),
            (5, _("Mai")),
            (6, _("Juin")),
            (7, _("Juillet")),
            (8, _("Août")),
            (9, _("Septembre")),
            (10, _("Octobre")),
            (11, _("Novembre")),
            (12, _("Décembre")),
        ],
        widget=forms.Select(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    class Meta:
        model = StatsFournisseur
        fields = [
            "fournisseur",
        ]

        widgets = {
            "fournisseur": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),
        }

        labels = {
            "fournisseur": _("Fournisseur"),
        }

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe", None)
        super().__init__(*args, **kwargs)

        if societe:
            self.fields["fournisseur"].queryset = (
                self.fields["fournisseur"]
                .queryset
                .filter(societe=societe)
                .order_by("nom")
            )