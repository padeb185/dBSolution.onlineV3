from django import forms
from django.utils.translation import gettext_lazy as _
from .models import VoitureExemplaire
from .utils.vin_decoder import VinDecoderService

INVALID_VIN_CHARS = set("IOQ")


class VoitureExemplaireForm(forms.ModelForm):
    date_mise_en_circulation = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d", "%d/%m/%Y"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "input",
            }
        ),
        label=_("Date de mise en circulation")
    )

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
            "kilometres_boite",
            "kilometres_embrayage",
            "kilometres_dernier_entretien",
            "kilometres_rodage",
            "mois_production",
            "date_mise_en_circulation",
            "est_apres_2010",
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
            "est_apres_2010": forms.CheckboxInput(attrs={"class": "mt-2"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["date_mise_en_circulation"].widget.format = "%Y-%m-%d"

    def clean_numero_vin(self):
        vin = self.cleaned_data.get("numero_vin")

        if vin:
            vin = vin.upper().strip()

            if len(vin) != 17:
                raise forms.ValidationError(_("Le VIN doit contenir 17 caractères."))

            if any(c in INVALID_VIN_CHARS for c in vin):
                raise forms.ValidationError(_("Le VIN contient des caractères interdits (I, O, Q)."))

        return vin

    def clean(self):
        cleaned_data = super().clean()
        vin = cleaned_data.get("numero_vin")

        if vin:
            decoder = VinDecoderService(vin)
            data = decoder.decode()
            annee = data.get("model_year")

            cleaned_data["annee_production"] = annee

            if annee:
                cleaned_data["est_apres_2010"] = annee >= 2010

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.societe = getattr(self.user, "societe", None)

        # Important : applique les valeurs calculées
        instance.annee_production = self.cleaned_data.get("annee_production")
        instance.est_apres_2010 = self.cleaned_data.get("est_apres_2010", instance.est_apres_2010)

        if commit:
            instance.save()

        return instance