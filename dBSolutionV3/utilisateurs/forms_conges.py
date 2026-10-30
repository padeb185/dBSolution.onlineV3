from django import forms
from django.utils.translation import gettext_lazy as _

from compta.models import CompteTresorerie, PaiementConges

DATE = {"type": "date"}
NOMBRE = {"step": "0.01", "min": "0"}


class PaiementCongesForm(forms.ModelForm):
    class Meta:
        model = PaiementConges
        fields = ["type", "annee", "date", "jours", "brut", "onss", "precompte", "cotisations_patronales",
                  "date_paiement", "compte_paiement", "remarques"]
        widgets = {
            "date": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_paiement": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "jours": forms.NumberInput(attrs={"step": "0.5", "min": "0"}),
            "brut": forms.NumberInput(attrs=NOMBRE),
            "onss": forms.NumberInput(attrs=NOMBRE),
            "precompte": forms.NumberInput(attrs=NOMBRE),
            "cotisations_patronales": forms.NumberInput(attrs=NOMBRE),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["compte_paiement"].queryset = (
            CompteTresorerie.objects.filter(societe=societe, actif=True) if societe is not None
            else CompteTresorerie.objects.none())
        self.fields["compte_paiement"].empty_label = _("Compte bancaire par défaut")
        for nom, f in self.fields.items():
            if not isinstance(f.widget, (forms.CheckboxInput,)):
                f.widget.attrs.setdefault("class", "input w-full")

    def clean(self):
        c = super().clean()
        brut = c.get("brut") or 0
        if brut <= 0:
            self.add_error("brut", _("Indiquez le montant brut (bouton « Calculer » pour une proposition)."))
        if brut and (c.get("onss") or 0) + (c.get("precompte") or 0) > brut:
            self.add_error("precompte", _("Les retenues dépassent le montant brut."))
        return c
