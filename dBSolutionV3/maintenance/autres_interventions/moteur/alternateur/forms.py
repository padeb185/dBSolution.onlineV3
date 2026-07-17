from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre

from .models import Alternateur


class AlternateurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(
        required=False,
        min_value=0
    )

    temps_minutes = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=59
    )

    class Meta:
        model = Alternateur

        exclude = (
            "alternateur_tva_achat",
            "alternateur_prix_vente_htva",
            "alternateur_tva_vente",
            "alternateur_prix_ttc",
            "alternateur_marge",
            "courroie_accessoires_tva_achat",
            "courroie_accessoires_prix_ttc",
            "courroie_accessoires_prix_vente_htva",
            "courroie_accessoires_tva_vente",
        )

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

    def clean_kilometrage_alte(self):
        km = self.cleaned_data.get("kilometrage_alte")

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
        controle_alternateur = super().save(commit=False)

        # ---------------- VÉHICULE ----------------
        km = self.cleaned_data.get("kilometrage_alte")

        if self.exemplaire:
            controle_alternateur.voiture_exemplaire = self.exemplaire

            if km is not None:
                controle_alternateur.kilometrage_alte = km

        # ---------------- TAUX HORAIRE ----------------
        taux_horaire = (
            self.cleaned_data.get("taux_horaire")
            or Decimal("50.00")
        )

        controle_alternateur.taux_horaire = taux_horaire

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

        controle_alternateur.main_oeuvre = main_oeuvre

        if commit:
            controle_alternateur.save()
            self.save_m2m()

        return controle_alternateur