from datetime import date
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from .models import Fuel
from django.utils.translation import gettext_lazy as _






class FuelForm(forms.ModelForm):
    voiture_marque = forms.CharField(
        label=_("Marque"),
        required=False,
        disabled=True,
    )

    voiture_modele = forms.CharField(
        label=_("Modèle"),
        required=False,
        disabled=True,
    )

    taille_reservoir_display = forms.DecimalField(
        label=_("Volume max (L)"),
        required=False,
        disabled=True,
        max_digits=10,
        decimal_places=2,
    )

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
        "AT": Decimal("20.0"),
        "BE": Decimal("21.0"),
        "BG": Decimal("20.0"),
        "HR": Decimal("25.0"),
        "CY": Decimal("19.0"),
        "CZ": Decimal("21.0"),
        "DK": Decimal("25.0"),
        "EE": Decimal("24.0"),
        "FI": Decimal("25.5"),
        "FR": Decimal("20.0"),
        "DE": Decimal("19.0"),
        "GR": Decimal("24.0"),
        "HU": Decimal("27.0"),
        "IE": Decimal("23.0"),
        "IT": Decimal("22.0"),
        "LV": Decimal("21.0"),
        "LT": Decimal("21.0"),
        "LU": Decimal("17.0"),
        "MT": Decimal("18.0"),
        "NL": Decimal("21.0"),
        "PL": Decimal("23.0"),
        "PT": Decimal("23.0"),
        "RO": Decimal("21.0"),
        "SK": Decimal("23.0"),
        "SI": Decimal("22.0"),
        "ES": Decimal("21.0"),
        "SE": Decimal("25.0"),
        "GB": Decimal("20.0"),
    }

    class Meta:
        model = Fuel

        fields = [
            "voiture_exemplaire",
            "immatriculation",

            # Champs d’affichage ajoutés au formulaire
            "voiture_marque",
            "voiture_modele",
            "taille_reservoir_display",

            "kilometres_chassis",
            "kilometrage_fuel",
            "type_carburant",
            "date",
            "litres",
            "prix_refuelling",
            "pays",
        ]


        widgets = {
            "voiture_exemplaire": forms.HiddenInput(),

            "immatriculation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Commencez à saisir une immatriculation"),
                    "autocomplete": "off",
                }
            ),


            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "readonly": True,
                }
            ),

            "kilometrage_fuel": forms.NumberInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "placeholder": "Kilométrage lors du plein",
                    "min": "0",
                }
            ),

            "type_carburant": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                }
            ),

            "litres": forms.NumberInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "placeholder": "Ex : 50",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "prix_refuelling": forms.NumberInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "placeholder": "Ex : 92.50",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "pays": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                }
            ),

              "date_recharge": forms.DateInput(
                attrs={
                    "type": "date",
                },
                format="%Y-%m-%d",
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
            "kilometrage_fuel",
            "kilometrage_variation",

            "date",
            "type_carburant",

            "litres",
            "prix_refuelling",

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
                    and self.instance.kilometrage_fuel is not None
            ):
                # À adapter suivant l'endroit où tu stockes
                # le kilométrage précédent
                variation = self.instance.kilometrage_variation or 0

            self.fields["kilometrage_variation"].initial = variation

        voiture = None

        if getattr(self.instance, "voiture_exemplaire_id", None):
            voiture = self.instance.voiture_exemplaire

        self.exemplaire = voiture

        if voiture:
            modele = getattr(voiture, "voiture_modele", None)
            marque = (
                getattr(modele, "voiture_marque", None)
                if modele
                else None
            )

            self.fields["voiture_exemplaire"].initial = voiture.pk

            self.fields["immatriculation"].initial = (
                voiture.immatriculation or ""
            )

            self.fields["kilometres_chassis"].initial = (
                voiture.kilometres_chassis or 0
            )

            self.fields["kilometrage_fuel"].initial = (
                self.instance.kilometrage_fuel
                if self.instance.kilometrage_fuel is not None
                else voiture.kilometres_chassis
            )

            if marque:
                self.fields["voiture_marque"].initial = (
                    marque.nom_marque or ""
                )

            if modele:
                self.fields["voiture_modele"].initial = (
                    modele.nom_modele or ""
                )

                self.fields["taille_reservoir_display"].initial = (
                    modele.taille_reservoir or 0
                )

        if self.instance and self.instance.pk:
            # Modification : reprendre la date enregistrée
            if self.instance.date:
                self.fields["date"].initial = self.instance.date
        else:
            # Création : date du jour
            self.fields["date"].initial = date.today()


    def clean_kilometrage_fuel(self):
        kilometrage_fuel = self.cleaned_data.get("kilometrage_fuel")

        voiture = (
            self.cleaned_data.get("voiture_exemplaire")
            or getattr(self.instance, "voiture_exemplaire", None)
        )

        if kilometrage_fuel is None:
            return kilometrage_fuel

        if kilometrage_fuel < 0:
            raise ValidationError(
                "Le kilométrage ne peut pas être négatif."
            )

        if voiture:
            kilometrage_actuel = voiture.kilometres_chassis or 0

            if kilometrage_fuel < kilometrage_actuel:
                raise ValidationError(
                    "Le kilométrage ne peut pas être inférieur "
                    f"au kilométrage actuel du véhicule "
                    f"({kilometrage_actuel} km)."
                )

        return kilometrage_fuel

    def clean(self):
        cleaned_data = super().clean()

        voiture = cleaned_data.get("voiture_exemplaire")
        litres = cleaned_data.get("litres")

        if voiture:
            modele = getattr(voiture, "voiture_modele", None)

            volume_max = (
                getattr(modele, "taille_reservoir", None)
                if modele
                else None
            )

            if (
                litres is not None
                and volume_max is not None
                and litres > volume_max
            ):
                self.add_error(
                    "litres",
                    (
                        f"La quantité saisie ({litres} L) dépasse "
                        f"la capacité maximale du réservoir "
                        f"({volume_max} L)."
                    ),
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = instance.voiture_exemplaire
        kilometrage_fuel = self.cleaned_data.get("kilometrage_fuel")

        # Enregistrer le kilométrage du plein.
        if kilometrage_fuel is not None:
            instance.kilometrage_fuel = kilometrage_fuel

        if voiture:
            kilometrage_actuel = voiture.kilometres_chassis or 0

            # Mettre à jour le kilométrage du véhicule.
            if (
                kilometrage_fuel is not None
                and kilometrage_fuel >= kilometrage_actuel
            ):
                voiture.kilometres_chassis = kilometrage_fuel

                voiture.save(
                    update_fields=["kilometres_chassis"]
                )

            modele = getattr(voiture, "voiture_modele", None)
            marque = (
                getattr(modele, "voiture_marque", None)
                if modele
                else None
            )

            # Remplissage automatique des informations du véhicule.
            if hasattr(instance, "voiture_marque"):
                instance.voiture_marque = marque

            if hasattr(instance, "voiture_modele"):
                instance.voiture_modele = modele

            if hasattr(instance, "taille_reservoir"):
                instance.taille_reservoir = (
                    getattr(modele, "taille_reservoir", 0)
                    if modele
                    else 0
                )

            if hasattr(instance, "kilometres_chassis"):
                instance.kilometres_chassis = (
                    voiture.kilometres_chassis or 0
                )

            if hasattr(instance, "immatriculation"):
                instance.immatriculation = (
                    voiture.immatriculation or ""
                )

        litres = instance.litres
        prix_refuelling = instance.prix_refuelling

        # Calcul automatique des montants.
        if (
            litres is not None
            and prix_refuelling is not None
            and litres > 0
        ):
            litres_decimal = Decimal(str(litres))
            prix_total = Decimal(str(prix_refuelling))

            taux_tva = self.TVA_PAYS.get(
                instance.pays,
                Decimal("0.0"),
            )

            instance.prix_litre = (
                prix_total / litres_decimal
            ).quantize(Decimal("0.0001"))

            # Prix total considéré comme TTC.
            if taux_tva > 0:
                instance.montant_ht = (
                    prix_total
                    / (
                        Decimal("1.0")
                        + taux_tva / Decimal("100.0")
                    )
                ).quantize(Decimal("0.01"))

                instance.montant_tva = (
                    prix_total - instance.montant_ht
                ).quantize(Decimal("0.01"))

            else:
                instance.montant_ht = prix_total.quantize(
                    Decimal("0.01")
                )
                instance.montant_tva = Decimal("0.00")

        else:
            instance.prix_litre = Decimal("0.0000")
            instance.montant_tva = Decimal("0.00")
            instance.montant_ht = Decimal("0.00")

        if commit:
            instance.save()

        return instance