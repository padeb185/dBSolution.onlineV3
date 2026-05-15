from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import ListView
from django_tenants.utils import tenant_context
from .models import NettoyageExterieur
from maindoeuvre.models import MainDoeuvre


class NettoyageExterieurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)
    # Déclarer explicitement le champ date
    date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'readonly': 'readonly', 'class': 'form-input'},
            format='%Y-%m-%d %H:%M:%S'  # format affiché dans le form
        )
    )

    class Meta:
        model = NettoyageExterieur
        exclude = ['maintenance', 'voiture_exemplaire']
        widgets = {
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Ajoutez des remarques ici..."
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

        if self.instance and self.instance.pk and self.instance.date:
            # ✅ convertir en heure locale et formatter comme string
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

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_net_ext")
        voiture = self.exemplaire

        if km is not None and voiture:

            if km < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

            instance.kilometrage_net_ext = km
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