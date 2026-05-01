from django import forms
from django.core.exceptions import ValidationError
from .models import RemplacementMoteur


class RemplacementMoteurForm(forms.ModelForm):

    class Meta:
        model = RemplacementMoteur
        exclude = ["kilometres_remplacement_moteur"]
        widgets = {
            "date_derniere_intervention": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔒 Champs calculés → non modifiables
        self.fields["kilometres_moteur"].disabled = True
        self.fields["variation_kilometres"].disabled = True

        # 💡 Option UX
        self.fields["remplacement_effectue"].help_text = (
            "Cochez pour remplacer le moteur (le kilométrage sera remis à 0 automatiquement)."
        )

    def clean(self):
        cleaned_data = super().clean()

        km_chassis = cleaned_data.get("kilometres_chassis") or 0
        km_entretien = cleaned_data.get("kilometres_dernier_entretien") or 0
        remplacement = cleaned_data.get("remplacement_effectue")

        # 🚫 incohérence entretien
        if km_entretien > km_chassis:
            raise ValidationError(
                "Le kilométrage du dernier entretien ne peut pas dépasser le kilométrage du châssis."
            )

        # ⚠️ sécurité remplacement
        if remplacement and km_chassis == 0:
            raise ValidationError(
                "Impossible de remplacer un moteur avec un kilométrage châssis à 0."
            )

        return cleaned_data