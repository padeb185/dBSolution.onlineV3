from datetime import timedelta
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import CourroieDistribution


class CourroieDistributionForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = CourroieDistribution
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
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


        # ✅ initialisation date seulement si le champ existe
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Initialiser les champs technicien et société si présents
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

                # Initialiser prix et quantite si les champs existent
        for f in ["prix", "quantite"]:
            if f in self.fields:
                self.fields[f].initial = 0
                self.fields[f].required = False

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        km_courroie = cleaned.get("kilometrage_cour")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)

        if not voiture or km_courroie in [None, ""]:
            return cleaned

        try:
            km_courroie = Decimal(str(km_courroie))
        except:
            raise ValidationError({
                "kilometrage_admission": _("Kilométrage invalide")
            })

        km_voiture = voiture.kilometres_chassis or Decimal("0")

        if km_courroie < km_voiture:
            raise ValidationError({
                "kilometrage_cour": _(
                    "Le kilométrage doit être ≥ %(km)s"
                ) % {"km": km_voiture}
            })

        return cleaned


    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_cour")
        voiture = self.exemplaire

        if km is not None and voiture:

            if km < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

            instance.kilometrage_cour = km
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