from django import forms
from voiture.voiture_embrayage.models import VoitureEmbrayage


class VoitureEmbrayageForm(forms.ModelForm):
    class Meta:
        model = VoitureEmbrayage
        exclude = ('societe', 'voitures_exemplaires', 'voitures_modeles')