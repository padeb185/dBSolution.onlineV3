# voiture_electricite/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Electricite, TypeCarburant


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
            "date": forms.DateInput(attrs={"type": "date"}),
            "date_recharge": forms.DateInput(attrs={"type": "date"}),
            "temps_recharge": forms.TimeInput(attrs={"type": "time"}),
        }
        labels = {
            "voiture_marque": _("Marque"),
            "voiture_modele": _("Modèle"),
            "voiture_exemplaire": _("Véhicule"),
            "immatriculation": _("Immatriculation"),
            "volume_max": _("Kilos Watt max"),
            "kW": _("Kilos Watt"),
            "prix_recharge": _("Prix de la recharge (€)"),
            "date_recharge": _("Date de la recharge"),
            "temps_recharge": _("Temps de recharge"),
            "validation": _("Validation"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Forcer le type de carburant sur ELECTRICITE
        self.instance.type_carburant = TypeCarburant.ELECTRICITE