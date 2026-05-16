from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import Turbo


class TurboForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Turbo
        fields = "__all__"
        widgets = {
            "maintenance": forms.HiddenInput(),
            "remarques": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": _("Ajoutez des remarques ici...")
            }),
        }

    def __init__(self, *args, user=None, exemplaire=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.exemplaire = exemplaire

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


        # -------- DATE --------
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields["date"].initial = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        # -------- TECHNICIEN / SOCIETE --------
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

        # -------- DEFAULT VALUES --------
        for f in ["prix", "quantite"]:
            if f in self.fields:
                self.fields[f].initial = 0
                self.fields[f].required = False



    def clean(self):

        cleaned_data = super().clean()

        # Temps
        h = cleaned_data.get("temps_heures") or 0
        m = cleaned_data.get("temps_minutes") or 0

        if m >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometres_turbo")
        voiture = self.exemplaire

        if km is not None and voiture:

            if km < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

            instance.kilometres_turbo = km
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

        if commit:
            instance.save()

        return instance