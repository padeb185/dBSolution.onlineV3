from decimal import Decimal

from django import forms
from maintenance.obligatoires import ChampsObligatoiresMaintenanceMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat

from .models import Crevaison




class CrevaisonForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = Crevaison
        exclude = [
            "voiture_exemplaire",
            "maintenance",
            "kilometres_boite",
            "kilometres_moteur",
            "kilometres_embrayage",
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
        ]
        widgets = {
            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "class": "bg-gray-100 cursor-not-allowed",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        # Le véhicule doit être connu pour la validation du modèle (Crevaison.clean)
        if self.exemplaire is not None:
            self.instance.voiture_exemplaire = self.exemplaire

        # Crevaison : widgets
        for nom in ("reparation_prix", "pneu_prix", "valve_prix", "masses_prix"):
            if nom in self.fields:
                self.fields[nom].widget.attrs.update({"step": "0.01", "min": "0", "inputmode": "decimal"})
        if "pression_bar" in self.fields:
            self.fields["pression_bar"].widget.attrs.update({"step": "0.05", "min": "0", "inputmode": "decimal"})
        if "remarques" in self.fields:
            self.fields["remarques"].widget = forms.Textarea(attrs={"rows": 3})
        if "pneu_nouveau" in self.fields:
            from voiture.voiture_pneus.models import VoiturePneus
            self.fields["pneu_nouveau"].queryset = VoiturePneus.objects.all()
        # Choix en boutons radio (solution et type de réparation)
        if "solution" in self.fields:
            self.fields["solution"].widget = forms.RadioSelect(choices=self.fields["solution"].choices)
        if "type_reparation" in self.fields:
            self.fields["type_reparation"].widget = forms.RadioSelect(
                choices=[c for c in self.fields["type_reparation"].choices if c[0]])

        # Le kilométrage "avant" est affiché mais jamais modifiable
        if "kilometres_chassis" in self.fields:
            self.fields["kilometres_chassis"].disabled = True

        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        variation = 0
        if (
            self.instance.pk
            and self.instance.kilometrage_crevaison is not None
        ):
            variation = (
                self.instance.kilometrage_crevaison
                - (self.instance.kilometres_chassis or 0)
            )
        self.fields["kilometrage_variation"].initial = variation

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)
            self.fields["main_oeuvre"].widget.attrs.update({"class": "input"})

        if self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = mo.taux_horaire

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def clean_kilometrage_crevaison(self):
        km = self.cleaned_data.get("kilometrage_crevaison")

        if km is None or not self.exemplaire:
            return km

        # Création : comparaison au véhicule.
        # Modification : comparaison au kilométrage figé avant ce contrôle.
        if self.instance.pk:
            minimum = self.instance.kilometres_chassis or 0
        else:
            minimum = self.exemplaire.kilometres_chassis or 0

        if km < minimum:
            raise ValidationError(
                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                % {"km": minimum}
            )
        return km

    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )
        return serrage_roues

    # ======================================================
    # SAUVEGARDE
    # ======================================================
    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.exemplaire is not None:
            instance.voiture_exemplaire = self.exemplaire

        # -------- MAIN D'ŒUVRE --------
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0
        taux_horaire = self.cleaned_data.get("taux_horaire")
        total_minutes = heures * 60 + minutes

        main = instance.main_oeuvre
        if main:
            main.temps_minutes = total_minutes
            if taux_horaire is not None:
                main.taux_horaire = taux_horaire
            main.save(update_fields=["temps_minutes", "taux_horaire"])
        else:
            main = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire or Decimal("50.00"),
            )
            instance.main_oeuvre = main

        if commit:
            instance.save()
            self.save_m2m()

        return instance
