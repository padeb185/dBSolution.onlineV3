from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from maintenance.carrosserie_interne.models import CarrosserieInterne
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat


class CarrosserieInterneForm(forms.ModelForm):

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
        model = CarrosserieInterne
        exclude = [
            "societe",
            "maintenance",
            "voiture_exemplaire",
            "created_at",
            "updated_at",
            "total_pieces",
            "total_main_oeuvre",
            "total_peinture",
            "total_htva",
            "total_tva",
            "total_tvac",
            "date",
        ]
        widgets = {
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
                    and self.instance.kilometrage_intervention is not None
            ):
                # À adapter suivant l'endroit où tu stockes
                # le kilométrage précédent
                variation = self.instance.kilometrage_variation or 0

            self.fields["kilometrage_variation"].initial = variation

        # Rendre tous les select non obligatoires
        for name, field in self.fields.items():
            if field.widget.__class__.__name__ == "Select":
                field.required = False

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

        # Initialiser date si le champ existe
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        # Initialiser technicien et société si présents
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

    def clean_kilometrage_intervention(self):
        km = self.cleaned_data.get("kilometrage_intervention")
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

        km = self.cleaned_data.get("kilometrage_intervention")
        voiture = self.exemplaire

        if km is not None and voiture:
            instance.kilometrage_intervention = km
            instance.voiture_exemplaire = voiture

            # -------- MAIN D'ŒUVRE --------
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