from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import RemplacementMoteur





class RemplacementMoteurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = RemplacementMoteur

        # champs calculés / auto-gérés exclus
        exclude = [
            "kilometres_remplacement_moteur",
            "variation_kilometres",
            "kilometres_dernier_entretien",
        ]

        widgets = {
            "date_derniere_intervention": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        # -----------------------
        # MAIN D'ŒUVRE
        # -----------------------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

        # -----------------------
        # AUTO-REMPLISSAGE VOITURE
        # -----------------------
        if self.exemplaire:
            if "voiture_exemplaire" in self.fields:
                self.fields["voiture_exemplaire"].initial = self.exemplaire

            if "voiture_marque" in self.fields:
                self.fields["voiture_marque"].initial = self.exemplaire.voiture_modele.voiture_marque

            if "voiture_modele" in self.fields:
                self.fields["voiture_modele"].initial = self.exemplaire.voiture_modele

            if "kilometres_chassis" in self.fields:
                self.fields["kilometres_chassis"].initial = self.exemplaire.kilometres_chassis

            if "immatriculation" in self.fields:
                self.fields["immatriculation"].initial = self.exemplaire.immatriculation





        # -----------------------
        # TECHNICIEN AUTO
        # -----------------------
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True




        # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        if "tech_last_maintained_by" in self.fields:
            self.fields["tech_last_maintained_by"].disabled = True




        # -----------------------
        # CHAMPS CALCULÉS
        # -----------------------
        if "kilometres_moteur" in self.fields:
            self.fields["kilometres_moteur"].disabled = True





        # -----------------------
        # UX
        # -----------------------
        if "remplacement_effectue" in self.fields:
            self.fields["remplacement_effectue"].help_text = _(
                "Cochez pour remplacer le moteur (remise à zéro automatique du kilométrage)."
            )


    # =========================================================
    # VALIDATION PROPRE
    # =========================================================
    def clean(self):
        cleaned_data = super().clean()

        voiture = cleaned_data.get("voiture_exemplaire") or self.exemplaire
        km_moteur = cleaned_data.get("kilometres_moteur")

        if voiture and km_moteur is not None:

            km_voiture = voiture.kilometres_chassis or 0

            if km_moteur > km_voiture:
                self.add_error(
                    "kilometres_moteur",
                    _("Le kilométrage moteur ne peut pas dépasser celui du véhicule.")
                )

        return cleaned_data
    # =========================================================
    # SAUVEGARDE MÉTIER
    # =========================================================
    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometres_remplacement_moteur")
        voiture = self.exemplaire

        if km is not None and voiture:

            if km < voiture.kilometres_chassis:
                raise forms.ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

            instance.kilometres_remplacement_moteur = km
            instance.voiture_exemplaire = voiture

        # MAIN D’ŒUVRE
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0

        total_minutes = heures * 60 + minutes

        main = instance.main_oeuvre

        if main:
            main.temps_minutes = total_minutes
            main.save(update_fields=["temps_minutes"])
        elif self.user:
            main = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes
            )
            instance.main_oeuvre = main

        if self.user:
            instance.assign_technicien(self.user)

        if commit:
            instance.save()

        return instance