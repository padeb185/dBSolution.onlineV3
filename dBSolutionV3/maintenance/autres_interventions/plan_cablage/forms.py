from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import ConnecteurCablage, FilCablage, PlanCablage

INPUT = "border rounded px-3 py-2 w-full"
PETIT = "border rounded px-2 py-1 w-full text-sm"


class PlanCablageForm(forms.ModelForm):
    class Meta:
        model = PlanCablage
        fields = ["type_cablage", "nom_boitier", "reference_boitier", "nom", "remarques"]
        widgets = {
            "type_cablage": forms.Select(attrs={"class": INPUT}),
            "nom_boitier": forms.TextInput(attrs={"class": INPUT, "placeholder": "Bosch ME7.5"}),
            "reference_boitier": forms.TextInput(attrs={"class": INPUT, "placeholder": "0 261 208 xxx"}),
            "nom": forms.TextInput(attrs={"class": INPUT, "placeholder": _("Faisceau moteur")}),
            "remarques": forms.Textarea(attrs={"class": INPUT, "rows": 3}),
        }


class ConnecteurCablageForm(forms.ModelForm):
    class Meta:
        model = ConnecteurCablage
        fields = ["nom", "reference_connecteur", "longueur_cm", "nombre_coudes", "gaine", "ordre", "remarques"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": INPUT, "placeholder": _("Injecteur cylindre 1")}),
            "reference_connecteur": forms.TextInput(attrs={"class": INPUT, "placeholder": "Bosch EV1"}),
            "longueur_cm": forms.NumberInput(attrs={"class": INPUT, "min": "0", "placeholder": "160"}),
            "nombre_coudes": forms.NumberInput(attrs={"class": INPUT, "min": "0"}),
            "gaine": forms.TextInput(attrs={"class": INPUT}),
            "ordre": forms.NumberInput(attrs={"class": INPUT, "min": "0"}),
            "remarques": forms.TextInput(attrs={"class": INPUT}),
        }


class FilCablageForm(forms.ModelForm):
    class Meta:
        model = FilCablage
        fields = ["pin_connecteur", "pin_boitier", "couleur_fil", "couleur_bande", "fonction", "description",
                  "section_mm2"]
        widgets = {
            "pin_connecteur": forms.TextInput(attrs={"class": PETIT, "placeholder": "1"}),
            "pin_boitier": forms.TextInput(attrs={"class": PETIT, "placeholder": "A12"}),
            "couleur_fil": forms.Select(attrs={"class": PETIT + " couleur-fil"}),
            "couleur_bande": forms.Select(attrs={"class": PETIT + " couleur-bande"}),
            "fonction": forms.Select(attrs={"class": PETIT}),
            "description": forms.TextInput(attrs={"class": PETIT}),
            "section_mm2": forms.NumberInput(attrs={"class": PETIT, "step": "0.05", "min": "0", "placeholder": "0.75"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("couleur_bande") and cleaned.get("couleur_bande") == cleaned.get("couleur_fil"):
            self.add_error("couleur_bande", _("La bande doit être d'une autre couleur que le fil."))
        return cleaned


class BaseFilFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        pins = []
        for f in self.forms:
            if not hasattr(f, "cleaned_data") or f.cleaned_data.get("DELETE") or not f.cleaned_data:
                continue
            pin = (f.cleaned_data.get("pin_connecteur") or "").strip().upper()
            if pin:
                if pin in pins:
                    raise forms.ValidationError(_("La position %(pin)s du connecteur est utilisée plusieurs fois.") % {"pin": pin})
                pins.append(pin)


FilFormSet = inlineformset_factory(
    ConnecteurCablage, FilCablage, form=FilCablageForm, formset=BaseFilFormSet,
    extra=0, can_delete=True,
)
