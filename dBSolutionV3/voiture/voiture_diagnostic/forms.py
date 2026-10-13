from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Diagnostic, DiagnosticCode


class DiagnosticForm(forms.ModelForm):
    # Temps de main-d'œuvre (enregistré dans MainDoeuvre, comme pour les checkups)
    temps_heures = forms.IntegerField(label=_("Heures"), required=False, min_value=0)
    temps_minutes = forms.IntegerField(label=_("Minutes"), required=False, min_value=0, max_value=59)

    class Meta:
        model = Diagnostic
        fields = ("voiture_exemplaire", "date_diagnostic", "kilometrage", "description", "taux_horaire")
        widgets = {
            "date_diagnostic": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)

        # Temps de main-d'œuvre existant
        if self.instance.pk and self.instance.main_oeuvre:
            self.fields["temps_heures"].initial = self.instance.main_oeuvre.heures
            self.fields["temps_minutes"].initial = self.instance.main_oeuvre.minutes

        # Nouveau diagnostic : taux horaire repris du dernier diagnostic de la société
        if not self.instance.pk and societe is not None and not self.initial.get("taux_horaire"):
            dernier = (
                Diagnostic.objects.filter(societe=societe, taux_horaire__gt=0)
                .order_by("-created_at").values_list("taux_horaire", flat=True).first()
            )
            if dernier:
                self.initial["taux_horaire"] = dernier

        # Exemplaires triés par marque, puis modèle, puis immatriculation
        vehicules = (
            VoitureExemplaire.objects
            .select_related("voiture_marque", "voiture_modele")
            .order_by(
                "voiture_marque__nom_marque",
                "voiture_modele__nom_modele",
                "voiture_modele__nom_variante",
                "immatriculation",
            )
        )
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)

        self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["voiture_exemplaire"].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe

        # Main-d'œuvre : création ou mise à jour (temps, véhicule, taux)
        total_minutes = (self.cleaned_data.get("temps_heures") or 0) * 60 + (self.cleaned_data.get("temps_minutes") or 0)
        descriptif = f"{_('Diagnostic')} {instance.voiture_exemplaire or ''}".strip()[:255]
        if instance.main_oeuvre_id:
            MainDoeuvre.objects.filter(pk=instance.main_oeuvre_id).update(
                temps_minutes=total_minutes,
                taux_horaire=instance.taux_horaire,
                voiture_exemplaire=instance.voiture_exemplaire,
                descriptif=descriptif,
            )
        else:
            instance.main_oeuvre = MainDoeuvre.objects.create(
                societe=instance.societe,
                utilisateur=self.user,
                voiture_exemplaire=instance.voiture_exemplaire,
                kilometres_chassis=instance.kilometrage or getattr(instance.voiture_exemplaire, "kilometres_chassis", 0) or 0,
                taux_horaire=instance.taux_horaire,
                temps_minutes=total_minutes,
                descriptif=descriptif,
            )
        # Kilométrage repris du véhicule s'il n'est pas saisi
        if instance.kilometrage is None and instance.voiture_exemplaire_id:
            instance.kilometrage = instance.voiture_exemplaire.kilometres_chassis
        if commit:
            instance.save()
        return instance


class DiagnosticCodeForm(forms.ModelForm):
    class Meta:
        model = DiagnosticCode
        fields = ("code_defaut", "piece_defaut", "piece_defaut_autre")
        widgets = {
            "code_defaut": forms.TextInput(attrs={
                "style": "text-transform:uppercase", "maxlength": 20, "placeholder": "P0301",
            }),
            "piece_defaut_autre": forms.TextInput(attrs={"placeholder": _("Préciser la pièce")}),
        }

    def clean_code_defaut(self):
        return (self.cleaned_data.get("code_defaut") or "").strip().upper()


class BaseDiagnosticCodeFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        vus = set()
        for form in self.forms:
            if not getattr(form, "cleaned_data", None) or form.cleaned_data.get("DELETE"):
                continue
            cle = (form.cleaned_data.get("code_defaut"), form.cleaned_data.get("piece_defaut"),
                   (form.cleaned_data.get("piece_defaut_autre") or "").strip().lower())
            if cle in vus:
                raise forms.ValidationError(_("Le même code défaut est encodé deux fois avec la même pièce."))
            vus.add(cle)


DiagnosticCodeFormSet = inlineformset_factory(
    Diagnostic,
    DiagnosticCode,
    form=DiagnosticCodeForm,
    formset=BaseDiagnosticCodeFormSet,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
