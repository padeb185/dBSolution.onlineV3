from django import forms
from decimal import Decimal
from .models import Fuel


class FuelForm(forms.ModelForm):

    # Champs affichés en lecture seule
    voiture_marque = forms.CharField(
        label="Marque",
        required=False,
        disabled=True
    )

    voiture_modele = forms.CharField(
        label="Modèle",
        required=False,
        disabled=True
    )

    taille_reservoir_display = forms.FloatField(
        label="Volume max (L)",
        required=False,
        disabled=True
    )

    class Meta:
        model = Fuel
        fields = [
            "immatriculation",
            "voiture_exemplaire",
            "type_carburant",
            "date",
            "litres",
            "prix_refuelling",
            "validation",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "voiture_exemplaire": forms.HiddenInput(),
        }

    # ---------------------------
    # INITIALISATION
    # ---------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.voiture_exemplaire:
            self._fill_readonly_fields(self.instance.voiture_exemplaire)

    def _fill_readonly_fields(self, voiture):
        self.fields["voiture_marque"].initial = voiture.voiture_marque.nom_marque
        self.fields["voiture_modele"].initial = voiture.voiture_modele.nom_modele
        self.fields["taille_reservoir_display"].initial = (
            voiture.voiture_modele.taille_reservoir
        )

    # ---------------------------
    # VALIDATION
    # ---------------------------
    def clean(self):
        cleaned_data = super().clean()

        voiture = cleaned_data.get("voiture_exemplaire")
        litres = cleaned_data.get("litres")
        prix_refuelling = cleaned_data.get("prix_refuelling")

        if voiture and litres:
            taille_max = voiture.voiture_modele.taille_reservoir
            if litres > taille_max:
                raise forms.ValidationError(
                    "Le nombre de litres ne peut pas dépasser le volume maximum du réservoir."
                )

        if prix_refuelling and prix_refuelling <= 0:
            raise forms.ValidationError(
                "Le prix du plein doit être supérieur à 0."
            )

        return cleaned_data

    # ---------------------------
    # SAVE
    # ---------------------------
    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.voiture_exemplaire:
            instance.voiture_marque = instance.voiture_exemplaire.voiture_marque
            instance.voiture_modele = instance.voiture_exemplaire.voiture_modele
            instance.taille_reservoir = (
                instance.voiture_exemplaire.voiture_modele.taille_reservoir
            )

        if instance.litres and instance.prix_refuelling:
            instance.prix_litre = (
                Decimal(instance.prix_refuelling) /
                Decimal(instance.litres)
            )

        if commit:
            instance.save()

        return instance

