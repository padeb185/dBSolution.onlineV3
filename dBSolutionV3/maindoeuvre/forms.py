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
            "utilisateur": forms.Select(attrs={
                "class": "border rounded px-4 py-2 w-full",
            }),

            "temps_minutes": forms.NumberInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "step": "1",
                "min": "1",
                "placeholder": _("Temps en minutes"),
            }),

            "descriptif": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 4,
            }),
        }

        labels = {
            "utilisateur": _("Utilisateur"),
            "temps_minutes": _("Temps (minutes)"),
            "descriptif": _("Descriptif"),
            "remarques": _("Remarques"),
        }

    def __init__(self, *args, **kwargs):
        # Accepte l'argument optionnel "user"
        self.user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

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