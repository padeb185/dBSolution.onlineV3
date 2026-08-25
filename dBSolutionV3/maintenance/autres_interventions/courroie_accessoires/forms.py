from datetime import timedelta
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import CourroieAccessoires



class CourroieAccessoiresForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(
            attrs={
                "readonly": "readonly",
                "class": "input",
            }
        ),
    )

    class Meta:
        model = CourroieAccessoires
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

        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        if "kilometrage_variation" in self.fields:

            variation = 0

            if (
                    self.instance
                    and self.instance.pk
                    and self.instance.kilometrage_access is not None
                    and self.exemplaire
                    and self.exemplaire.kilometres_chassis is not None
            ):
                variation = (
                        self.instance.kilometrage_access
                        - self.exemplaire.kilometres_chassis
                )

            self.fields["kilometrage_variation"].initial = variation



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

    def clean_kilometres_courroie_access(self):
        km = self.cleaned_data["kilometres_access"]

        if km < self.exemplaire.kilometres_chassis:
            raise ValidationError(
                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel du véhicule.")
            )

        return km

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        km_courroie = cleaned.get("kilometrage_access")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)

        if not voiture or km_courroie in [None, ""]:
            return cleaned

        try:
            km_courroie = Decimal(str(km_courroie))
        except:
            raise ValidationError({
                "kilometrage_access": _("Kilométrage invalide")
            })

        km_voiture = voiture.kilometres_chassis or Decimal("0")

        if km_courroie < km_voiture:
            raise ValidationError({
                "kilometrage_access": _(
                    "Le kilométrage doit être ≥ %(km)s"
                ) % {"km": km_voiture}
            })

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = self.exemplaire
        if voiture:
            instance.voiture_exemplaire = voiture

        km = self.cleaned_data.get("kilometrage_access")
        if km is not None:
            instance.kilometrage_courroie_access = km

            # =====================================
            # MAIN D'ŒUVRE
            # =====================================
            heures = self.cleaned_data.get("temps_heures") or 0
            minutes = self.cleaned_data.get("temps_minutes") or 0
            taux_horaire = self.cleaned_data.get("taux_horaire")

            total_minutes = heures * 60 + minutes

            # Ne pas remplacer une valeur choisie par 50
            if taux_horaire is None:
                taux_horaire = 50

            main = instance.main_oeuvre

            if main:
                main.temps_minutes = total_minutes
                main.taux_horaire = taux_horaire

                main.save(
                    update_fields=[
                        "temps_minutes",
                        "taux_horaire",
                    ]
                )

            else:
                main = MainDoeuvre.objects.create(
                    utilisateur=self.user,
                    temps_minutes=total_minutes,
                    taux_horaire=taux_horaire,
                )

                instance.main_oeuvre = main

        return instance