from django import forms
from decimal import Decimal
from .models import Electricite
from django.utils.translation import gettext_lazy as _


class ElectriciteForm(forms.ModelForm):
    voiture_marque = forms.CharField(label="Marque", required=False, disabled=True)
    voiture_modele = forms.CharField(label="Modèle", required=False, disabled=True)
    capacite_batterie_display = forms.FloatField(label="Volume max (kW)", required=False, disabled=True)

    # TVA par pays
    TVA_PAYS = {
        'BE': Decimal('21.0'),
        'LU': Decimal('17.0'),
        'DE': Decimal('19.0'),
    }

    class Meta:
        model = Electricite
        fields = [
            "immatriculation",
            "voiture_exemplaire",
            "kilometrage_electricite",
            "type_carburant",
            "date",
            "kW",
            "prix_recharge",
            "pays",
            "validation",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "voiture_exemplaire": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        voiture = getattr(self.instance, "voiture_exemplaire", None)
        if voiture:
            self.fields["voiture_marque"].initial = voiture.voiture_modele.voiture_marque.nom_marque
            self.fields["voiture_modele"].initial = voiture.voiture_modele.nom_modele
            self.fields["capacite_batterie_display"].initial = voiture.voiture_modele.capacite_batterie
            self.fields["kilometrage_electricite"].initial = getattr(self.instance, "kilometrage_electricite", voiture.kilometres_chassis)


            # Initialiser le champ caché voiture_exemplaire
            self.fields["voiture_exemplaire"].initial = voiture.id

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire

        # Sauvegarder le kilométrage Fuel
        instance.kilometrage_electricite = self.cleaned_data.get("kilometrage_electricite", 0)

        # Mettre à jour le kilométrage de la voiture si plus grand
        if voiture and instance.kilometrage_electricite >= voiture.kilometres_chassis:
            voiture.kilometres_chassis = instance.kilometrage_electricite
            voiture.save()

        # Remplissage automatique des infos voiture
        if voiture:
            instance.voiture_marque = voiture.voiture_marque
            instance.voiture_modele = voiture.voiture_modele
            instance.capacite_batterie = voiture.voiture_modele.capacite_batterie

        # Calcul automatique des prix et TVA
        if instance.kW and instance.prix_recharge:
            instance.prix_watt = Decimal(instance.prix_recharge) / Decimal(instance.kW)
            taux_tva = self.TVA_PAYS.get(instance.pays, Decimal('0.0'))
            instance.montant_tva = Decimal(instance.prix_recharge) * taux_tva / Decimal('100.0')
            instance.montant_ht = Decimal(instance.prix_recharge) - instance.montant_tva
        else:
            instance.prix_watt = Decimal('0.0')
            instance.montant_tva = Decimal('0.0')
            instance.montant_ht = Decimal('0.0')

        if commit:
            instance.save()
        return instance