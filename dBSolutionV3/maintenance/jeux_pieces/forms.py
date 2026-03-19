from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ControleJeuxPieces


class ControleJeuxPiecesForm(forms.ModelForm):
    class Meta:
        model = ControleJeuxPieces
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),
        }

    def __init__(self, *args, user=None, exemplaire=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.exemplaire = exemplaire

    # ✅ VALIDATION UNIQUE
    def clean(self):
        cleaned_data = super().clean()

        voiture = self.instance.voiture_exemplaire or self.exemplaire
        km_checkup = cleaned_data.get("kilometres_chassis")

        if voiture and km_checkup is not None:
            if km_checkup < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    _("Le kilométrage ne peut pas être inférieur au kilométrage actuel.")
                )

        return cleaned_data

    # ✅ LOGIQUE MÉTIER UNIQUE
    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = instance.voiture_exemplaire or self.exemplaire
        km_checkup = self.cleaned_data.get("kilometres_chassis")

        if voiture and km_checkup is not None:

            # Mise à jour voiture si augmentation
            if km_checkup > voiture.kilometres_chassis:
                voiture.kilometres_chassis = km_checkup
                voiture.save(update_fields=["kilometres_chassis"])

            # Mise à jour contrôle
            instance.kilometres_chassis = km_checkup

            # Lien voiture
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        if commit:
            instance.save()

        return instance