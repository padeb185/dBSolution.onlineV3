from django import forms
from .models import VoitureExemplaire
from .utils_vin import get_vin_year

# Lettres interdites dans un VIN
INVALID_VIN_CHARS = set("IOQ")


class VoitureExemplaireForm(forms.ModelForm):
    class Meta:
        model = VoitureExemplaire
        fields = (
            "voiture_marque",
            "voiture_modele",
            "immatriculation",
            "pays",
            "numero_vin",
            "type_utilisation",
            "kilometres_chassis",
            "kilometres_moteur",
            "kilometres_derniere_intervention",
            "mois_production",
            "date_mise_en_circulation",
            "est_avant_2010",
        )

        widgets = {
            "numero_vin": forms.TextInput(attrs={
                "maxlength": 17,
                "style": "text-transform:uppercase",
                "class": "input"
            }),
            "type_utilisation": forms.Select(attrs={"class": "input"}),
            "date_mise_en_circulation": forms.DateInput(attrs={
                "type": "date",
                "class": "input"
            }),
            "est_avant_2010": forms.CheckboxInput(attrs={"class": "mt-2"}),
        }

    def __init__(self, *args, **kwargs):
        # Récupère l'utilisateur depuis la vue
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_numero_vin(self):
        vin = self.cleaned_data.get("numero_vin")
        if vin:
            vin = vin.upper()
            if len(vin) != 17:
                raise forms.ValidationError("Le VIN doit contenir 17 caractères.")
            if any(c in INVALID_VIN_CHARS for c in vin):
                raise forms.ValidationError("Le VIN contient des caractères interdits (I, O, Q).")
        return vin

    def clean(self):
        cleaned_data = super().clean()
        vin = cleaned_data.get("numero_vin")

        annee = get_vin_year(vin) if vin else None
        cleaned_data["annee_production"] = annee
        cleaned_data["est_avant_2010"] = bool(annee and annee < 2010)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assigne automatiquement la société depuis l'utilisateur
        if self.user:
            instance.societe = getattr(self.user, 'societe', None)
        if commit:
            instance.save()
        return instance