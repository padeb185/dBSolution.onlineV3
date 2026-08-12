from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat
from .models import Rodage






class RodageForm(forms.ModelForm):
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
        model = Rodage
        exclude = ["pieces"]

        widgets = {
            "maintenance": forms.HiddenInput(),

            "remarques": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": _("Ajoutez des remarques ici..."),
                }
            ),

            "moteur_ajout_huile_quantite": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),

            "liquide_direction_quantite": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),

            "lave_glace_quantite": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),

            "frein_liquide_quantite": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),

            "refroidissement_liquide_quantite": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),
            "pneu_pression_bar_avd": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),
            "pneu_pression_bar_avg": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),
            "pneu_pression_bar_ard": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),
            "pneu_pression_bar_arg": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        # ---------------- CHAMPS FACULTATIFS ----------------
        champs_facultatifs = [
            "moteur_filtre_huile",
            "liquide_direction_etat",
            "liquide_direction_quantite",
            "liquide_direction_qualite",
        ]

        for champ in champs_facultatifs:
            if champ in self.fields:
                self.fields[champ].required = False

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

        # Initialisation depuis la main-d'œuvre existante
        if self.instance and self.instance.main_oeuvre_id:
            main_oeuvre = self.instance.main_oeuvre

            total_minutes = main_oeuvre.temps_minutes or 0

            self.fields["temps_heures"].initial = total_minutes // 60
            self.fields["temps_minutes"].initial = total_minutes % 60

            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = (
                    main_oeuvre.taux_horaire
                )

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

    def clean_kilometres_rodage(self):
        km = self.cleaned_data.get("kilometres_rodage")

        if km is not None and self.exemplaire:
            ancien_km = self.exemplaire.kilometres_chassis or 0

            if km < ancien_km:
                raise ValidationError(
                    _(
                        "Le kilométrage ne peut pas être inférieur "
                        "au kilométrage actuel de la voiture."
                    )
                )

        return km

    def clean(self):
        cleaned_data = super().clean()

        heures = cleaned_data.get("temps_heures") or 0
        minutes = cleaned_data.get("temps_minutes") or 0

        if minutes >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59."),
            )

        if heures == 0 and minutes == 0:
            cleaned_data["temps_heures"] = 0
            cleaned_data["temps_minutes"] = 0

        return cleaned_data

    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise forms.ValidationError(
                _(
                    "Vous devez confirmer que le serrage des roues "
                    "est FAIT avant de valider."
                )
            )

        return serrage_roues

    def save(self, commit=True):
        rodage = super().save(commit=False)

        # ---------------- VÉHICULE ----------------
        km = self.cleaned_data.get("kilometres_rodage")

        if km is not None and self.exemplaire:
            rodage.kilometres_rodage = km
            rodage.voiture_exemplaire = self.exemplaire

        # ---------------- TAUX HORAIRE ----------------
        taux_horaire = self.cleaned_data.get("taux_horaire")

        if taux_horaire is None:
            taux_horaire = Decimal("50.00")

        # ---------------- TEMPS ----------------
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0

        total_minutes = (heures * 60) + minutes

        # ---------------- MAIN-D'ŒUVRE ----------------
        main_oeuvre = rodage.main_oeuvre

        if main_oeuvre:
            main_oeuvre.temps_minutes = total_minutes
            main_oeuvre.taux_horaire = taux_horaire

            if self.user:
                main_oeuvre.utilisateur = self.user

            champs_a_mettre_a_jour = [
                "temps_minutes",
                "taux_horaire",
            ]

            if self.user:
                champs_a_mettre_a_jour.append("utilisateur")

            main_oeuvre.save(
                update_fields=champs_a_mettre_a_jour
            )

        else:
            main_oeuvre = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire,
            )

            rodage.main_oeuvre = main_oeuvre

        # Conserve également le taux dans Rodage
        if hasattr(rodage, "taux_horaire"):
            rodage.taux_horaire = taux_horaire

        # ---------------- SAVE FINAL ----------------
        if commit:
            rodage.save()
            self.save_m2m()

        return rodage
