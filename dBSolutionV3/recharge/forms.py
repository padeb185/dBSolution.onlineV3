from django import forms
from decimal import Decimal, ROUND_HALF_UP
from .models import Electricite


class ElectriciteForm(forms.ModelForm):
    voiture_marque = forms.CharField(label="Marque", required=False, disabled=True)
    voiture_modele = forms.CharField(label="Modèle", required=False, disabled=True)

    TVA_PAYS = {
        'BE': Decimal('21.0'),
        'LU': Decimal('17.0'),
        'DE': Decimal('19.0'),
    }

    class Meta:
        model = Electricite
        fields = [
            "voiture_exemplaire",
            "immatriculation",
            "kilometrage_electricite",
            "type_carburant",
            "date",
            "kW",
            "prix_recharge",
            "pays",
        ]

        widgets = {
            "voiture_exemplaire": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        voiture = None

        voiture_id = self.data.get("voiture_exemplaire") or self.initial.get("voiture_exemplaire")

        if voiture_id:
            from voiture.voiture_exemplaire.models import VoitureExemplaire

            voiture = VoitureExemplaire.objects.select_related(
                "voiture_modele",
                "voiture_modele__voiture_marque"
            ).filter(id=voiture_id).first()

        if not voiture and self.instance and getattr(self.instance, "pk", None):
            try:
                voiture = self.instance.voiture_exemplaire
            except Exception:
                voiture = None

        if voiture:
            self.fields["voiture_marque"].initial = voiture.voiture_modele.voiture_marque.nom_marque
            self.fields["voiture_modele"].initial = voiture.voiture_modele.nom_modele

            if not self.data.get("kilometrage_electricite"):
                self.fields["kilometrage_electricite"].initial = voiture.kilometres_chassis

            self.fields["voiture_exemplaire"].initial = voiture.id

    def clean(self):
        cleaned = super().clean()

        voiture = cleaned.get("voiture_exemplaire")

        if voiture:
            try:
                cleaned["voiture_marque"] = voiture.voiture_modele.voiture_marque.nom_marque
                cleaned["voiture_modele"] = voiture.voiture_modele.nom_modele
            except Exception:
                pass

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = getattr(instance, "voiture_exemplaire", None)

        instance.kilometrage_electricite = self.cleaned_data.get("kilometrage_electricite", 0)

        if voiture and instance.kilometrage_electricite >= voiture.kilometres_chassis:
            voiture.kilometres_chassis = instance.kilometrage_electricite
            voiture.save()

        if voiture:
            instance.voiture_marque = voiture.voiture_marque
            instance.voiture_modele = voiture.voiture_modele

        if instance.kW and instance.kW > 0 and instance.prix_recharge:
            instance.prix_watt = (
                Decimal(instance.prix_recharge) / Decimal(instance.kW)
            ).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)

            taux_tva = self.TVA_PAYS.get(instance.pays, Decimal('0.0'))

            instance.montant_tva = (
                Decimal(instance.prix_recharge) * taux_tva / Decimal('100.0')
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            instance.montant_ht = (
                Decimal(instance.prix_recharge) - instance.montant_tva
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            instance.prix_watt = Decimal('0.0')
            instance.montant_tva = Decimal('0.0')
            instance.montant_ht = Decimal('0.0')

        if commit:
            instance.save()

        return instance