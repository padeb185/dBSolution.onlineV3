from decimal import Decimal
from functools import lru_cache

from django import forms
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from maindoeuvre.models import MainDoeuvre
from maintenance.choices import RouesSerrageEtat

from .models import Vitrage


# Icône dédiée à chaque section (à déposer dans theme/static/icons/).
# Tant qu'un fichier n'existe pas, ICONE_PAR_DEFAUT est affichée.
ICONE_PAR_DEFAUT = "vitres.png"

PIECES_ICONES = {
    "pare_brise": "pare-brise-casse.png",
    "impact_pare_brise": "pare-brise-casse.png",
    "joint_pare_brise": "vitre.png",
    "capteur_pluie": "vitre.png",
    "camera_adas": "vitre.png",
    "lunette_arriere": "lunette.png",
    "degivrage_lunette": "lunette.png",
    "vitre_porte": "vitre.png",
    "leve_vitre": "vitre.png",
    "moteur_leve_vitre": "vitre.png",
    "joint_vitre": "vitre.png",
    "vitre_custode": "vitre.png",
    "toit_ouvrant": "vitres.png",
    "film_teinte": "vitres.png",
    "retroviseur_complet": "retro.png",
    "glace_retroviseur": "retro.png",
    "coque_retroviseur": "retro.png",
    "moteur_retroviseur": "retro.png",
    "clignotant_retroviseur": "retro.png",
    "degivrage_retroviseur": "retro.png",
    "retroviseur_interieur": "retro.png",
}


@lru_cache(maxsize=None)
def icone_piece(base):
    """Nom du fichier icône d'une pièce, ou l'icône par défaut si le fichier n'existe pas."""
    nom = PIECES_ICONES.get(base)
    if nom and finders.find(f"icons/{nom}"):
        return nom
    return ICONE_PAR_DEFAUT

SUFFIXES_PIECE = ("", "_cote", "_fabricant", "_quantite", "_prix")


class VitrageForm(forms.ModelForm):
    temps_heures = forms.IntegerField(required=False, min_value=0)
    temps_minutes = forms.IntegerField(required=False, min_value=0, max_value=59)

    kilometrage_variation = forms.IntegerField(
        required=False,
        label=_("Variation du kilométrage"),
        widget=forms.NumberInput(attrs={"readonly": "readonly", "class": "input"}),
    )

    class Meta:
        model = Vitrage
        exclude = [
            "voiture_exemplaire",
            "maintenance",
            "kilometres_boite",
            "kilometres_moteur",
            "kilometres_embrayage",
            "kilometres_boite_rollback",
            "kilometres_moteur_rollback",
            "kilometres_embrayage_rollback",
        ]
        widgets = {
            "kilometres_chassis": forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "class": "bg-gray-100 cursor-not-allowed",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.exemplaire = kwargs.pop("exemplaire", None)
        super().__init__(*args, **kwargs)

        # Le véhicule doit être connu pour la validation du modèle (Vitrage.clean)
        if self.exemplaire is not None:
            self.instance.voiture_exemplaire = self.exemplaire

        # Le kilométrage "avant" est affiché mais jamais modifiable
        if "kilometres_chassis" in self.fields:
            self.fields["kilometres_chassis"].disabled = True

        # =========================
        # VARIATION KILOMÉTRAGE
        # =========================
        variation = 0
        if (
            self.instance.pk
            and self.instance.kilometrage_vitrage is not None
        ):
            variation = (
                self.instance.kilometrage_vitrage
                - (self.instance.kilometres_chassis or 0)
            )
        self.fields["kilometrage_variation"].initial = variation

        # =========================
        # MAIN D'ŒUVRE
        # =========================
        if "main_oeuvre" in self.fields:
            self.fields["main_oeuvre"].queryset = MainDoeuvre.objects.select_related(
                "utilisateur"
            ).filter(utilisateur__is_active=True)
            self.fields["main_oeuvre"].widget.attrs.update({"class": "input"})

        if self.instance.main_oeuvre_id:
            mo = self.instance.main_oeuvre
            self.fields["temps_heures"].initial = mo.heures
            self.fields["temps_minutes"].initial = mo.minutes
            if "taux_horaire" in self.fields:
                self.fields["taux_horaire"].initial = mo.taux_horaire

    # ======================================================
    # SECTIONS PIÈCES (pour les templates)
    # ======================================================
    @property
    def sections_pieces(self):
        """[{base, label, icone, champs: [BoundField, ...]}, ...] dans l'ordre de PIECES_DEF."""
        sections = []
        for label, base in Vitrage.PIECES_DEF:
            champs = [
                self[f"{base}{suffixe}"]
                for suffixe in SUFFIXES_PIECE
                if f"{base}{suffixe}" in self.fields
            ]
            if champs:
                sections.append({
                    "base": base,
                    "label": label,
                    "icone": icone_piece(base),
                    "champs": champs,
                })
        return sections

    # ======================================================
    # VALIDATIONS
    # ======================================================
    def clean_kilometrage_vitrage(self):
        km = self.cleaned_data.get("kilometrage_vitrage")

        if km is None or not self.exemplaire:
            return km

        # Création : comparaison au véhicule.
        # Modification : comparaison au kilométrage figé avant ce contrôle.
        if self.instance.pk:
            minimum = self.instance.kilometres_chassis or 0
        else:
            minimum = self.exemplaire.kilometres_chassis or 0

        if km < minimum:
            raise ValidationError(
                _("Le kilométrage ne peut pas être inférieur à %(km)s km.")
                % {"km": minimum}
            )
        return km

    def clean_serrage_roues(self):
        serrage_roues = self.cleaned_data.get("serrage_roues")

        if serrage_roues != RouesSerrageEtat.FAIT:
            raise ValidationError(
                _("Vous devez confirmer que le serrage des roues est FAIT avant de valider.")
            )
        return serrage_roues

    # ======================================================
    # SAUVEGARDE
    # ======================================================
    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.exemplaire is not None:
            instance.voiture_exemplaire = self.exemplaire

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
            main.save(update_fields=["temps_minutes", "taux_horaire"])
        else:
            main = MainDoeuvre.objects.create(
                utilisateur=self.user,
                temps_minutes=total_minutes,
                taux_horaire=taux_horaire or Decimal("50.00"),
            )
            instance.main_oeuvre = main

        if commit:
            instance.save()
            self.save_m2m()

        return instance
