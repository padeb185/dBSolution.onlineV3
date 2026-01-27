from django import forms
from django.utils import timezone
from .models import VoiturePneus
from django import forms
from .models import VoiturePneus, TypePneus



class RemplacementPneusForm(forms.Form):
    type_pneus = forms.ChoiceField(
        choices=TypePneus.choices,
        label="Type de pneus"
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
