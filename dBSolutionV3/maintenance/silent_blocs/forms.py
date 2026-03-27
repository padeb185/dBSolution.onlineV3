from decimal import Decimal
from django import forms
from .models import SilentBloc
from django.utils.translation import gettext_lazy as _


class SilentBlocForm(forms.ModelForm):
    class Meta:
        model = SilentBloc
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["tech_technicien"].initial = self.user
            self.fields["tech_technicien"].disabled = True
            self.fields["tech_societe"].initial = self.user.societe
            self.fields["tech_societe"].disabled = True



    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire  # fallback si pas encore lié

        # Récupération du kilométrage check-up depuis le formulaire
        kilometrage_silent= self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_silent is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_silent < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage du check-up ({kilometrage_silent}) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_silent > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_silent
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_silent

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance