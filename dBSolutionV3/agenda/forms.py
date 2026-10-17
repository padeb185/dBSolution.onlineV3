import unicodedata

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from maintenance.models import Maintenance
from voiture.voiture_exemplaire.models import VoitureExemplaire

from .models import AgendaTache

ROLES_TECHNICIENS = ["mecanicien", "apprenti", "magasinier", "chef_mecanicien", "direction"]


def cle_alphabetique(texte):
    """Clé de tri insensible à la casse et aux accents (« Éclairage » avec les E)."""
    texte = unicodedata.normalize("NFKD", str(texte))
    return "".join(c for c in texte if not unicodedata.combining(c)).casefold()


class AgendaTacheForm(forms.ModelForm):
    class Meta:
        model = AgendaTache
        fields = [
            "date",
            "type_maintenance",
            "voiture_exemplaire",
            "technicien",
            "tag",
            "statut",
            "prete_pour",
            "remarques",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        societe = getattr(user, "societe", None)

        # Véhicules de la société (avec ou sans client)
        self.fields["voiture_exemplaire"].queryset = (
            VoitureExemplaire.objects.filter(
                Q(client__societe=societe) | Q(client__isnull=True, societe=societe)
            )
            .select_related("voiture_marque", "voiture_modele")
            .order_by(
                "voiture_marque__nom_marque",
                "voiture_modele__nom_modele",
                "immatriculation",
            )
        )

        # Techniciens actifs de la société
        self.fields["technicien"].queryset = (
            get_user_model()
            .objects.filter(societe=societe, is_active=True, role__in=ROLES_TECHNICIENS)
            .order_by("nom", "prenom")
        )
        self.fields["technicien"].label_from_instance = lambda u: f"{u.prenom} {u.nom}"

        # Maintenances triées par ordre alphabétique (libellé traduit), choix vide en tête
        choix = list(self.fields["type_maintenance"].choices)
        vides = [c for c in choix if c[0] in ("", None)]
        autres = sorted((c for c in choix if c[0] not in ("", None)), key=lambda c: cle_alphabetique(c[1]))
        self.fields["type_maintenance"].choices = vides + autres

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")

    def clean(self):
        cleaned = super().clean()
        # « Prête pour » n'a de sens que pour un checkup piste
        if cleaned.get("type_maintenance") != Maintenance.TypeMaintenance.CHECKUP_TRACK:
            cleaned["prete_pour"] = ""
        return cleaned


class AgendaTacheRapideForm(forms.ModelForm):
    """Modification en ligne depuis la page du jour : tag, statut, prête pour."""

    class Meta:
        model = AgendaTache
        fields = ["tag", "statut", "prete_pour"]


# =====================================================================
# AGENDA DES LOCATIONS
# =====================================================================
from .models import AgendaLocation  # noqa: E402


class AgendaLocationSortieForm(forms.ModelForm):
    class Meta:
        model = AgendaLocation
        fields = ["kilometrage_avant", "niveau_essence_depart", "remarques"]
        widgets = {"remarques": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["kilometrage_avant"].required = True
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")


class AgendaLocationRetourForm(forms.ModelForm):
    class Meta:
        model = AgendaLocation
        fields = [
            "kilometrage_avant", "kilometrage_apres", "controle_carrosserie", "bruit_moteur",
            "niveau_essence_retour", "tag_retour", "remarques",
        ]
        widgets = {"remarques": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for nom in ("kilometrage_apres", "controle_carrosserie", "bruit_moteur", "niveau_essence_retour"):
            self.fields[nom].required = True
        # Au retour : jaune (à contrôler en atelier) ou rouge (problème)
        self.fields["tag_retour"].choices = [
            (Maintenance.Tag.JAUNE, Maintenance.Tag.JAUNE.label),
            (Maintenance.Tag.ROUGE, Maintenance.Tag.ROUGE.label),
        ]
        self.fields["tag_retour"].required = True
        if not self.initial.get("tag_retour"):
            self.initial["tag_retour"] = Maintenance.Tag.JAUNE
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")

    def clean(self):
        cleaned = super().clean()
        avant, apres = cleaned.get("kilometrage_avant"), cleaned.get("kilometrage_apres")
        if avant is not None and apres is not None and apres < avant:
            self.add_error("kilometrage_apres",
                           _("Le kilométrage après location ne peut pas être inférieur au kilométrage avant location."))
        # Un problème (carrosserie ou bruit moteur) impose le tag rouge
        if AgendaLocation.Controle.PROBLEME in (cleaned.get("controle_carrosserie"), cleaned.get("bruit_moteur")):
            cleaned["tag_retour"] = Maintenance.Tag.ROUGE
        return cleaned
