from django import forms
from .models import Piece, Fabricant, CodeBarre, Inventaire


class FabricantForm(forms.ModelForm):
    class Meta:
        model = Fabricant
        fields = ["nom", "pays"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "pays": forms.TextInput(attrs={"class": "form-control"}),
        }


class CodeBarreForm(forms.ModelForm):
    class Meta:
        model = CodeBarre
        fields = ["code"]
        widgets = {
            "code": forms.TextInput(attrs={"class": "form-control"}),
        }


class PieceForm(forms.ModelForm):

    class Meta:
        model = Piece
        fields = [
            "societe",
            "modele",
            "voiture_marque",
            "vehicule",
            "fabricants",
            "codes_barres",
            "immatriculation",
            "annee",
            "site",
            "pays",
            "emplacement_etagere",
            "qualite",
            "oem",
            "prix_achat",
            "majoration_pourcent",
            "tva",
            "prix_vente",
            "quantite_stock",
            "quantite_min",
            "organe",
            "marque",
        ]

        widgets = {

            "fabricants": forms.SelectMultiple(attrs={"class": "form-select"}),
            "codes_barres": forms.SelectMultiple(attrs={"class": "form-select"}),

            "immatriculation": forms.TextInput(attrs={"class": "form-control"}),
            "annee": forms.NumberInput(attrs={"class": "form-control"}),

            "site": forms.TextInput(attrs={"class": "form-control"}),
            "pays": forms.TextInput(attrs={"class": "form-control"}),

            "emplacement_etagere": forms.TextInput(attrs={"class": "form-control"}),

            "qualite": forms.TextInput(attrs={"class": "form-control"}),

            "oem": forms.TextInput(attrs={"class": "form-control"}),

            "prix_achat": forms.NumberInput(attrs={"class": "form-control"}),
            "majoration_pourcent": forms.NumberInput(attrs={"class": "form-control"}),
            "tva": forms.NumberInput(attrs={"class": "form-control"}),
            "prix_vente": forms.NumberInput(attrs={"class": "form-control"}),

            "quantite_stock": forms.NumberInput(attrs={"class": "form-control"}),
            "quantite_min": forms.NumberInput(attrs={"class": "form-control"}),

            "organe": forms.TextInput(attrs={"class": "form-control"}),
            "marque": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        prix_achat = cleaned_data.get("prix_achat")
        majoration = cleaned_data.get("majoration_pourcent")

        if prix_achat and majoration:
            cleaned_data["prix_vente"] = prix_achat * (1 + majoration / 100)

        return cleaned_data


class InventaireForm(forms.ModelForm):

    class Meta:
        model = Inventaire
        fields = ["piece", "variation", "commentaire"]

        widgets = {
            "piece": forms.Select(attrs={"class": "form-select"}),
            "variation": forms.NumberInput(attrs={"class": "form-control"}),
            "commentaire": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def save(self, commit=True):

        inventaire = super().save(commit=False)

        if commit:
            inventaire.save()
            inventaire.mise_a_jour_stock(inventaire.variation)

        return inventaire