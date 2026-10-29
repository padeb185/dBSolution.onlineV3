from django import forms
from django.utils.translation import gettext_lazy as _
from .models import VoitureExemplaire
from .utils_vin import VinDecoderService
from .immatriculation import exemples_par_pays, valider_immatriculation
import json

INVALID_VIN_CHARS = set("IOQ")


def valider_kilometrage_achat(form, cleaned_data):
    """
    Neuf : kilométrage de départ = 0.
    Occasion : kilométrage de départ obligatoire, ≤ kilométrage châssis.
    """
    etat = cleaned_data.get("etat_achat")
    km = cleaned_data.get("kilometrage_achat")
    km_chassis = cleaned_data.get("kilometres_chassis", form.instance.kilometres_chassis)
    if etat == "NEUF":
        cleaned_data["kilometrage_achat"] = 0
    elif etat == "OCCASION" and km in (None, ""):
        form.add_error("kilometrage_achat", _("Indiquez le kilométrage de départ du véhicule d'occasion."))
    elif etat == "OCCASION" and km is not None and km_chassis is not None and km > km_chassis:
        form.add_error(
            "kilometrage_achat",
            _("Le kilométrage de départ ne peut pas dépasser le kilométrage actuel (%(km)s km).") % {"km": km_chassis},
        )
    return cleaned_data


class VoitureExemplaireForm(forms.ModelForm):
    date_mise_en_circulation = forms.DateField(
        required=False,
        input_formats=["%Y-%m-%d", "%d/%m/%Y"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": "input",
            }
        ),
        label=_("Date de mise en circulation")
    )

    class Meta:
        model = VoitureExemplaire
        fields = (
            "voiture_marque",
            "voiture_modele",
            "immatriculation",
            "pays",
            "numero_vin",
            "type_utilisation",
            "cote_conduite",
            "kilometres_chassis",
            "etat_achat",
            "date_achat",
            "kilometrage_achat",
            "kilometres_moteur",
            "kilometres_boite",
            "kilometres_embrayage",
            "kilometres_dernier_entretien",
            "kilometres_rodage",
            "kilometres_entretien",
            "mois_production",
            "date_mise_en_circulation",
            
        )

        widgets = {
            "numero_vin": forms.TextInput(attrs={
                "maxlength": 17,
                "style": "text-transform:uppercase",
                "class": "input"
            }),
            "type_utilisation": forms.Select(attrs={"class": "input"}),
            "date_mise_en_circulation": forms.DateInput(attrs={
                "type": "date",
                "class": "input"
            }, format="%Y-%m-%d"),
            "est_apres_2010": forms.CheckboxInput(attrs={"class": "mt-2"}),
            "kilometrage_achat": forms.NumberInput(attrs={"min": "0"}),
            "date_achat": forms.DateInput(attrs={"type": "date", "class": "input"}, format="%Y-%m-%d"),
        }
        labels = {
            "etat_achat": _("Véhicule acheté"),
            "date_achat": _("Date d'achat"),
            "kilometrage_achat": _("Kilométrage de départ (km)"),
        }
        help_texts = {
            "kilometrage_achat": _("Neuf : 0 km. Occasion : kilométrage du véhicule au moment de l'achat."),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["date_mise_en_circulation"].widget.format = "%Y-%m-%d"
        self.fields["date_achat"].required = False

        # Aide à la saisie : formats de plaque acceptés par pays (lu par le JS du template)
        if "immatriculation" in self.fields:
            self.fields["immatriculation"].widget.attrs.update({
                "data-formats": json.dumps(exemples_par_pays(), ensure_ascii=False),
                "style": "text-transform:uppercase",
                "autocomplete": "off",
            })

    def _valider_immatriculation(self, cleaned_data):
        """Contrôle du format selon le pays — seulement si la plaque ou le pays change,
        pour ne pas bloquer les fiches existantes enregistrées avant la validation."""
        immat = cleaned_data.get("immatriculation")
        if not immat:
            return
        pays = cleaned_data.get("pays")
        inchange = (
            self.instance.pk
            and immat == self.instance.immatriculation
            and pays == self.instance.pays
        )
        if inchange:
            return
        try:
            cleaned_data["immatriculation"] = valider_immatriculation(immat, pays)
        except forms.ValidationError as e:
            self.add_error("immatriculation", e)

    def clean_numero_vin(self):
        vin = self.cleaned_data.get("numero_vin")

        if vin:
            vin = vin.upper().strip()

            if len(vin) != 17:
                raise forms.ValidationError(_("Le VIN doit contenir 17 caractères."))

            if any(c in INVALID_VIN_CHARS for c in vin):
                raise forms.ValidationError(_("Le VIN contient des caractères interdits (I, O, Q)."))

        return vin

    def clean(self):
        cleaned_data = super().clean()

        valider_kilometrage_achat(self, cleaned_data)
        self._valider_immatriculation(cleaned_data)

        vin = cleaned_data.get("numero_vin")
        voiture_marque = cleaned_data.get("voiture_marque")

        if not vin:
            return cleaned_data

        brand = (
            voiture_marque.nom_marque
            if voiture_marque
            else None
        )

        decoder = VinDecoderService(
            vin=vin,
            brand=brand,
        )

        data = decoder.decode()

        annee_production = data.get("production_year")

        if annee_production is not None:
            self.instance.annee_production = annee_production

            cleaned_data["est_apres_2010"] = (
                    annee_production >= 2010
            )
        else:
            self.instance.annee_production = None

        return cleaned_data




    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.user:
            instance.societe = getattr(
                self.user,
                "societe",
                None,
            )

        # -----------------------------------------------------
        # Valeurs calculées dans clean()
        # -----------------------------------------------------

        # annee_production a déjà été placée dans self.instance
        # dans clean(), donc on ne la relit pas depuis cleaned_data.

        instance.est_apres_2010 = self.cleaned_data.get(
            "est_apres_2010",
            instance.est_apres_2010,
        )

        if commit:
            instance.save()

        return instance

# =====================================================================
# DONNÉES FINANCIÈRES (onglet Direction)
# =====================================================================

FINANCE_FIELDS = (
    "etat_achat",
    "date_achat",
    "kilometrage_achat",
    "prix_achat",
    "assurance",
    "taxe_mise_en_circulation",
    "taxe_roulage",
    "nombre_proprietaires",
    "part_proprietaires_pourcent",
)

# Champs financiers facultatifs (non comptés dans « données incomplètes »)
FINANCE_FIELDS_OPTIONNELS = (
    "frais_achat",
    "valeur_revente",
    "kilometrage_creation",
    "consommation_estimee",
    "prix_carburant_estime",
)


class VoitureExemplaireFinanceForm(forms.ModelForm):
    """
    Complète les données financières d'un exemplaire existant.
    Les données d'identification (marque, VIN, km...) ne sont pas modifiables ici.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["valeur_revente"].required = False

    class Meta:
        model = VoitureExemplaire
        fields = FINANCE_FIELDS + FINANCE_FIELDS_OPTIONNELS
        labels = {
            "etat_achat": _("Véhicule acheté"),
            "kilometrage_achat": _("Kilométrage de départ (km)"),
            "prix_achat": _("Prix d'achat (€)"),
            "assurance": _("Assurance annuelle (€)"),
            "taxe_mise_en_circulation": _("Taxe de mise en circulation (€)"),
            "taxe_roulage": _("Taxe de roulage annuelle (€)"),
            "date_achat": _("Date d'achat"),
            "frais_achat": _("Autres frais d'achat (immatriculation, plaques, transport…) (€)"),
            "valeur_revente": _("Valeur de revente (€)"),
            "nombre_proprietaires": _("Nombre de propriétaires"),
            "part_proprietaires_pourcent": _("Part des propriétaires (%)"),
            "kilometrage_creation": _("Kilométrage à la création du véhicule (km)"),
            "consommation_estimee": _("Consommation moyenne (L/100 km)"),
            "prix_carburant_estime": _("Prix approximatif du carburant (€/L TVAC)"),
        }
        help_texts = {
            "kilometrage_creation": _("Premier kilométrage introduit pour le véhicule : fin de la période sans pleins encodés (depuis l'achat). Vide : premier kilométrage connu (pleins, maintenances)."),
            "consommation_estimee": _("Pour estimer le carburant non encodé. Vide : moyenne calculée sur les pleins encodés."),
            "prix_carburant_estime": _("Pour estimer le carburant non encodé. Vide : prix moyen des pleins encodés, sinon 1,850 €/L."),
            "kilometrage_achat": _("Neuf : 0 km. Occasion : kilométrage du véhicule au moment de l'achat."),
            "valeur_revente": _("Valeur estimée ou prix de revente réel, déduit du coût total. 0 par défaut."),
        }
        widgets = {
            "kilometrage_achat": forms.NumberInput(attrs={"min": "0"}),
            "prix_achat": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "assurance": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "taxe_mise_en_circulation": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "taxe_roulage": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "date_achat": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "frais_achat": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "valeur_revente": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "nombre_proprietaires": forms.NumberInput(attrs={"min": "1", "max": "10"}),
            "part_proprietaires_pourcent": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "100"}),
            "kilometrage_creation": forms.NumberInput(attrs={"min": "0"}),
            "consommation_estimee": forms.NumberInput(attrs={"step": "0.01", "min": "0", "placeholder": "8.24"}),
            "prix_carburant_estime": forms.NumberInput(attrs={"step": "0.001", "min": "0", "placeholder": "1.850"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for name in ("prix_achat", "assurance", "taxe_mise_en_circulation", "taxe_roulage", "frais_achat", "valeur_revente",
                     "consommation_estimee", "prix_carburant_estime"):
            value = cleaned_data.get(name)
            if value is not None and value < 0:
                self.add_error(name, _("Le montant ne peut pas être négatif."))

        # Kilométrage de départ : 0 pour un neuf, obligatoire pour une occasion
        valider_kilometrage_achat(self, cleaned_data)
        km_creation = cleaned_data.get("kilometrage_creation")
        if km_creation is not None and km_creation > (self.instance.kilometres_chassis or 0):
            self.add_error("kilometrage_creation", _("Le kilométrage à la création ne peut pas dépasser le kilométrage actuel (%(km)s km).")
                           % {"km": self.instance.kilometres_chassis or 0})
        # Champ vidé : revient à la valeur par défaut 0
        if cleaned_data.get("valeur_revente") is None:
            cleaned_data["valeur_revente"] = 0
        return cleaned_data



from .models import CoutAnnuelVehicule  # noqa: E402


class CoutAnnuelVehiculeForm(forms.ModelForm):
    class Meta:
        model = CoutAnnuelVehicule
        fields = ["annee", "type_cout", "pays", "libelle", "montant", "date"]
        widgets = {
            "annee": forms.NumberInput(attrs={"min": "1990", "max": "2100", "class": "border rounded px-2 py-1 w-24"}),
            "type_cout": forms.Select(attrs={"class": "border rounded px-2 py-1"}),
            "pays": forms.Select(attrs={"class": "border rounded px-2 py-1"}),
            "libelle": forms.TextInput(attrs={"class": "border rounded px-2 py-1 w-full"}),
            "montant": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "border rounded px-2 py-1 w-28"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "border rounded px-2 py-1"}, format="%Y-%m-%d"),
        }

    def clean_montant(self):
        montant = self.cleaned_data.get("montant")
        if montant is not None and montant < 0:
            raise forms.ValidationError(_("Le montant ne peut pas être négatif."))
        return montant
