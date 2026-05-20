from django import forms
from django.utils.translation import gettext_lazy as _
from ..voiture_freins_ar.models import VoitureFreinsAR


class VoitureFreinsARForm(forms.ModelForm):
    taille_disque_ar = forms.DecimalField(
        required=False,
        localize=True
    )

    epaisseur_disque_ar = forms.DecimalField(
        required=False,
        localize=True
    )

    epaisseur_min_disque_ar = forms.DecimalField(
        required=False,
        localize=True
    )

    plaquettes_ar = forms.DecimalField(
        required=False,
        localize=True
    )

    class Meta:
        model = VoitureFreinsAR
        exclude = [
            "voitures_exemplaires",
            "societe",
        ]

        labels = {
            "marque_disques_ar": _("Marque des disques arrière"),
            "numero_oem_disques_ar": _("Numéro OEM des disques arrière"),
            "marque_plaquettes_ar": _("Marque des plaquettes arrière"),
            "numero_oem_plaquettes_ar": _("Numéro OEM des plaquettes arrière"),
            "frein_ar_matiere": _("Matière des disques arrière"),
            "type_disques_ar": _("Type de disque arrière"),
            "taille_disque_ar": _("Diamètre du disque arrière (mm)"),
            "epaisseur_disque_ar": _("Épaisseur du disque arrière (mm)"),
            "epaisseur_min_disque_ar": _("Épaisseur minimum du disque arrière (mm)"),
            "plaquette_ar_matiere": _("Matière des plaquettes arrière"),
            "plaquettes_ar": _("Épaisseur des plaquettes arrière (mm)"),
            "remarques": _("Remarques"),
        }

        widgets = {
            "marque_disques_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : Brembo")
            }),
            "numero_oem_disques_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Référence OEM disque arrière")
            }),
            "marque_plaquettes_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : Bosch")
            }),
            "numero_oem_plaquettes_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Référence OEM plaquette arrière")
            }),
            "frein_ar_matiere": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),
            "type_disques_ar": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),
            "taille_disque_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 280 ou 280,5")
            }),
            "epaisseur_disque_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 24 ou 24,4")
            }),
            "epaisseur_min_disque_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 22 ou 22,4")
            }),
            "plaquette_ar_matiere": forms.Select(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm"
            }),
            "plaquettes_ar": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "placeholder": _("Ex : 10 ou 10,5")
            }),
            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-3 py-2 w-full text-sm",
                "rows": 4,
                "placeholder": _("Ajoutez des remarques...")
            }),
        }

    def clean_decimal_field(self, field_name):
        value = self.data.get(field_name)

        if value in [None, ""]:
            return None

        value = str(value).replace(",", ".")

        try:
            return float(value)
        except ValueError:
            raise forms.ValidationError(_("Saisissez un nombre valide."))

    def clean_taille_disque_ar(self):
        return self.clean_decimal_field("taille_disque_ar")

    def clean_epaisseur_disque_ar(self):
        return self.clean_decimal_field("epaisseur_disque_ar")

    def clean_epaisseur_min_disque_ar(self):
        return self.clean_decimal_field("epaisseur_min_disque_ar")

    def clean_plaquettes_ar(self):
        return self.clean_decimal_field("plaquettes_ar")