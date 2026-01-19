from django import forms
from voiture.voiture_embrayage.models import VoitureEmbrayage


class VoitureEmbrayageForm(forms.ModelForm):
    class Meta:
        model = VoitureEmbrayage
        fields = '__all__'