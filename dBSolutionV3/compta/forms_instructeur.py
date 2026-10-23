from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CompteTresorerie, FactureInstructeur, ProfilInstructeur, RegimeTVAInstructeur

DATE = {"type": "date"}


class ProfilInstructeurForm(forms.ModelForm):
    class Meta:
        model = ProfilInstructeur
        fields = ["nom_commercial", "numero_entreprise", "regime_tva", "taux_tva", "tarif_horaire_htva",
                  "iban", "delai_paiement_jours", "accord_autofacturation", "date_accord_autofacturation", "remarques"]
        widgets = {
            "date_accord_autofacturation": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "taux_tva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "tarif_horaire_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_iban(self):
        iban = self.cleaned_data.get("iban")
        if not iban:
            return ""
        try:
            from core.iban import nettoyer_iban_formulaire
            return nettoyer_iban_formulaire(iban) or ""
        except ImportError:
            return iban.replace(" ", "").upper()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("accord_autofacturation") and not cleaned.get("date_accord_autofacturation"):
            self.add_error("date_accord_autofacturation",
                           _("Indiquez la date de l'accord écrit d'autofacturation."))
        if cleaned.get("regime_tva") == RegimeTVAInstructeur.ASSUJETTI and not cleaned.get("taux_tva"):
            self.add_error("taux_tva", _("Indiquez le taux de TVA de l'instructeur."))
        return cleaned


class FactureInstructeurForm(forms.ModelForm):
    class Meta:
        model = FactureInstructeur
        fields = ["autofacturation", "reference_instructeur", "date_facture", "periode_debut", "periode_fin",
                  "date_echeance", "remarques"]
        widgets = {
            "date_facture": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "periode_debut": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "periode_fin": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_echeance": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, profil=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.profil = profil
        if profil is None or not profil.autofacturation_possible:
            self.fields["autofacturation"].help_text = _(
                "Autofacturation indisponible : complétez le profil de l'instructeur "
                "(numéro d'entreprise, accord écrit et sa date)."
            )

    def clean(self):
        cleaned = super().clean()
        debut, fin = cleaned.get("periode_debut"), cleaned.get("periode_fin")
        if debut and fin and fin < debut:
            self.add_error("periode_fin", _("La fin de période doit être postérieure au début."))
        if cleaned.get("autofacturation") and (self.profil is None or not self.profil.autofacturation_possible):
            self.add_error("autofacturation", _("Pas d'accord d'autofacturation enregistré pour cet instructeur."))
        return cleaned


class PaiementFactureInstructeurForm(forms.Form):
    date_paiement = forms.DateField(label=_("Date du paiement"),
                                    widget=forms.DateInput(attrs=DATE, format="%Y-%m-%d"))
    compte_paiement = forms.ModelChoiceField(
        label=_("Payée depuis le compte"), queryset=CompteTresorerie.objects.none(), required=False,
        empty_label=_("Compte bancaire par défaut"),
    )

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        if societe is not None:
            self.fields["compte_paiement"].queryset = CompteTresorerie.objects.filter(societe=societe, actif=True)
