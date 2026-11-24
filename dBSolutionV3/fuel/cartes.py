"""
Champ « carte carburant / recharge » commun aux formulaires carburant, recharge électrique et AdBlue.
"""
from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import CarteCarburant

FAMILLE_TYPES = {
    "carburant": ("CARBURANT", "MIXTE"),
    "adblue": ("CARBURANT", "MIXTE"),
    "electricite": ("RECHARGE", "MIXTE"),
}


def configurer_champ_carte(form, famille):
    """Cartes actives compatibles (+ la carte déjà enregistrée), libellé, carte attribuée au véhicule par défaut."""
    if "carte" not in form.fields:
        return

    champ = form.fields["carte"]
    actuelle = getattr(form.instance, "carte_id", None)
    qs = CarteCarburant.objects.filter(type_carte__in=FAMILLE_TYPES[famille]).select_related("fournisseur")
    societe = getattr(form, "societe", None)
    if societe is not None:
        qs = qs.filter(societe=societe)
    qs = qs.filter(Q(actif=True) | Q(pk=actuelle)) if actuelle else qs.filter(actif=True)
    champ.queryset = qs.order_by("nom")
    champ.required = False
    champ.label = _("Carte carburant / recharge")
    champ.empty_label = _("Aucune (paiement direct)")
    champ.help_text = _("Carte à relevé hebdomadaire / mensuel : la dépense est payée au fournisseur à l'échéance du relevé.")
    champ.widget.attrs.setdefault("class", "border rounded px-3 py-2 w-full text-sm")

    # Nouvelle saisie : carte attribuée au véhicule (une seule) proposée par défaut
    if not form.is_bound and not actuelle and not form.initial.get("carte"):
        vehicule = form.initial.get("voiture_exemplaire")
        if vehicule:
            cartes = list(champ.queryset.filter(voiture_exemplaire=vehicule)[:2])
            if len(cartes) == 1:
                form.initial["carte"] = cartes[0].pk


def verifier_carte(form, famille):
    """Erreurs : carte incompatible avec l'énergie, ou attribuée à un autre véhicule."""
    carte = form.cleaned_data.get("carte")
    if not carte:
        return
    if not carte.accepte(famille):
        form.add_error("carte", _("Cette carte n'accepte pas ce type de dépense (%(type)s).")
                       % {"type": carte.get_type_carte_display()})
    vehicule = form.cleaned_data.get("voiture_exemplaire")
    if carte.voiture_exemplaire_id and vehicule and carte.voiture_exemplaire_id != getattr(vehicule, "pk", vehicule):
        form.add_error("carte", _("Cette carte est attribuée au véhicule %(immat)s.")
                       % {"immat": carte.voiture_exemplaire.immatriculation})


class CarteCarburantForm(forms.ModelForm):
    class Meta:
        model = CarteCarburant
        fields = ["nom", "fournisseur", "type_carte", "numero_fin", "voiture_exemplaire", "titulaire",
                  "date_expiration", "plafond_journalier", "plafond_mensuel",
                  "mode_paiement", "delai_paiement_jours", "compte_tresorerie", "actif", "remarques"]
        widgets = {
            "date_expiration": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "numero_fin": forms.TextInput(attrs={"inputmode": "numeric", "pattern": "[0-9]{4}", "maxlength": "4",
                                                 "placeholder": "1234", "autocomplete": "off"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.societe = societe
        from compta.models import CompteTresorerie
        from fournisseur.models import Fournisseur
        from utilisateurs.models import Utilisateur
        from voiture.voiture_exemplaire.models import VoitureExemplaire
        if societe is not None:
            self.fields["fournisseur"].queryset = Fournisseur.objects.filter(
                Q(societe=societe) | Q(societe__isnull=True)).order_by("nom")
            self.fields["voiture_exemplaire"].queryset = VoitureExemplaire.objects.filter(
                societe=societe).select_related("voiture_marque", "voiture_modele").order_by("immatriculation")
            self.fields["titulaire"].queryset = Utilisateur.objects.filter(
                societe=societe, is_active=True).order_by("nom", "prenom")
            self.fields["compte_tresorerie"].queryset = CompteTresorerie.objects.filter(
                societe=societe, actif=True).exclude(type="CAISSE").order_by("nom")
        self.fields["voiture_exemplaire"].empty_label = _("Tous les véhicules")
        self.fields["compte_tresorerie"].empty_label = _("Compte bancaire principal (550000)")
        for nom, champ in self.fields.items():
            if not isinstance(champ.widget, forms.CheckboxInput):
                champ.widget.attrs.setdefault("class", "border rounded px-3 py-2 w-full")

    def clean_numero_fin(self):
        n = (self.cleaned_data.get("numero_fin") or "").strip().replace(" ", "")
        if n and (not n.isdigit() or len(n) != 4):
            raise forms.ValidationError(_("Indiquez exactement les 4 derniers chiffres."))
        return n

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("mode_paiement") == "INSTANTANE":
            cleaned["delai_paiement_jours"] = 0
        return cleaned
