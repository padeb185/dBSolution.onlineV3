from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from maintenance.autres_interventions.moteur.allumage.models import Allumage
from maintenance.choices import RouesSerrageEtat


class AllumageForm(forms.ModelForm):
    temps_heures = forms.IntegerField(
        required=False,
        min_value=0
    )

    temps_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59
    )

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
        model = Allumage

        exclude = [
                "voiture_exemplaire",
                "immatriculation",
        ]

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

        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        if "kilometrage_variation" in self.fields:

            variation = 0

            if (
                    self.instance
                    and self.instance.pk
                    and self.instance.kilometrage_allumage is not None
                    and self.exemplaire
                    and self.exemplaire.kilometres_chassis is not None
            ):
                variation = (
                        self.instance.kilometrage_allumage
                        - self.exemplaire.kilometres_chassis
                )

            self.fields["kilometrage_variation"].initial = variation



        # ---------------- MAIN-D'ŒUVRE ----------------
        if "main_oeuvre" in self.fields:
            queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(
                utilisateur__is_active=True
            )

            # Recommandé dans une application multi-tenant
            if self.user and self.user.societe:
                queryset = queryset.filter(
                    utilisateur__societe=self.user.societe
                )

            self.fields["main_oeuvre"].queryset = queryset

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input",
            })

        # Temps initial provenant de la main-d'œuvre existante
        if self.instance and self.instance.pk and self.instance.main_oeuvre_id:
            main_oeuvre = self.instance.main_oeuvre
            total_minutes = main_oeuvre.temps_minutes or 0

            self.fields["temps_heures"].initial = total_minutes // 60
            self.fields["temps_minutes"].initial = total_minutes % 60

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

        # ---------------- VALEURS PAR DÉFAUT ----------------
        for field_name in ["prix", "quantite"]:
            if field_name in self.fields:
                self.fields[field_name].initial = 0
                self.fields[field_name].required = False

    def clean_kilometrage_allumage(self):
        km = self.cleaned_data.get("kilometrage_allumage")

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

        if minutes > 59:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        cleaned_data["temps_heures"] = heures
        cleaned_data["temps_minutes"] = minutes

        return cleaned_data

    def save(self, commit=True):
        allumage = super().save(commit=False)

        # ---------------- VÉHICULE ----------------
        km = self.cleaned_data.get("kilometrage_allumage")

        if self.exemplaire:
            allumage.voiture_exemplaire = self.exemplaire

            if km is not None:
                allumage.kilometrage_allumage = km

        # ---------------- TAUX HORAIRE ----------------
        taux_horaire = (
            self.cleaned_data.get("taux_horaire")
            or Decimal("50.00")
        )

        allumage.taux_horaire = taux_horaire

        # ---------------- TEMPS ----------------
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0

        total_minutes = (heures * 60) + minutes

        # ---------------- MAIN-D'ŒUVRE ----------------
        main_oeuvre = self.cleaned_data.get("main_oeuvre")

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

        allumage.main_oeuvre = main_oeuvre

        if commit:
            allumage.save()
            self.save_m2m()

        return allumage

    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise forms.ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )

        return serrage_roues