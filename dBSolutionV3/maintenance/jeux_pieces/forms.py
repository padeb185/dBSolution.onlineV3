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

    def __init__(self, *args, **kwargs):
        # ✅ Extraire l'utilisateur si fourni
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 🔹 Exemple : rendre certains champs readonly selon le rôle
        if self.user:
            # Par exemple, le technicien ne peut pas changer le kilométrage initial
            # self.fields['kilometres_chassis'].disabled = True
            pass

        # 🔹 Préparer une référence à l'exemplaire si déjà lié
        self.exemplaire = getattr(self.instance, 'voiture_exemplaire', None)

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire

        # 🔹 Récupération du kilométrage check-up depuis le formulaire
        kilometrage_checkup = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_checkup is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_checkup < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    _("Le kilométrage du check-up ({checkup}) ne peut pas être inférieur au kilométrage actuel de la voiture ({current}).").format(
                        checkup=kilometrage_checkup,
                        current=voiture.kilometres_chassis
                    )
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_checkup > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_checkup
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_checkup

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        # 🔹 Sauvegarde finale
        if commit:
            instance.save()

        return instance