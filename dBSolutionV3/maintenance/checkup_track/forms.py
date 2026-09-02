from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CheckupTrack
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import RouesSerrageEtat




class CheckupTrackForm(forms.ModelForm):

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
        model = CheckupTrack
        fields = "__all__"
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),

            "pneu_epaisseur_avd": forms.NumberInput(attrs={
                "step": "0.5",
                "min": "0",
            }),
            "pneu_epaisseur_avg": forms.NumberInput(attrs={
                "step": "0.5",
                "min": "0",
            }),
            "pneu_epaisseur_ard": forms.NumberInput(attrs={
                "step": "0.5",
                "min": "0",
            }),
            "pneu_epaisseur_arg": forms.NumberInput(attrs={
                "step": "0.5",
                "min": "0",
            }),
            "pneu_pression_bar_avd": forms.NumberInput(attrs={"step": "0.1"}),
            "pneu_pression_bar_avg": forms.NumberInput(attrs={"step": "0.1"}),
            "pneu_pression_bar_ard": forms.NumberInput(attrs={"step": "0.1"}),
            "pneu_pression_bar_arg": forms.NumberInput(attrs={"step": "0.1"}),
            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "class": "bg-gray-100 cursor-not-allowed",
                }
            ),
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

            # =========================
            # INSTANCE EXISTANTE
            # =========================
            if self.instance:

                ancien_km = (
                        self.instance.kilometres_chassis or 0
                )

                nouveau_km = (
                    self.instance.kilometrage_checkup_track
                )

                if nouveau_km is not None:
                    variation = nouveau_km - ancien_km

            self.fields["kilometrage_variation"].initial = variation

        # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

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

        self.fields["nettoyage_interieur_plastiques"].required = False

        # ------- Récupération du temps de main d'oeuvre ------#
        if self.instance and self.instance.main_oeuvre:
            mo = self.instance.main_oeuvre

            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes

    def clean_kilometrage_checkup_track(self):
        km = self.cleaned_data.get("kilometrage_checkup_track")
        exemplaire = self.exemplaire

        if km is not None and exemplaire:
            if km < exemplaire.kilometres_chassis:
                raise ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

        return km

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_checkup_track")
        voiture = self.exemplaire

        if km is not None and voiture:
            instance.kilometrage_checkup_track = km
            instance.voiture_exemplaire = voiture

            if km > voiture.kilometres_chassis:
                voiture.kilometres_chassis = km
                voiture.kilometres_dernier_entretien = km
                voiture.date_derniere_intervention = timezone.now().date()
                voiture.update_kilometres()
                voiture.save()

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




    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise forms.ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )

        return serrage_roues