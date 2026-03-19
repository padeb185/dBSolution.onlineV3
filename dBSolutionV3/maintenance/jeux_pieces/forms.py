from decimal import Decimal
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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # 🔹 Initialisation des champs utilisateur si existants et valides
        if self.user:
            if 'utilisateur_auteur' in self.fields:
                self.fields['utilisateur_auteur'].initial = self.user
            if 'utilisateur_role' in self.fields:
                user_role = getattr(self.user, 'role', None)
                valid_choices = [choice[0] for choice in self.fields['utilisateur_role'].choices]
                if user_role in valid_choices:
                    self.fields['utilisateur_role'].initial = user_role

        # 🔹 Préparer une référence à l'exemplaire lié si présent
        self.exemplaire = getattr(self.instance, 'voiture_exemplaire', None)

    def clean_kilometres_chassis(self):
        """
        Validation : le kilométrage ne peut pas être inférieur au kilométrage actuel de la voiture.
        """
        km = self.cleaned_data.get("kilometres_chassis")
        voiture = self.instance.voiture_exemplaire or self.exemplaire
        if km is not None and voiture and km < voiture.kilometres_chassis:
            raise forms.ValidationError(
                _("Le kilométrage du check-up (%(checkup)s) ne peut pas être inférieur au kilométrage actuel de la voiture (%(current)s).") % {
                    "checkup": km,
                    "current": voiture.kilometres_chassis
                }
            )
        return km

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire
        kilometrage_checkup = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_checkup is not None:
            # 🔹 Mise à jour du kilométrage de la voiture si nécessaire
            if kilometrage_checkup > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_checkup
                voiture.save(update_fields=["kilometres_chassis"])

            # 🔹 Mise à jour du contrôle
            instance.kilometres_chassis = kilometrage_checkup

            # 🔹 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        if commit:
            instance.save()

        return instance