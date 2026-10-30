from decimal import Decimal

from django import forms
from maintenance.obligatoires import ChampsObligatoiresMaintenanceMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import FAMILLES_PIECES, PieceAccident, RapportAccident

_C = "border rounded px-2 py-1 bg-white"


class RapportAccidentForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)
    kilometrage_variation = forms.IntegerField(
        required=False, label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = RapportAccident
        exclude = {
            "maintenance", "voiture_exemplaire", "main_oeuvre",
            "kilometres_boite_rollback", "kilometres_moteur_rollback", "kilometres_embrayage_rollback",
            "kilometres_boite", "kilometres_moteur", "kilometres_embrayage",
        }
        widgets = {
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "circonstances": forms.Textarea(attrs={"rows": 3, "placeholder": _("Déroulement, conditions (pluie, nuit…), trajectoire…")}),
            "tiers_details": forms.Textarea(attrs={"rows": 2}),
            "date_accident": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "heure_accident": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "kilometres_chassis": forms.NumberInput(attrs={"readonly": "readonly", "class": "bg-gray-100 cursor-not-allowed"}),
            "vitesse_estimee": forms.NumberInput(attrs={"min": "0", "max": "400"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        variation = 0
        if self.instance.pk and self.instance.kilometrage_accident is not None:
            variation = self.instance.kilometrage_accident - (self.instance.kilometres_chassis or 0)
        self.fields["kilometrage_variation"].initial = variation

        if self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            self.fields["taux_horaire"].initial = mo.taux_horaire

        if self.user:
            for nom, valeur in (("tech_technicien", self.user), ("tech_societe", getattr(self.user, "societe", None))):
                if nom in self.fields:
                    self.fields[nom].initial = valeur
                    self.fields[nom].disabled = True

        # Sinistres déclarés pour ce véhicule
        from assurance_police.models import Sinistre
        sinistres = Sinistre.objects.select_related("police").order_by("-date_sinistre")
        if self.exemplaire is not None:
            sinistres = sinistres.filter(police__voiture_exemplaire=self.exemplaire)
        self.fields["sinistre"].queryset = sinistres
        self.fields["sinistre"].required = False
        self.fields["sinistre"].help_text = _("Sinistre déclaré dans les assurances du véhicule (facultatif).")

    def clean(self):
        cleaned = super().clean()
        km = cleaned.get("kilometrage_accident")
        voiture = self.exemplaire or self.instance.voiture_exemplaire
        if voiture and km is not None:
            km_ref = (self.instance.kilometres_chassis if self.instance.pk else voiture.kilometres_chassis) or 0
            if Decimal(str(km)) < Decimal(str(km_ref)):
                self.add_error("kilometrage_accident", _("Le kilométrage doit être ≥ %(km)s") % {"km": km_ref})
        if not cleaned.get("tiers_implique"):
            cleaned["tiers_details"] = ""
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
            instance.main_oeuvre = MainDoeuvre.objects.create(utilisateur=self.user, temps_minutes=total, taux_horaire=taux)


class PieceAccidentForm(forms.ModelForm):
    class Meta:
        model = PieceAccident
        fields = ("zone", "piece", "precision", "type_dommage", "gravite", "decision", "fabricant", "quantite", "prix")
        widgets = {
            "zone": forms.Select(attrs={"class": _C + " w-44"}),
            "piece": forms.Select(attrs={"class": _C + " w-56"}),
            "precision": forms.TextInput(attrs={"class": _C + " w-36", "placeholder": _("Précision")}),
            "type_dommage": forms.Select(attrs={"class": _C + " w-40"}),
            "gravite": forms.Select(attrs={"class": _C}),
            "decision": forms.Select(attrs={"class": _C + " w-40"}),
            "fabricant": forms.Select(attrs={"class": _C + " w-36"}),
            "quantite": forms.NumberInput(attrs={"class": _C + " w-16 text-right", "min": "0"}),
            "prix": forms.NumberInput(attrs={"class": _C + " w-24 text-right", "step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["piece"].choices = [("", _("— Choisir —"))] + [(str(f), liste) for f, liste in FAMILLES_PIECES]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("piece") == "AUTRE" and not cleaned.get("precision"):
            self.add_error("precision", _("Précisez la pièce."))
        return cleaned

    def has_changed(self):
        # une ligne ajoutée sans pièce choisie n'est pas enregistrée
        if self.is_bound and not self.instance.pk:
            return bool(self.data.get(self.add_prefix("piece")))
        return super().has_changed()


PieceAccidentFormSet = forms.inlineformset_factory(
    RapportAccident, PieceAccident, form=PieceAccidentForm, extra=0, can_delete=True,
)
