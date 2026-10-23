from django import forms
from django.utils.translation import gettext_lazy as _

from .models import (COMPTES_IMMOBILISATIONS, CategorieImmobilisation, CompteTresorerie, Immobilisation,
                     ValorisationStock, VersementSocial)

DATE = {"type": "date"}
NOMBRE = {"step": "0.01", "min": "0"}


class _ComptesMixin:
    def _comptes(self, societe):
        if "compte_paiement" in self.fields:
            self.fields["compte_paiement"].queryset = CompteTresorerie.objects.filter(societe=societe, actif=True) \
                if societe is not None else CompteTresorerie.objects.none()
            self.fields["compte_paiement"].empty_label = _("Compte bancaire par défaut")


class ImmobilisationForm(_ComptesMixin, forms.ModelForm):
    class Meta:
        model = Immobilisation
        fields = ["categorie", "libelle", "fournisseur", "reference_facture", "immatriculation",
                  "date_acquisition", "date_mise_en_service", "valeur_acquisition", "frais_accessoires",
                  "taux_tva", "tva_deductible", "valeur_residuelle", "methode", "duree_annees", "prorata_temporis",
                  "date_paiement", "compte_paiement", "date_cession", "prix_cession", "remarques"]
        widgets = {
            "date_acquisition": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_mise_en_service": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_paiement": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_cession": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "valeur_acquisition": forms.NumberInput(attrs=NOMBRE),
            "frais_accessoires": forms.NumberInput(attrs=NOMBRE),
            "taux_tva": forms.NumberInput(attrs=NOMBRE),
            "tva_deductible": forms.NumberInput(attrs=NOMBRE),
            "valeur_residuelle": forms.NumberInput(attrs=NOMBRE),
            "prix_cession": forms.NumberInput(attrs=NOMBRE),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._comptes(societe)
        if "fournisseur" in self.fields:
            from fournisseur.models import Fournisseur
            qs = Fournisseur.objects.all()
            if societe is not None:
                qs = qs.filter(societe=societe) | Fournisseur.objects.filter(societe__isnull=True)
            self.fields["fournisseur"].queryset = qs.order_by("nom")
            self.fields["fournisseur"].required = False

    def clean(self):
        cleaned = super().clean()
        cat = cleaned.get("categorie")
        if cat == CategorieImmobilisation.TERRAIN:
            cleaned["duree_annees"] = 0
        elif not cleaned.get("duree_annees"):
            cleaned["duree_annees"] = COMPTES_IMMOBILISATIONS.get(cat, (None, None, 5))[2] or 5
        if cleaned.get("date_cession") and cleaned.get("date_acquisition") and cleaned["date_cession"] < cleaned["date_acquisition"]:
            self.add_error("date_cession", _("La cession ne peut pas précéder l'acquisition."))
        if (cleaned.get("valeur_residuelle") or 0) > (cleaned.get("valeur_acquisition") or 0) + (cleaned.get("frais_accessoires") or 0):
            self.add_error("valeur_residuelle", _("La valeur résiduelle dépasse la valeur d'acquisition."))
        return cleaned


class ValorisationStockForm(forms.ModelForm):
    class Meta:
        model = ValorisationStock
        fields = ["date", "valeur_pieces", "valeur_autres", "remarques"]
        widgets = {
            "date": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "valeur_pieces": forms.NumberInput(attrs=NOMBRE),
            "valeur_autres": forms.NumberInput(attrs=NOMBRE),
            "remarques": forms.Textarea(attrs={"rows": 2}),
        }


class VersementSocialForm(_ComptesMixin, forms.ModelForm):
    class Meta:
        model = VersementSocial
        fields = ["type", "periode", "date", "montant", "compte_paiement", "reference"]
        widgets = {
            "date": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "montant": forms.NumberInput(attrs=NOMBRE),
        }

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._comptes(societe)
