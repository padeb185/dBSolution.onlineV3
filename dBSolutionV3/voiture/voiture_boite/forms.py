from django import forms
from voiture.voiture_boite.models import VoitureBoite
from django.utils.translation import gettext_lazy as _



class VoitureBoiteForm(forms.ModelForm):

    class Meta:
        model = VoitureBoite

        exclude = ['voitures_modeles', 'voitures_exemplaires', 'kilometres_chassis',
                   'dernier_entretien', 'numero_boite']

        labels = {
            "fabricant": _("Fabricant"),
            "nom_du_type": _("Nom du type"),
            "type_de_boite": _("Type de boîte"),
            "oem": _("OEM"),

            "nombre_rapport": _("Nombre de rapports"),

            # Lubrification
            "qualite_huile": _("Qualité d'huile de boîte"),
            "quantite_huile_l": _("Quantité d'huile boîte (L)"),

            # Suivi kilométrique
            "kilometres_chassis": _("Kilométrage châssis"),
            "intervalle_entretien_km": _("Intervalle entretien (km)"),

            # Historique entretien
            "dernier_entretien": _("Dernier entretien"),

            # Gestion remplacement
            "numero_boite": _("Numéro de boîte"),

            # Dates
            "date_creation": _("Date de création"),

            # Divers
            "remarques": _("Remarques"),
        }

        widgets = {

            # -------------------------
            # TEXTE
            # -------------------------
            "fabricant": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: ZF, Aisin..."
            }),

            "nom_du_type": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: 8HP, DSG7..."
            }),

            "qualite_huile": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: ATF-III, 75W90..."
            }),

            # -------------------------
            # SELECT
            # -------------------------
            "type_de_boite": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm h-10"
            }),

            # -------------------------
            # NUMBERS
            # -------------------------
            "nombre_rapport": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: 6, 7, 8"
            }),

            "quantite_huile_l": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": "Ex: 7.5",
                "step": "0.1",
                "min": "0"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)