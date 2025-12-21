from django import forms
from django.utils import timezone
from .models import VoiturePneus



class RemplacementPneusForm(forms.Form):
    nouveau_type = forms.ChoiceField(
        choices=VoiturePneus.TypePneus.choices,
        label="Nouveau type de pneus"
    )

    pneus_avant = forms.CharField(
        max_length=15,
        label="Pneus avant",
        help_text="Format xxx/xx/xx"
    )

    pneus_arriere = forms.CharField(
        max_length=15,
        label="Pneus arrière",
        help_text="Format xxx/xx/xx"
    )

    date_remplacement = forms.DateField(
        required=False,
        initial=timezone.now,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Date de remplacement"
    )
