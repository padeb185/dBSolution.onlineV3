from django import forms
from django.utils import timezone
from .models import Entretien
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre

class EntretienForm(forms.ModelForm):
    temps_main_oeuvre = forms.DecimalField(
        max_digits=6,
        decimal_places=2,
        required=False,
        label="Temps presté (heures)"
    )
    class Meta:
        model = Entretien
        fields = "__all__"
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

        if self.instance and self.instance.pk and self.instance.main_oeuvre:
            self.fields["temps_main_oeuvre"].initial = self.instance.main_oeuvre.temps

        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)

            self.fields["main_oeuvre"].widget.attrs.update({
                "class": "input"
            })

        if "date" in self.fields and self.instance and self.instance.pk and self.instance.date:
            local_dt = timezone.localtime(self.instance.date)
            self.fields['date'].initial = local_dt.strftime('%Y-%m-%d %H:%M:%S')

        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True

            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        voiture = instance.voiture_exemplaire or self.exemplaire

        # -------- KILOMÉTRAGE --------
        km = self.cleaned_data.get("kilometres_chassis")

        if voiture and km is not None:
            if km < voiture.kilometres_chassis:
                raise forms.ValidationError("Kilométrage invalide.")

            if km > voiture.kilometres_chassis:
                voiture.kilometres_chassis = km
                voiture.save(update_fields=["kilometres_chassis"])

            instance.kilometres_chassis = km

            if not instance.voiture_exemplaire:
                instance.voiture_exemplaire = voiture

        # -------- MAIN D'ŒUVRE --------
        temps = self.cleaned_data.get("temps_main_oeuvre")

        if temps is not None:
            main = instance.main_oeuvre

            if main:
                main.temps = temps
                main.save(update_fields=["temps"])
            else:
                main = MainDoeuvre.objects.create(
                    utilisateur=self.user,
                    temps=temps
                )
                instance.main_oeuvre = main

        # -------- SAVE FINAL --------
        if commit:
            instance.save()
            if instance.main_oeuvre:
                instance.main_oeuvre.save()

        return instance