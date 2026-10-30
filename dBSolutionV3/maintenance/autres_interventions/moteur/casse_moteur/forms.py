from decimal import Decimal

from django import forms
from maintenance.obligatoires import ChampsObligatoiresMaintenanceMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import CasseMoteur, EssaiCylindre, PieceCassee, PieceMoteur

_C = "border rounded px-2 py-1 bg-white"


class CasseMoteurForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = CasseMoteur
        exclude = {
            "moteur_lie",
            "maintenance",
            "voiture_exemplaire",
            "main_oeuvre",
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
            "kilometres_boite",
            "kilometres_moteur",
            "kilometres_embrayage",
        }
        widgets = {
            "remarques": forms.Textarea(attrs={"rows": 4, "placeholder": _("Ajoutez des remarques ici...")}),
            "circonstances": forms.Textarea(attrs={"rows": 3}),
            "analyse_huile": forms.Textarea(attrs={"rows": 3, "placeholder": _("Aspect, odeur, limaille, paillettes, eau, carburant…")}),
            "endoscopie": forms.Textarea(attrs={"rows": 3, "placeholder": _("Têtes de pistons, soupapes, parois des cylindres…")}),
            "date_casse": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "kilometres_chassis": forms.NumberInput(attrs={"readonly": "readonly", "class": "bg-gray-100 cursor-not-allowed"}),
            "nombre_cylindres": forms.NumberInput(attrs={"min": "1", "max": "16"}),
            "compression_nominale_bar": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "ecart_compression_max_pct": forms.NumberInput(attrs={"step": "0.1", "min": "0"}),
            "fuite_max_pct": forms.NumberInput(attrs={"step": "0.1", "min": "0", "max": "100"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        variation = 0
        if (self.instance and self.instance.pk and self.instance.kilometrage_casse is not None
                and self.exemplaire and self.exemplaire.kilometres_chassis is not None):
            variation = self.instance.kilometrage_casse - self.exemplaire.kilometres_chassis
        self.fields["kilometrage_variation"].initial = variation

        if self.instance and self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            self.fields["taux_horaire"].initial = mo.taux_horaire

        if self.user:
            if "tech_technicien" in self.fields:
                self.fields["tech_technicien"].initial = self.user
                self.fields["tech_technicien"].disabled = True
            if "tech_societe" in self.fields:
                self.fields["tech_societe"].initial = self.user.societe
                self.fields["tech_societe"].disabled = True

    def clean(self):
        cleaned = super().clean()
        if (cleaned.get("temps_minutes") or 0) >= 60:
            raise ValidationError(_("Les minutes ne peuvent pas dépasser 59."))

        km = cleaned.get("kilometrage_casse")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)
        if voiture and km not in (None, ""):
            km_ref = (self.instance.kilometres_chassis if self.instance and self.instance.pk
                      else voiture.kilometres_chassis) or 0
            if self.instance and self.instance.pk:
                km_ref = min(km_ref, self.instance.kilometrage_casse or km_ref)
            if Decimal(str(km)) < Decimal(str(km_ref)):
                self.add_error("kilometrage_casse", _("Le kilométrage doit être ≥ %(km)s") % {"km": km_ref})
        return cleaned

    def enregistrer_main_oeuvre(self, instance):
        heures = self.cleaned_data.get("temps_heures") or 0
        minutes = self.cleaned_data.get("temps_minutes") or 0
        taux = self.cleaned_data.get("taux_horaire") or 0
        total = heures * 60 + minutes
        if instance.main_oeuvre_id:
            mo = instance.main_oeuvre
            mo.temps_minutes = total
            mo.taux_horaire = taux
            mo.save(update_fields=["temps_minutes", "taux_horaire"])
        else:
            instance.main_oeuvre = MainDoeuvre.objects.create(
                utilisateur=self.user, temps_minutes=total, taux_horaire=taux,
            )


class PieceCasseeForm(forms.ModelForm):
    class Meta:
        model = PieceCassee
        fields = ("piece", "precision", "cylindre", "type_dommage", "gravite", "decision", "fabricant", "quantite", "prix")
        widgets = {
            "piece": forms.Select(attrs={"class": _C + " w-56"}),
            "precision": forms.TextInput(attrs={"class": _C + " w-40", "placeholder": _("Précision")}),
            "cylindre": forms.NumberInput(attrs={"class": _C + " w-16 text-center", "min": "1", "max": "16"}),
            "type_dommage": forms.Select(attrs={"class": _C + " w-44"}),
            "gravite": forms.Select(attrs={"class": _C}),
            "decision": forms.Select(attrs={"class": _C + " w-44"}),
            "fabricant": forms.Select(attrs={"class": _C + " w-40"}),
            "quantite": forms.NumberInput(attrs={"class": _C + " w-16 text-right", "min": "0"}),
            "prix": forms.NumberInput(attrs={"class": _C + " w-24 text-right", "step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["piece"].choices = [("", _("— Choisir —"))] + list(PieceMoteur.choices)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("piece") == PieceMoteur.AUTRE and not cleaned.get("precision"):
            self.add_error("precision", _("Précisez la pièce."))
        return cleaned

    def has_changed(self):
        # une ligne ajoutée sans pièce choisie n'est pas enregistrée
        if self.is_bound and not self.instance.pk:
            return bool(self.data.get(self.add_prefix("piece")))
        return super().has_changed()


class EssaiCylindreForm(forms.ModelForm):
    class Meta:
        model = EssaiCylindre
        fields = ("numero", "compression_bar", "fuite_pct", "fuite_admission", "fuite_echappement", "fuite_carter",
                  "fuite_refroidissement", "remarque")
        widgets = {
            "numero": forms.NumberInput(attrs={"class": _C + " w-14 text-center font-semibold", "min": "1"}),
            "compression_bar": forms.NumberInput(attrs={"class": _C + " w-20 text-right essai", "step": "0.1", "min": "0"}),
            "fuite_pct": forms.NumberInput(attrs={"class": _C + " w-20 text-right essai", "step": "0.1", "min": "0", "max": "100"}),
            "remarque": forms.TextInput(attrs={"class": _C + " w-48"}),
        }

    def has_changed(self):
        if self.is_bound and not self.instance.pk:
            champs = ("compression_bar", "fuite_pct", "remarque", "fuite_admission", "fuite_echappement",
                      "fuite_carter", "fuite_refroidissement")
            return any(self.data.get(self.add_prefix(n)) not in (None, "") for n in champs)
        return super().has_changed()


PieceCasseeFormSet = forms.inlineformset_factory(
    CasseMoteur, PieceCassee, form=PieceCasseeForm, extra=0, can_delete=True,
)
EssaiCylindreFormSet = forms.inlineformset_factory(
    CasseMoteur, EssaiCylindre, form=EssaiCylindreForm, extra=0, can_delete=True,
)
