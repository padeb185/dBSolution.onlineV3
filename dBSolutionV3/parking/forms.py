from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Parking


class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ["nom", "largeur_m", "longueur_m", "nombre_lignes", "nombre_emplacements",
                  "box_largeur_m", "box_longueur_m", "largeur_allee_m", "remarques"]
        widgets = {
            "largeur_m": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
            "longueur_m": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
            "nombre_lignes": forms.NumberInput(attrs={"min": "1", "max": "26"}),
            "nombre_emplacements": forms.NumberInput(attrs={"min": "1", "max": "200"}),
            "box_largeur_m": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
            "box_longueur_m": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
            "largeur_allee_m": forms.NumberInput(attrs={"step": "0.01", "min": "1"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nombre_lignes"].help_text = _("Lignes nommées de A à Z (26 au maximum).")
        self.fields["nombre_emplacements"].help_text = _("Emplacements numérotés de 1 à X (50 par défaut, 200 au maximum).")
        for champ in self.fields.values():
            champ.widget.attrs.setdefault("class", "input")
