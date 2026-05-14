from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import Admission





class AdmissionForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Admission
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

        # -------- Temps --------
        heures = cleaned.get("temps_heures") or 0
        minutes = cleaned.get("temps_minutes") or 0

        if minutes >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        km_admission = cleaned.get("kilometrage_admission")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)

        if not voiture or km_admission in [None, ""]:
            return cleaned

        try:
            km_admission = Decimal(str(km_admission))
        except:
            raise ValidationError({
                "kilometrage_admission": _("Kilométrage invalide")
            })

        km_voiture = voiture.kilometres_chassis or Decimal("0")

        if km_admission < km_voiture:
            raise ValidationError({
                "kilometrage_admission": _(
                    "Le kilométrage doit être ≥ %(km)s"
                ) % {"km": km_voiture}
            })

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km_admission = self.cleaned_data.get("kilometrage_admission")

        if km_admission not in [None, ""]:
            km_admission = Decimal(str(km_admission))

            voiture = instance.voiture_exemplaire

            if voiture:
                voiture.refresh_from_db(fields=["kilometres_chassis"])

                km_voiture = voiture.kilometres_chassis or Decimal("0")

                # 🔒 validation métier
                if km_admission < km_voiture:
                    raise ValidationError(
                        "Le kilométrage ne peut pas être inférieur au véhicule"
                    )

                # 🔥 SOURCE UNIQUE
                voiture.kilometres_chassis = km_admission
                voiture.save(update_fields=["kilometres_chassis"])

            # 🔁 sync alternateur
            instance.kilometres_chassis = km_admission
            instance.kilometrage_admission = km_admission

        # ---------------- MAIN D’ŒUVRE ----------------
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