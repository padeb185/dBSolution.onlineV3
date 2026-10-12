from django import forms
from django.utils.translation import gettext_lazy as _

from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = (
            "voiture_exemplaire",
            "client",
            "type_location",
            "circuit",
            "route",
            "date_debut",
            "date_fin",
            "kilometrage",
            "prix",
            "remarques",
        )
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "prix": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)
        if societe is not None:
            self.fields["voiture_exemplaire"].queryset = (
                VoitureExemplaire.objects.filter(societe=societe)
                .select_related("voiture_marque", "voiture_modele")
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if commit:
            instance.save()
        return instance
