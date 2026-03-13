from django import forms
from .models import Electricite, TypeCarburant
from voiture.voiture_exemplaire.models import VoitureExemplaire




class ElectriciteForm(forms.ModelForm):
    class Meta:
        model = Electricite
        fields = [
            "voiture_marque",
            "voiture_modele",
            "voiture_exemplaire",
            "immatriculation",
            "volume_max",
            "date",
            "kW",
            "prix_recharge",
            "date_recharge",
            "temps_recharge",
            "validation",
        ]
        widgets = {
            "voiture_marque": forms.TextInput(attrs={"readonly": "readonly"}),
            "voiture_modele": forms.TextInput(attrs={"readonly": "readonly"}),
            "volume_max": forms.TextInput(attrs={"readonly": "readonly"}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "date_recharge": forms.DateInput(attrs={"type": "date"}),
            "temps_recharge": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        # ⚡ Récupération sécurisée de la voiture si fournie
        voiture = kwargs.pop("voiture", None)
        super().__init__(*args, **kwargs)
        self.instance.type_carburant = TypeCarburant.ELECTRICITE

        if voiture:
            self.fields["voiture_marque"].initial = voiture.voiture_modele.voiture_marque.nom_marque
            self.fields["voiture_modele"].initial = voiture.voiture_modele.nom_modele
            self.fields["volume_max"].initial = voiture.voiture_modele.capacite_batterie
            self.fields["voiture_exemplaire"].initial = voiture

    def clean_immatriculation(self):
        immat = self.cleaned_data.get("immatriculation")
        if immat:
            try:
                voiture = VoitureExemplaire.objects.get(immatriculation=immat)
            except VoitureExemplaire.DoesNotExist:
                raise forms.ValidationError("Aucune voiture ne correspond à cette immatriculation.")

            # ⚡ Remplir les champs FK correctement avec les instances
            self.cleaned_data["voiture_exemplaire"] = voiture
            self.cleaned_data["voiture_modele"] = voiture.voiture_modele
            self.cleaned_data["voiture_marque"] = voiture.voiture_modele.voiture_marque
            self.cleaned_data["volume_max"] = voiture.voiture_modele.capacite_batterie

        return immat