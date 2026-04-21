from django import forms
from .models import MoteurVoiture


class MoteurVoitureAdminForm(forms.ModelForm):

    class Meta:
        model = MoteurVoiture
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        cylindree = cleaned_data.get("cylindree_l")
        puissance = cleaned_data.get("puissance_ch")
        couple = cleaned_data.get("couple_nm")

        # ⚠️ cohérence technique simple
        if cylindree and cylindree <= 0:
            self.add_error("cylindree_l", "La cylindrée doit être supérieure à 0.")

        if puissance and puissance < 0:
            self.add_error("puissance_ch", "La puissance ne peut pas être négative.")

        if couple and couple < 0:
            self.add_error("couple_nm", "Le couple ne peut pas être négatif.")

        return cleaned_data