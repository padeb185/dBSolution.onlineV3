from django.db import models
from datetime import timedelta
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat
from .models import Fusibles



class FusiblesForm(forms.ModelForm):
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
        model = Fusibles
        exclude = {
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
            "kilometres_boite",
            "kilometres_moteur",
            "kilometres_embrayage",

        }
        widgets = {
            'maintenance': forms.HiddenInput(),
            'remarques': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': _("Ajoutez des remarques ici...")
            }),
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

            if (
                    self.instance
                    and self.instance.pk
                    and self.instance.kilometrage_fusibles is not None
                    and self.exemplaire
                    and self.exemplaire.kilometres_chassis is not None
            ):
                variation = (
                        self.instance.kilometrage_fusibles
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

            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = mo.taux_horaire


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

    def clean_kilometrage_fusibles(self):
        km = self.cleaned_data["kilometrage_fusibles"]

        if km < self.exemplaire.kilometres_chassis:
            raise ValidationError(
                _("Le kilométrage ne peut pas être inférieur au kilométrage actuel du véhicule.")
            )

        return km

    def clean(self):
        cleaned = super().clean()

        h = cleaned.get("temps_heures") or 0
        m = cleaned.get("temps_minutes") or 0

        if m >= 60:
            raise ValidationError("Les minutes ne peuvent pas dépasser 59.")

        km_fusibles = cleaned.get("kilometrage_fusibles")
        voiture = self.exemplaire or (self.instance.voiture_exemplaire if self.instance else None)

        if not voiture or km_fusibles in [None, ""]:
            return cleaned

        try:
            km_fusibles = Decimal(str(km_fusibles))
        except:
            raise ValidationError({
                "kilometrage_fusibles": _("Kilométrage invalide")
            })

        km_voiture = voiture.kilometres_chassis or Decimal("0")

        if km_fusibles < km_voiture:
            raise ValidationError({
                "kilometrage_fusibles": _(
                    "Le kilométrage doit être ≥ %(km)s"
                ) % {"km": km_voiture}
            })

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)

        km = self.cleaned_data.get("kilometrage_fusibles")
        voiture = self.exemplaire

        if km is not None and voiture:
            instance.kilometrage_fusibles = km
            instance.voiture_exemplaire = voiture

            # -------- MAIN D'ŒUVRE --------
            heures = self.cleaned_data.get("temps_heures") or 0
            minutes = self.cleaned_data.get("temps_minutes") or 0
            taux_horaire = self.cleaned_data.get("taux_horaire")

            total_minutes = heures * 60 + minutes

            main = instance.main_oeuvre

            if main:
                main.temps_minutes = total_minutes

                if taux_horaire is not None:
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


    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise forms.ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )

        return serrage_roues


# ---------------------------------------------------------------
# Détail des fusibles (formset) : boîte, repère, type, ampérage, organe, état
# ---------------------------------------------------------------
from .models import AMPERAGES_FUSIBLES, FusibleDetail  # noqa: E402

_C = "block w-full border rounded px-3 py-2 bg-white"


class FusibleDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import FabricantFusible
        qs = FabricantFusible.objects.filter(actif=True)
        if self.instance.pk and self.instance.fabricant_id:
            qs = FabricantFusible.objects.filter(models.Q(actif=True) | models.Q(pk=self.instance.fabricant_id))
        # Ordre alphabétique ; « Constructeur (OEM) » en tête et « Autre » en dernier
        from django.db.models.functions import Lower
        qs = qs.order_by("-oem", models.Case(models.When(nom="Autre", then=1), default=0), Lower("nom"))
        self.fields["fabricant"].queryset = qs
        self.fields["fabricant"].empty_label = _("— Choisir —")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("circuit") == "AUTRE" and not cleaned.get("organe"):
            self.add_error("organe", _("Précisez le circuit protégé."))
        return cleaned

    class Meta:
        model = FusibleDetail
        fields = ["emplacement", "repere", "circuit", "organe", "fabricant", "type_fusible", "amperage", "etat"]
        widgets = {
            "emplacement": forms.Select(attrs={"class": _C}),
            "repere": forms.TextInput(attrs={"class": _C + " font-mono uppercase", "placeholder": "F12"}),
            "type_fusible": forms.Select(attrs={"class": _C}),
            "amperage": forms.NumberInput(attrs={"class": _C, "step": "0.5", "min": "0", "list": "amperages-fusibles"}),
            "circuit": forms.Select(attrs={"class": _C}),
            "organe": forms.TextInput(attrs={"class": _C, "placeholder": _("Précision (si « Autre »)")}),
            "etat": forms.Select(attrs={"class": _C}),
            "fabricant": forms.Select(attrs={"class": _C}),
        }

    def has_changed(self):
        # Une ligne vide ajoutée mais non remplie n'est pas enregistrée
        return bool(self.data.get(self.add_prefix("organe")) or self.data.get(self.add_prefix("repere"))
                    or self.data.get(self.add_prefix("amperage")) or self.data.get(self.add_prefix("circuit"))) if self.is_bound and not self.instance.pk else super().has_changed()


FusibleDetailFormSet = forms.inlineformset_factory(
    Fusibles, FusibleDetail, form=FusibleDetailForm, extra=0, can_delete=True,
)
