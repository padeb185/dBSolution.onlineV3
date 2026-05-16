from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import Alternateur


class AlternateurForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Alternateur
        exclude =('alternateur_tva_achat',
                  'alternateur_prix_vente_htva',
                  'alternateur_tva_vente',
                  'alternateur_prix_ttc',
                  'alternateur_marge',
                  'courroie_accessoires_tva_achat',
                  'courroie_accessoires_prix_ttc',
                  'courroie_accessoires_prix_vente_htva',
                  'courroie_accessoires_tva_vente'
                  )
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

                # Initialiser prix et quantite si les champs existent
        for f in ["prix", "quantite"]:
            if f in self.fields:
                self.fields[f].initial = 0
                self.fields[f].required = False

    def clean_kilometrage_alte(self):
        km = self.cleaned_data.get("kilometrage_alte")
        exemplaire = self.exemplaire

        if km is not None and exemplaire:
            if km < exemplaire.kilometres_chassis:
                raise ValidationError(
                    "Le kilométrage ne peut pas diminuer."
                )

        return km

    def clean(self):
        cleaned = super().clean()

        # -------- Temps --------
        heures = cleaned.get("temps_heures") or 0
        minutes = cleaned.get("temps_minutes") or 0

        if minutes >= 60:
            self.add_error(
                "temps_minutes",
                _("Les minutes ne peuvent pas dépasser 59.")
            )

        km_alternateur = cleaned.get("kilometrage_alte")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)

        if not voiture or km_alternateur in [None, ""]:
            return cleaned

        try:
            km_alternateur = Decimal(str(km_alternateur))
        except:
            raise ValidationError({
                "kilometrage_admission": _("Kilométrage invalide")
            })

        km_voiture = voiture.kilometres_chassis or Decimal("0")

        if km_alternateur < km_voiture:
            raise ValidationError({
                "kilometrage_alte": _(
                    "Le kilométrage doit être ≥ %(km)s"
                ) % {"km": km_voiture}
            })

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_alte")
        voiture = self.exemplaire

        if km is not None and voiture:
            instance.kilometrage_alte = km
            instance.voiture_exemplaire = voiture

        # ---------------- MAIN D’ŒUVRE ----------------
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