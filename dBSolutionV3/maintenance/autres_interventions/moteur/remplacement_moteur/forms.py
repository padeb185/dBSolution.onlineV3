from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import RemplacementMoteur


class RemplacementMoteurForm(forms.ModelForm):
    nombre_remplacements_moteurs = forms.IntegerField(
        required=False,
        disabled=True,
        label=_("Nombre de remplacements")
    )

    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = RemplacementMoteur
        exclude = [
            "kilometres_remplacement_moteur",
            "variation_kilometres",
            "kilometres_dernier_entretien",
            "tva",
        ]

        widgets = {
            "date_derniere_intervention": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)

        super().__init__(*args, **kwargs)

        if self.exemplaire:
            if "voiture_exemplaire" in self.fields:
                self.fields["voiture_exemplaire"].initial = self.exemplaire
                self.fields["voiture_exemplaire"].disabled = True

            if "voiture_marque" in self.fields:
                self.fields["voiture_marque"].initial = self.exemplaire.voiture_modele.voiture_marque

            if "voiture_modele" in self.fields:
                self.fields["voiture_modele"].initial = self.exemplaire.voiture_modele

            if "kilometres_chassis" in self.fields:
                self.fields["kilometres_chassis"].initial = self.exemplaire.kilometres_chassis

            if "kilometres_moteur" in self.fields:
                self.fields["kilometres_moteur"].initial = self.exemplaire.kilometres_moteur
                self.fields["kilometres_moteur"].disabled = True
                self.fields["kilometres_moteur"].widget.attrs["readonly"] = True

        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

        if "tech_last_maintained_by" in self.fields:
            self.fields["tech_last_maintained_by"].disabled = True

        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = (
                MainDoeuvre.objects.select_related("utilisateur")
                .filter(utilisateur__is_active=True)
            )
            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        if "remplacement_effectue" in self.fields:
            self.fields["remplacement_effectue"].help_text = _(
                "Cochez pour remplacer le moteur "
                "(remise à zéro automatique du kilométrage)."
            )

        if "nombre_remplacements_moteurs" in self.fields:
            self.fields["nombre_remplacements_moteurs"].disabled = True
            self.fields["nombre_remplacements_moteurs"].widget.attrs["readonly"] = True

            instance_exists = (
                self.instance
                and self.instance.pk
                and RemplacementMoteur.objects.filter(pk=self.instance.pk).exists()
            )

            if instance_exists:
                prochain_numero = self.instance.nombre_remplacements_moteurs

            elif self.exemplaire:
                prochain_numero = (
                    RemplacementMoteur.objects.filter(
                        voiture_exemplaire_id=self.exemplaire.id,
                        remplacement_effectue=True
                    ).count() + 1
                )

            else:
                prochain_numero = 1

            self.fields["nombre_remplacements_moteurs"].initial = prochain_numero
            self.initial["nombre_remplacements_moteurs"] = prochain_numero
            self.fields["nombre_remplacements_moteurs"].widget.attrs["value"] = prochain_numero

    def clean(self):
        cleaned_data = super().clean()

        voiture = self.exemplaire or cleaned_data.get("voiture_exemplaire")
        km_moteur = cleaned_data.get("kilometres_moteur")

        if voiture and km_moteur is not None:
            km_voiture = voiture.kilometres_chassis or 0

            if km_moteur > km_voiture:
                self.add_error(
                    "kilometres_moteur",
                    _("Le kilométrage moteur ne peut pas dépasser celui du véhicule.")
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = self.exemplaire or instance.voiture_exemplaire

        if voiture:
            instance.voiture_exemplaire = voiture

        km_chassis = self.cleaned_data.get("kilometres_chassis")

        if voiture and km_chassis is not None:
            km_voiture = voiture.kilometres_chassis or 0

            if km_chassis < km_voiture:
                raise ValidationError(_("Kilométrage invalide"))

            voiture.kilometres_chassis = km_chassis
            voiture.save(update_fields=["kilometres_chassis"])

            instance.kilometres_chassis = km_chassis

        instance_exists = (
            instance.pk
            and RemplacementMoteur.objects.filter(pk=instance.pk).exists()
        )

        if not instance_exists and voiture:
            instance.nombre_remplacements_moteurs = (
                RemplacementMoteur.objects.filter(
                    voiture_exemplaire_id=voiture.id,
                    remplacement_effectue=True
                ).count() + 1
            )

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