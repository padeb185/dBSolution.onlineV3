from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from voiture.voiture_freins_av.models import VoitureFreinsAV




class VoitureFreinsAVForm(forms.ModelForm):
    class Meta:
        model = VoitureFreinsAV

        exclude = [
            "voitures_exemplaires",
            "societe",
        ]

        def clean_epaisseur_min_disque_av(self):
            valeur = self.cleaned_data.get("epaisseur_min_disque_av")

            if valeur:
                try:
                    # transforme 24,4 → 24.4
                    valeur = float(str(valeur).replace(",", "."))
                except ValueError:
                    raise ValidationError(
                        _("Veuillez entrer un nombre valide.")
                    )

            return valeur

        labels = {
            "marque_disques_av": _("Marque des disques avant"),
            "numero_oem_disques_av": _("Numéro OEM des disques avant"),
            "marque_plaquettes_av": _("Marque des plaquettes avant"),
            "numero_oem_plaquettes_av": _("Numéro OEM des plaquettes avant"),
            "frein_av_matiere": _("Matière des disques avant"),
            "type_disques_av": _("Type de disque avant"),
            "taille_disque_av": _("Taille des disques avant (mm)"),
            "epaisseur_disque_av": _("Épaisseur des disques avant (mm)"),
            "epaisseur_min_disque_av": _("Épaisseur minimum des disques avant (mm)"),
            "plaquette_av_matiere": _("Matière des plaquettes avant"),
            "plaquettes_av": _("Épaisseur des plaquettes avant (mm)"),
            "remarques": _("Remarques"),
        }

        widgets = {
            "marque_disques_av": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : Brembo")
            }),

            "numero_oem_disques_av": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Référence OEM disque")
            }),

            "marque_plaquettes_av": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : Bosch")
            }),

            "numero_oem_plaquettes_av": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Référence OEM plaquette")
            }),

            "frein_av_matiere": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "type_disques_av": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "taille_disque_av": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 288"),
                "step": "0.1",
                "min": "0"
            }),

            "epaisseur_disque_av": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 25"),
                "step": "0.1",
                "min": "0"
            }),

            "epaisseur_min_disque_av": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 24,4")
            }),

            "plaquette_av_matiere": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),

            "plaquettes_av": forms.NumberInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 10"),
                "step": "0.1",
                "min": "0"
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "rows": 4,
                "placeholder": _("Ajoutez des remarques...")
            }),
        }