from django import forms

from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Diagnostic


class DiagnosticForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ("voiture_exemplaire", "code_defaut", "piece_defaut", "piece_defaut_autre", "description")
        widgets = {
            "code_defaut": forms.TextInput(attrs={"style": "text-transform:uppercase", "maxlength": 20}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)

        # Exemplaires triés par marque, puis modèle, puis immatriculation
        vehicules = (
            VoitureExemplaire.objects
            .select_related("voiture_marque", "voiture_modele")
            .order_by(
                "voiture_marque__nom_marque",
                "voiture_modele__nom_modele",
                "voiture_modele__nom_variante",
                "immatriculation",
            )
        )
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)

        self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["voiture_exemplaire"].required = True

    def clean_code_defaut(self):
        return (self.cleaned_data.get("code_defaut") or "").strip().upper()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if commit:
            instance.save()
        return instance
