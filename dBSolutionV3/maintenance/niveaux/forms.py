from decimal import Decimal
from django import forms
from .models import Niveau
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre


class NiveauForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Niveau
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),

            'lave_glace_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'frein_liquide_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'refroidissement_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'pont_niveau_huile_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'boite_niveau_huile_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'moteur_niveau_huile_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'liquide_direction_quantite': forms.NumberInput(attrs={'step': '0.1'}),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop('exemplaire', None)
        super().__init__(*args, **kwargs)

         # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })



        if self.user:
            self.fields["tech_technicien"].initial = self.user
            self.fields["tech_technicien"].disabled = True
            self.fields["tech_societe"].initial = self.user.societe
            self.fields["tech_societe"].disabled = True



    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire  # fallback si pas encore lié

        # Récupération du kilométrage check-up depuis le formulaire
        kilometrage_niveaux = self.cleaned_data.get("kilometres_chassis")

        if voiture and kilometrage_niveaux is not None:
            # 🔒 Sécurité : ne jamais diminuer le kilométrage
            if kilometrage_niveaux < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    f"Le kilométrage des niveaux ({kilometrage_niveaux}) "
                    f"ne peut pas être inférieur au kilométrage actuel de la voiture ({voiture.kilometres_chassis})."
                )

            # ✅ Mettre à jour la voiture si le kilométrage a augmenté
            if kilometrage_niveaux > voiture.kilometres_chassis:
                voiture.kilometres_chassis = kilometrage_niveaux
                voiture.save(update_fields=["kilometres_chassis"])

            # ✅ Mettre à jour le contrôle
            instance.kilometres_chassis = kilometrage_niveaux

            # 🔗 Lier la voiture si ce n'était pas déjà fait
            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture


            # -------- MAIN D'ŒUVRE --------
            heures = self.cleaned_data.get("temps_heures") or 0
            minutes = self.cleaned_data.get("temps_minutes") or 0

            total_minutes = heures * 60 + minutes

            main = instance.main_oeuvre

            if main:
                main.temps_minutes = total_minutes
                main.save(update_fields=["temps_minutes"])
            else:
                main = MainDoeuvre.objects.create(
                    utilisateur=self.user,
                    temps_minutes=total_minutes
                )
                instance.main_oeuvre = main

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance