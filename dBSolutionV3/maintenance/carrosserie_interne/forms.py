from django import forms
from maintenance.carrosserie_interne.models import CarrosserieInterne


class CarrosserieInterneForm(forms.ModelForm):
    class Meta:
        model = CarrosserieInterne
        fields = "__all__"

        widgets = {
            "societe": forms.Select(attrs={"class": "form-select"}),
            "voiture_exemplaire": forms.Select(attrs={"class": "form-select"}),

            "kilometres_chassis": forms.NumberInput(attrs={"class": "form-input"}),
            "kilometrage_intervention": forms.NumberInput(attrs={"class": "form-input"}),

            "remarques": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 4
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 Appliquer un style par défaut à tous les champs
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-input")


