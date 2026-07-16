from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import Admission


class AdmissionForm(forms.ModelForm):
    temps_heures = forms.IntegerField(
        required=False,
        min_value=0,
        label=_("Heures"),
    )

    temps_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59,
        label=_("Minutes"),
    )

    class Meta:
        model = Admission
        fields = "__all__"

        widgets = {
            "maintenance": forms.HiddenInput(),
            "remarques": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": _("Ajoutez des remarques ici..."),
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        # ---------------- MAIN-D'ŒUVRE ----------------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = (
                MainDoeuvre.objects
                .select_related("utilisateur")
                .filter(utilisateur__is_active=True)
            )

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input",
            })

        if self.instance and self.instance.main_oeuvre_id:
            main_oeuvre = self.instance.main_oeuvre

            self.fields["temps_heures"].initial = (
                main_oeuvre.temps_minutes or 0
            ) // 60

            self.fields["temps_minutes"].initial = (
                main_oeuvre.temps_minutes or 0
            ) % 60

        # ---------------- DATE ----------------
        if (
            "date" in self.fields
            and self.instance
            and self.instance.pk
            and self.instance.date
        ):
            local_dt = timezone.localtime(self.instance.date)

            self.fields["date"].initial = local_dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        # ---------------- TECHNICIEN ----------------
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

        # ---------------- PRIX / QUANTITÉS ----------------
        for field_name in ["prix", "quantite"]:
            if field_name in self.fields:
                self.fields[field_name].required = False

                if not self.is_bound:
                    self.fields[field_name].initial = 0

    def clean_kilometrage_admission(self):
        km = self.cleaned_data.get("kilometrage_admission")

        if km is not None and self.exemplaire:
            ancien_km = self.exemplaire.kilometres_chassis or 0

            if km < ancien_km:
                raise ValidationError(
                    _("Le kilométrage ne peut pas diminuer.")
                )

        return km

    def clean(self):
        cleaned_data = super().clean()

        heures = cleaned_data.get("temps_heures") or 0
        minutes = cleaned_data.get("temps_minutes") or 0

        if minutes >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        if heures == 0 and minutes == 0:
            cleaned_data["temps_heures"] = 0
            cleaned_data["temps_minutes"] = 0

        return cleaned_data

    def save(self, commit=True):
        admission = super().save(commit=False)

        # ---------------- VÉHICULE ----------------
        km = self.cleaned_data.get("kilometrage_admission")

        if km is not None and self.exemplaire:
            admission.kilometrage_admission = km
            admission.voiture_exemplaire = self.exemplaire

        # Le taux sélectionné dans le formulaire Admission
        taux_horaire = (
            self.cleaned_data.get("taux_horaire")
            or Decimal("50.00")
        )

        # ---------------- TEMPS ----------------
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0

        total_minutes = (heures * 60) + minutes

        # ---------------- MAIN-D'ŒUVRE ----------------
        main_oeuvre = admission.main_oeuvre

        if main_oeuvre:
            main_oeuvre.temps_minutes = total_minutes
            main_oeuvre.taux_horaire = taux_horaire

            main_oeuvre.save(
                update_fields=[
                    "temps_minutes",
                    "taux_horaire",
                ]
            )

        else:
            main_oeuvre = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire,
            )

            admission.main_oeuvre = main_oeuvre

        # Conserve aussi le taux dans Admission
        admission.taux_horaire = taux_horaire

        if commit:
            admission.save()
            self.save_m2m()

        return admission