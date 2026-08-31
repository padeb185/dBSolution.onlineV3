from datetime import date

from django.core.exceptions import ValidationError

from django import forms
from decimal import Decimal, ROUND_HALF_UP
from .models import Electricite
from django.utils.translation import gettext_lazy as _


class ElectriciteForm(forms.ModelForm):
    voiture_marque = forms.CharField(label="Marque", required=False, disabled=True)
    voiture_modele = forms.CharField(label="Modèle", required=False, disabled=True)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(
            attrs={
                "readonly": "readonly",
                "class": "input",
            }
        ),
    )



    TVA_PAYS = {
        'AT': Decimal('20.0'),
        'BE': Decimal('21.0'),
        'BG': Decimal('20.0'),
        'HR': Decimal('25.0'),
        'CY': Decimal('19.0'),
        'CZ': Decimal('21.0'),
        'DK': Decimal('25.0'),
        'EE': Decimal('24.0'),
        'FI': Decimal('25.5'),
        'FR': Decimal('20.0'),
        'DE': Decimal('19.0'),
        'GR': Decimal('24.0'),
        'HU': Decimal('27.0'),
        'IE': Decimal('23.0'),
        'IT': Decimal('22.0'),
        'LV': Decimal('21.0'),
        'LT': Decimal('21.0'),
        'LU': Decimal('17.0'),
        'MT': Decimal('18.0'),
        'NL': Decimal('21.0'),
        'PL': Decimal('23.0'),
        'PT': Decimal('23.0'),
        'RO': Decimal('21.0'),
        'SK': Decimal('23.0'),
        'SI': Decimal('22.0'),
        'ES': Decimal('21.0'),
        'SE': Decimal('25.0'),
        'GB': Decimal('20.0'),
    }

    class Meta:
        model = Electricite

        fields = [
            "voiture_exemplaire",
            "immatriculation",

            "kilometres_chassis",
            "kilometrage_electricite",

            "date_recharge",
            "type_carburant",
            "kW",
            "prix_recharge",
            "pays",
        ]

        widgets = {
            "voiture_exemplaire": forms.HiddenInput(),

            "date_recharge": forms.DateInput(
                attrs={
                    "type": "date",
                },
                format="%Y-%m-%d",
            ),

            "immatriculation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _(
                        "Commencez à saisir une immatriculation"
                    ),
                    "autocomplete": "off",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        self.societe = kwargs.pop("societe", None)

        super().__init__(*args, **kwargs)

        self.order_fields([
            "voiture_exemplaire",
            "immatriculation",

            "voiture_marque",
            "voiture_modele",

            "kilometres_chassis",
            "kilometrage_electricite",
            "kilometrage_variation",

            "date_recharge",
            "type_carburant",

            "kW",
            "prix_recharge",

            "pays",
        ])


        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        if "kilometrage_variation" in self.fields:

            variation = 0

            if (
                    self.instance
                    and self.instance.pk
                    and self.instance.kilometrage_electricite is not None
            ):
                # À adapter suivant l'endroit où tu stockes
                # le kilométrage précédent
                variation = self.instance.kilometrage_variation or 0

            self.fields["kilometrage_variation"].initial = variation


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

        if self.instance and self.instance.pk:
            # Modification : reprendre la date enregistrée
            if self.instance.date_recharge:
                self.fields["date_recharge"].initial = self.instance.date_recharge
        else:
            # Création : date du jour
            self.fields["date_recharge"].initial = date.today()



    def clean_kilometrage_electricite(self):
        kilometrage_electricite = self.cleaned_data.get("kilometrage_electricite")

        voiture = (
            self.cleaned_data.get("voiture_exemplaire")
            or getattr(self.instance, "voiture_exemplaire", None)
        )

        if kilometrage_electricite is None:
            return kilometrage_electricite

        if kilometrage_electricite < 0:
            raise ValidationError(
                "Le kilométrage ne peut pas être négatif."
            )

        if voiture:
            kilometrage_actuel = voiture.kilometres_chassis or 0

            if kilometrage_electricite < kilometrage_actuel:
                raise ValidationError(
                    "Le kilométrage ne peut pas être inférieur "
                    f"au kilométrage actuel du véhicule "
                    f"({kilometrage_actuel} km)."
                )

        return kilometrage_electricite



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