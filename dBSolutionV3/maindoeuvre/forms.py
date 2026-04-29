from django import forms
from maindoeuvre.models import MainDoeuvre


class MainDoeuvreForm(forms.ModelForm):

    class Meta:
        model = MainDoeuvre
        fields = '__all__'

        widgets = {
            "utilisateur": forms.Select(attrs={"class": "input"}),
            "temps": forms.NumberInput(attrs={
                "class": "input",
                "step": "0.25",
                "min": "0"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 filtrer les utilisateurs actifs uniquement
        self.fields["utilisateur"].queryset = (
            self.fields["utilisateur"]
            .queryset
            .filter(is_active=True)
        )

    def clean_temps(self):
        temps = self.cleaned_data["temps"]
        if temps <= 0:
            raise forms.ValidationError("Le temps doit être supérieur à 0.")
        return temps