from django.forms import inlineformset_factory
from .models import Intervention,MainOeuvre, Peinture
from django import forms





class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
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




class MainOeuvreForm(forms.ModelForm):
    class Meta:
        model = MainOeuvre
        fields = [
            "description",
            "heures",
            "taux_horaire",
        ]
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "heures": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "taux_horaire": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


class PeintureForm(forms.ModelForm):
    class Meta:
        model = Peinture
        fields = [
            "zone",
            "prix",
        ]
        widgets = {
            "zone": forms.TextInput(attrs={"class": "form-control"}),
            "prix": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }




MainOeuvreFormSet = inlineformset_factory(
    Intervention,
    MainOeuvre,
    form=MainOeuvreForm,
    extra=1,
    can_delete=True
)

PeintureFormSet = inlineformset_factory(
    Intervention,
    Peinture,
    form=PeintureForm,
    extra=1,
    can_delete=True
)


