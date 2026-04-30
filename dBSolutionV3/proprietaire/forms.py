from django.db import models
from django import forms
from .models import Proprietaire
from .models import ProprietaireVoiture




class ProprietaireVoitureForm(forms.ModelForm):
    class Meta:
        model = ProprietaireVoiture
        fields = [
            "voiture_exemplaire",
            "proprietaire",
            "part_proprietaire_pourcent",
        ]
        exclude = ["societe"]

        widgets = {
            "voiture_exemplaire": forms.Select(attrs={
                "class": "input"
            }),
            "proprietaire": forms.Select(attrs={
                "class": "input"
            }),
            "part_proprietaire_pourcent": forms.NumberInput(attrs={
                "class": "input",
                "step": "0.01",
                "min": "0",
                "max": "100",
                "placeholder": "Ex: 50.00"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        voiture = cleaned_data.get("voiture_exemplaire")
        part = cleaned_data.get("part_proprietaire_pourcent")

        if voiture and part:
            total = ProprietaireVoiture.objects.filter(
                voiture_exemplaire=voiture
            ).exclude(
                pk=self.instance.pk
            ).aggregate(
                total=models.Sum("part_proprietaire_pourcent")
            )["total"] or 0

            if total + part > 100:
                raise forms.ValidationError(
                    "Le total des parts des propriétaires ne peut pas dépasser 100%."
                )

        return cleaned_data





class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = [
            "nom",
            "prenom",
            "adresse",
            "numero_telephone",
            "numero_permis",
            "numero_carte_id" ,
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "date_naissance",
            "remarques" ,
        ]

        widgets = {
            "nom": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Nom du propriétaire"
            }),
            "prenom": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Prénom du propriétaire"
            }),
            "adresse": forms.Select(attrs={
                "class": "input"
            }),
            "societe": forms.Select(attrs={
                "class": "input"
            }),
        }

    def clean_nom(self):
        nom = self.cleaned_data.get("nom")
        if nom and len(nom) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get("prenom")
        if prenom and len(prenom) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return prenom