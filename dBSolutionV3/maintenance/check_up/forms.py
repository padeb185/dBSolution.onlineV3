from decimal import Decimal
from django import forms
from .models import ControleGeneral
from django.utils.translation import gettext_lazy as _


class ControleGeneralForm(forms.ModelForm):
    class Meta:
        model = ControleGeneral
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Champs readonly pour le technicien
        self.fields['tech_nom_technicien']
        self.fields['tech_role_technicien']

        self.fields['tech_technicien']
        self.fields['tech_societe']

        # Pré-remplissage si user fourni
        if user:
            self.fields['tech_technicien'].initial = user
            self.fields['tech_societe'].initial = user.societe
            self.fields['tech_nom_technicien'].initial = f"{user.prenom} {user.nom}"
            self.fields['tech_role_technicien'].initial = user.role


    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire  # fallback si pas encore lié

        # Récupération du kilométrage check-up depuis le formulaire
        kilometrage_checkup = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_checkup is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_checkup < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage du check-up ({kilometrage_checkup}) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
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

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance