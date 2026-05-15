from django import forms
from django.core.exceptions import ValidationError
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

        if self.instance and self.instance.main_oeuvre:
            mo = self.instance.main_oeuvre

            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes

        if self.user:
            self.fields["tech_technicien"].initial = self.user
            self.fields["tech_technicien"].disabled = True
            self.fields["tech_societe"].initial = self.user.societe
            self.fields["tech_societe"].disabled = True

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_niveaux")
        voiture = self.exemplaire

        if km is not None and voiture:

            if km < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

            instance.kilometrage_niveaux = km
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