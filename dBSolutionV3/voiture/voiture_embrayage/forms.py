from django import forms
from django.utils.translation import gettext_lazy as _
from voiture.voiture_embrayage.models import VoitureEmbrayage


class VoitureEmbrayageForm(forms.ModelForm):

    class Meta:
        model = VoitureEmbrayage

        exclude = (
            'societe',
            'voitures_exemplaires',
            'voitures_modeles',
            'numero_embrayage',
            'kilometres_chassis',
        )

        labels = {
            "kilometres_chassis": _("Kilométrage châssis"),
            "fabricant": _("Fabricant"),
            "oem": _("Référence OEM"),
            "type_embrayage": _("Type d'embrayage"),
            "type_lubrification": _("Type de lubrification"),
            "volant_moteur": _("Type de volant moteur"),
            "plateau_pression": _("Plateau de pression"),
            "butee_embrayage": _("Butée d'embrayage"),
            "remarques": _("Remarques"),
        }

        widgets = {

            "fabricant": forms.Select(),

            "oem": forms.TextInput(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "placeholder": _("Référence OEM")
                }
            ),

            "type_embrayage": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm"
                }
            ),

            "type_lubrification": forms.Select(),

            "volant_moteur": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm"
                }
            ),

            "plateau_pression": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm"
                }
            ),

            "butee_embrayage": forms.Select(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm"
                }
            ),

            "remarques": forms.Textarea(
                attrs={
                    "class": "border rounded px-3 py-2 w-full text-sm",
                    "rows": 4,
                    "placeholder": _("Ajoutez des remarques...")
                }
            ),
        }

    # Style identique pour tous les champs
    CLASSE_CHAMP = "border rounded px-3 py-2 w-full text-sm"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = self.CLASSE_CHAMP

    def clean_fabricant(self):
        fabricant = self.cleaned_data.get("fabricant")

        if not fabricant or fabricant == "CHOISIR":
            raise forms.ValidationError(_("Veuillez choisir un fabricant."))

        return fabricant
