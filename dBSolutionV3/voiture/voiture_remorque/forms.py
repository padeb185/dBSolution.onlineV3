from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Remorque

DATE = {"type": "date"}


class RemorqueForm(forms.ModelForm):
    class Meta:
        model = Remorque
        exclude = ["societe", "created_at", "updated_at"]
        widgets = {
            "date_premiere_immatriculation": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "controle_technique": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "date_achat": forms.DateInput(attrs=DATE, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "immatriculation": forms.TextInput(attrs={"style": "text-transform: uppercase", "autocomplete": "off"}),
        }

    SECTIONS = [
        (_("Identification"), ["immatriculation", "pays", "nom", "marque", "modele", "numero_chassis", "annee",
                               "date_premiere_immatriculation"]),
        (_("Caractéristiques"), ["type_remorque", "essieux", "freinee", "mma_kg", "poids_vide_kg",
                                 "longueur_plateau_cm", "largeur_plateau_cm", "dimension_pneus",
                                 "treuil", "rampes", "roue_jockey"]),
        (_("Administratif"), ["controle_technique", "assurance", "prix_achat", "date_achat", "actif", "remarques"]),
    ]

    def __init__(self, *args, societe=None, **kwargs):
        self.societe = societe
        super().__init__(*args, **kwargs)
        for nom, f in self.fields.items():
            if not isinstance(f.widget, forms.CheckboxInput):
                f.widget.attrs.setdefault("class", "input w-full border rounded px-3 py-2")

    def sections(self):
        return [(titre, [self[n] for n in noms if n in self.fields]) for titre, noms in self.SECTIONS]

    def clean_immatriculation(self):
        immat = (self.cleaned_data.get("immatriculation") or "").upper().strip()
        qs = Remorque.objects.filter(societe=self.societe, immatriculation__iexact=immat)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if immat and qs.exists():
            raise forms.ValidationError(_("Une remorque avec cette immatriculation existe déjà."))
        return immat

    def clean(self):
        c = super().clean()
        mma, vide = c.get("mma_kg"), c.get("poids_vide_kg")
        if mma and vide and vide > mma:
            self.add_error("poids_vide_kg", _("Le poids à vide ne peut pas dépasser la masse maximale autorisée."))
        return c
