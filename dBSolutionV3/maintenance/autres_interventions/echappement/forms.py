from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from maindoeuvre.models import MainDoeuvre
from .models import Echappement
from django.utils.translation import gettext_lazy as _




class ControleEchappementForm(forms.ModelForm):
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
        model = Echappement
        fields = "__all__"
        exclude = ["voiture_exemplaire",]
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
                    and self.instance.kilometrage_echappement is not None
                    and self.exemplaire
                    and self.exemplaire.kilometres_chassis is not None
            ):
                variation = (
                        self.instance.kilometrage_echappement
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

                # Véhicule transmis par la vue
                if self.exemplaire:
                    self.instance.voiture_exemplaire = self.exemplaire

                    if hasattr(self.instance, "kilometres_chassis"):
                        self.instance.kilometres_chassis = (
                                self.exemplaire.kilometres_chassis or 0
                        )

    def clean_kilometrage_controle_echappement(self):
        km = self.cleaned_data.get("kilometrage_echappement")
        exemplaire = self.exemplaire

        if km is not None and exemplaire:
            if km < exemplaire.kilometres_chassis:
                raise ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

        return km

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_echappement")
        voiture = self.exemplaire

        if km is not None and voiture:
            instance.kilometrage_echappement = km
            instance.voiture_exemplaire = voiture

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

        # Sauvegarde finale
        if commit:
            instance.save()

        return instance