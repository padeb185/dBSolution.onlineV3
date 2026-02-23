from django import forms
from .models import VoitureModele
from voiture.voiture_marque.models import VoitureMarque


class VoitureModeleForm(forms.ModelForm):
    class Meta:
        model = VoitureModele
        fields = [
            "voiture_marque",
            "nom_modele",
            "nom_variante",
            "nombre_portes",
            "nbre_places",
            "taille_reservoir",
            "capacite_batterie",
        ]

        widgets = {
            "voiture_marque": forms.Select(attrs={"class": "form-select"}),
            "nom_modele": forms.TextInput(attrs={"class": "form-control"}),
            "nom_variante": forms.TextInput(attrs={"class": "form-control"}),
            "nombre_portes": forms.Select(attrs={"class": "form-select"}),
            "nbre_places": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "taille_reservoir": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "capacite_batterie": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  # ✅ stocker le user
        super().__init__(*args, **kwargs)

        # 🔒 Filtrer les marques par société
        if self.user and hasattr(self.user, "societe"):
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.filter(
                societe=self.user.societe
            )
        else:
            self.fields["voiture_marque"].queryset = VoitureMarque.objects.none()

        # Batterie optionnelle
        self.fields["capacite_batterie"].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ⚡ Assigner automatiquement la société
        if self.user and hasattr(self.user, "societe"):
            instance.societe = self.user.societe

        if commit:
            instance.save()

        return instance