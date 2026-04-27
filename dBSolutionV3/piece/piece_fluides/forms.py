from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PieceFluide


class PieceFluideForm(forms.ModelForm):
    class Meta:
        model = PieceFluide
        fields = [
            "reference",
            "designation",
            "type_fluide",
            "viscosite",
            "marque",
            "conditionnement_litre",
            "actif",
        ]

        widgets = {
            "reference": forms.TextInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": _("Référence"),
            }),

            "designation": forms.TextInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": _("Désignation"),
            }),

            "type_fluide": forms.Select(attrs={
                "class": "w-full border rounded px-3 py-2",
            }),

            "viscosite": forms.TextInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": _("Ex: 5W30 / DOT4 / G13 / CHF11S"),
            }),

            "marque": forms.TextInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "placeholder": _("Marque"),
            }),

            "conditionnement_litre": forms.NumberInput(attrs={
                "class": "w-full border rounded px-3 py-2",
                "step": "0.01",
                "min": "0",
            }),

            "actif": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-blue-600",
            }),
        }

        labels = {
            "reference": _("Référence"),
            "designation": _("Désignation"),
            "type_fluide": _("Type de fluide"),
            "viscosite": _("Viscosité / Norme"),
            "marque": _("Marque"),
            "conditionnement_litre": _("Conditionnement (litres)"),
            "actif": _("Actif"),
        }

    def clean_reference(self):
        reference = self.cleaned_data["reference"].strip().upper()
        return reference

    def clean_designation(self):
        designation = self.cleaned_data["designation"].strip()
        if len(designation) < 3:
            raise forms.ValidationError(
                _("La désignation doit contenir au moins 3 caractères.")
            )
        return designation

    def clean_conditionnement_litre(self):
        value = self.cleaned_data["conditionnement_litre"]
        if value <= 0:
            raise forms.ValidationError(
                _("Le conditionnement doit être supérieur à 0.")
            )
        return value