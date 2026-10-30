from decimal import Decimal

from django import forms
from maintenance.obligatoires import ChampsObligatoiresMaintenanceMixin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from .models import MesureCylindre, MesureTourillon, MetrologieMoteur

_COTE = {"step": "0.01", "min": "0", "inputmode": "decimal", "class": "input cote"}
_COTE_TABLE = {"step": "0.01", "min": "0", "inputmode": "decimal",
               "class": "cote w-24 border rounded px-2 py-1 text-right font-mono"}


class MetrologieMoteurForm(ChampsObligatoiresMaintenanceMixin, forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = MetrologieMoteur
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
            "kilometres_chassis": forms.NumberInput(attrs={"readonly": "readonly", "class": "bg-gray-100 cursor-not-allowed"}),
            "nombre_cylindres": forms.NumberInput(attrs={"min": "1", "max": "16", "class": "input"}),
            "cylindree_constructeur_cm3": forms.NumberInput(attrs={"step": "0.1", "min": "0", "class": "input"}),
            "cylindree_cm3": forms.NumberInput(attrs={"step": "0.1", "min": "0", "class": "input"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        # Cotes en mm au centième
        for name, field in self.fields.items():
            if isinstance(field, forms.DecimalField) and name not in ("taux_horaire", "cylindree_cm3", "cylindree_constructeur_cm3"):
                field.widget.attrs.update(_COTE)

        variation = 0
        if (self.instance and self.instance.pk and self.instance.kilometrage_metrologie is not None
                and self.exemplaire and self.exemplaire.kilometres_chassis is not None):
            variation = self.instance.kilometrage_metrologie - self.exemplaire.kilometres_chassis
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

        km = cleaned.get("kilometrage_metrologie")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)
        if voiture and km not in (None, ""):
            # en modification, la référence est le kilométrage avant l'intervention
            km_ref = (self.instance.kilometres_chassis if self.instance and self.instance.pk
                      else voiture.kilometres_chassis) or 0
            if self.instance and self.instance.pk:
                km_ref = min(km_ref, self.instance.kilometrage_metrologie or km_ref)
            if Decimal(str(km)) < Decimal(str(km_ref)):
                self.add_error("kilometrage_metrologie", _("Le kilométrage doit être ≥ %(km)s") % {"km": km_ref})

        # Tolérances : mini ≤ maxi
        for name in list(cleaned):
            if name.startswith("tol_") and name.endswith("_min"):
                maxi = name[:-4] + "_max"
                if cleaned.get(name) is not None and cleaned.get(maxi) is not None and cleaned[name] > cleaned[maxi]:
                    self.add_error(maxi, _("La valeur maxi doit être supérieure ou égale à la valeur mini."))
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


class _LigneMesureForm(forms.ModelForm):
    champs_mesure = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.champs_mesure:
            self.fields[name].widget.attrs.update(_COTE_TABLE)
        self.fields["numero"].widget.attrs.update({"class": "w-14 border rounded px-2 py-1 text-center font-semibold", "min": "1"})
        self.fields["remarque"].widget.attrs.update({"class": "w-48 border rounded px-2 py-1"})

    def has_changed(self):
        # Une ligne ajoutée sans aucune mesure n'est pas enregistrée
        if self.is_bound and not self.instance.pk:
            return any(self.data.get(self.add_prefix(n)) not in (None, "") for n in self.champs_mesure + ("remarque",))
        return super().has_changed()


class MesureCylindreForm(_LigneMesureForm):
    champs_mesure = (
        "chemise_haut_a", "chemise_haut_b", "chemise_milieu_a", "chemise_milieu_b", "chemise_bas_a", "chemise_bas_b",
        "piston_diametre",
        "segment_feu_jeu", "segment_etancheite_jeu", "segment_racleur_jeu",
        "maneton_1_a", "maneton_1_b", "maneton_2_a", "maneton_2_b",
        "pied_bielle_a", "pied_bielle_b", "axe_piston_diametre",
    )

    class Meta:
        model = MesureCylindre
        fields = ("numero",) + (
            "chemise_haut_a", "chemise_haut_b", "chemise_milieu_a", "chemise_milieu_b", "chemise_bas_a", "chemise_bas_b",
            "piston_diametre",
            "segment_feu_jeu", "segment_etancheite_jeu", "segment_racleur_jeu",
            "maneton_1_a", "maneton_1_b", "maneton_2_a", "maneton_2_b",
            "pied_bielle_a", "pied_bielle_b", "axe_piston_diametre",
            "remarque",
        )


class MesureTourillonForm(_LigneMesureForm):
    champs_mesure = ("section_1_a", "section_1_b", "section_2_a", "section_2_b")

    class Meta:
        model = MesureTourillon
        fields = ("numero", "section_1_a", "section_1_b", "section_2_a", "section_2_b", "remarque")


MesureCylindreFormSet = forms.inlineformset_factory(
    MetrologieMoteur, MesureCylindre, form=MesureCylindreForm, extra=0, can_delete=True,
)
MesureTourillonFormSet = forms.inlineformset_factory(
    MetrologieMoteur, MesureTourillon, form=MesureTourillonForm, extra=0, can_delete=True,
)
