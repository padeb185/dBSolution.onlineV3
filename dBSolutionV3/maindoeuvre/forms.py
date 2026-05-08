from django import forms
from maindoeuvre.models import MainDoeuvre
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MainDoeuvre





class MainDoeuvreForm(forms.ModelForm):

    class Meta:
        model = MainDoeuvre

        fields = [
            "utilisateur",
            "temps_minutes",
            "descriptif",
            "remarques",
        ]

        widgets = {

            # -------------------------
            # UTILISATEUR
            # -------------------------
            "utilisateur": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            # -------------------------
            # TEMPS
            # -------------------------
            "temps_minutes": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "step": "1",
                "min": "0",
                "placeholder": "Temps en minutes"
            }),
        }

        labels = {
            "utilisateur": _("Utilisateur"),
            "temps_minutes": _("Temps (minutes)"),
            "descriptif": _("Descriptif"),
            "remarques": _("Remarques"),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # 🔥 utilisateurs actifs uniquement
        if "utilisateur" in self.fields:
            self.fields["utilisateur"].queryset = (
                self.fields["utilisateur"]
                .queryset
                .filter(is_active=True)
            )

    def clean_temps_minutes(self):

        temps = self.cleaned_data.get("temps_minutes")

        if temps is None or temps <= 0:
            raise forms.ValidationError(
                _("Le temps doit être supérieur à 0.")
            )

        return temps