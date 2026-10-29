from decimal import Decimal

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import COMPTES_CONTREPARTIE, CompteTresorerie, MouvementTresorerie


class CompteTresorerieForm(forms.ModelForm):
    class Meta:
        model = CompteTresorerie
        fields = ["type", "nom", "compte_pcmn", "banque", "iban", "bic", "date_ouverture",
                  "solde_ouverture", "compte_contrepartie_ouverture", "par_defaut", "actif", "remarques"]
        widgets = {
            "date_ouverture": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "solde_ouverture": forms.NumberInput(attrs={"step": "0.01"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "compte_contrepartie_ouverture": forms.TextInput(attrs={"list": "comptes-pcmn"}),
        }

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")
        if not iban:
            return ""
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(iban) or ""

    def clean(self):
        cleaned = super().clean()
        pcmn = (cleaned.get("compte_pcmn") or "").strip()
        type_ = cleaned.get("type")
        if pcmn:
            if not pcmn.isdigit():
                self.add_error("compte_pcmn", _("Le compte comptable ne contient que des chiffres."))
            elif type_ == CompteTresorerie.Type.CAISSE and not pcmn.startswith("57"):
                self.add_error("compte_pcmn", _("Un compte de caisse commence par 57 (PCMN)."))
            elif type_ == CompteTresorerie.Type.BANQUE and not pcmn.startswith("55"):
                self.add_error("compte_pcmn", _("Un compte bancaire commence par 55 (PCMN)."))
        if type_ == CompteTresorerie.Type.CAISSE and (cleaned.get("solde_ouverture") or Decimal("0")) < 0:
            self.add_error("solde_ouverture", _("Une caisse ne peut pas avoir un solde négatif."))
        return cleaned


class MouvementTresorerieForm(forms.ModelForm):
    class Meta:
        model = MouvementTresorerie
        fields = ["date", "sens", "montant", "libelle", "compte_contrepartie", "piece", "remarques"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "montant": forms.NumberInput(attrs={"step": "0.01", "min": "0.01"}),
            "compte_contrepartie": forms.TextInput(attrs={"list": "comptes-pcmn"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.compte = kwargs.pop("compte")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        if d and d < self.compte.date_ouverture:
            self.add_error("date", _("La date est antérieure à l'ouverture du compte (%(date)s).")
                           % {"date": self.compte.date_ouverture.strftime("%d/%m/%Y")})
        pcmn = (cleaned.get("compte_contrepartie") or "").strip()
        if pcmn and not pcmn.isdigit():
            self.add_error("compte_contrepartie", _("Le compte comptable ne contient que des chiffres."))

        # Une caisse ne peut pas devenir négative
        if (self.compte.type == self.compte.Type.CAISSE and d and cleaned.get("montant")
                and cleaned.get("sens") == MouvementTresorerie.Sens.SORTIE):
            solde = self.compte.solde(au=d)
            if self.instance.pk:
                ancien = self.instance
                if ancien.date <= d:
                    solde += ancien.montant if ancien.sens == ancien.Sens.SORTIE else -ancien.montant
            if cleaned["montant"] > solde:
                self.add_error("montant", _("Solde de caisse insuffisant (%(solde)s € disponibles).")
                               % {"solde": f"{solde:.2f}"})
        return cleaned


class VirementInterneForm(forms.Form):
    compte_source = forms.ModelChoiceField(queryset=CompteTresorerie.objects.none(), label=_("Depuis le compte"))
    compte_destination = forms.ModelChoiceField(queryset=CompteTresorerie.objects.none(), label=_("Vers le compte"))
    date = forms.DateField(label=_("Date"), widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    montant = forms.DecimalField(label=_("Montant"), max_digits=12, decimal_places=2, min_value=Decimal("0.01"))
    libelle = forms.CharField(label=_("Libellé"), max_length=255, required=False,
                              help_text=_("Ex. : dépôt de la caisse en banque, retrait au distributeur…"))

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe")
        super().__init__(*args, **kwargs)
        qs = CompteTresorerie.objects.filter(societe=societe, actif=True)
        self.fields["compte_source"].queryset = qs
        self.fields["compte_destination"].queryset = qs

    def clean(self):
        cleaned = super().clean()
        src, dst, d, montant = (cleaned.get(k) for k in ("compte_source", "compte_destination", "date", "montant"))
        if src and dst and src == dst:
            self.add_error("compte_destination", _("Choisissez deux comptes différents."))
        for compte, champ in ((src, "compte_source"), (dst, "compte_destination")):
            if compte and d and d < compte.date_ouverture:
                self.add_error("date", _("La date est antérieure à l'ouverture du compte %(compte)s.")
                               % {"compte": compte.nom})
        if src and d and montant and src.type == src.Type.CAISSE and montant > src.solde(au=d):
            self.add_error("montant", _("Solde de caisse insuffisant (%(solde)s € disponibles).")
                           % {"solde": f"{src.solde(au=d):.2f}"})
        return cleaned


CHOIX_CONTREPARTIE = COMPTES_CONTREPARTIE
