from decimal import Decimal
from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from .models import Turbo


class TurboForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    class Meta:
        model = Turbo
        fields = "__all__"
        widgets = {
            "maintenance": forms.HiddenInput(),
            "remarques": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": _("Ajoutez des remarques ici...")
            }),
        }

    def __init__(self, *args, user=None, exemplaire=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.exemplaire = exemplaire

        # -------- MAIN D'ŒUVRE QUERYSET --------
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        # -------- DATE --------
        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields["date"].initial = local_dt.strftime("%Y-%m-%d %H:%M:%S")

        # -------- TECHNICIEN / SOCIETE --------
        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

        # -------- DEFAULT VALUES --------
        for f in ["prix", "quantite"]:
            if f in self.fields:
                self.fields[f].initial = 0
                self.fields[f].required = False

    # 🔴 VALIDATION PROPRE (AU LIEU DE save)
    def clean(self):
        cleaned_data = super().clean()

        voiture = self.exemplaire or self.instance.voiture_exemplaire
        km = cleaned_data.get("kilometres_chassis")

        if voiture and km is not None:
            # sécurité logique
            if km < voiture.kilometres_chassis:
                self.add_error(
                    "kilometres_chassis",
                    _(
                        f"Le kilométrage du turbo ({km}) "
                        f"ne peut pas être inférieur au kilométrage du véhicule ({voiture.kilometres_chassis})."
                    )
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        voiture = self.exemplaire or instance.voiture_exemplaire
        km = self.cleaned_data.get("kilometres_chassis")

        if voiture and km is not None:
            # mise à jour voiture uniquement si augmentation
            if km > voiture.kilometres_chassis:
                voiture.kilometres_chassis = km
                voiture.save(update_fields=["kilometres_chassis"])

            instance.kilometres_chassis = km

            if not instance.voiture_exemplaire:
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