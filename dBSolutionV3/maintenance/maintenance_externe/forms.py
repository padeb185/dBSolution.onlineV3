import unicodedata

from django import forms
from django.utils.translation import gettext_lazy as _

from garage_officiel.models import GarageOfficiel
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import CarrosserieExterne, MaintenanceExterne


class MaintenanceExterneForm(forms.ModelForm):
    class Meta:
        model = MaintenanceExterne
        fields = (
            "voiture_exemplaire", "garage", "type_maintenance", "date_facture", "numero_facture",
            "kilometrage", "pays", "taux_tva", "pieces_htva", "main_oeuvre_htva", "description",
        )
        widgets = {
            "date_facture": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "taux_tva": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "100"}),
            "pieces_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "main_oeuvre_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)

        vehicules = (
            VoitureExemplaire.objects.select_related("voiture_marque", "voiture_modele")
            .order_by("voiture_marque__nom_marque", "voiture_modele__nom_modele",
                      "voiture_modele__nom_variante", "immatriculation")
        )
        garages = GarageOfficiel.objects.select_related("adresse", "voiture_marque").order_by("nom")
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)
            garages = garages.filter(societe=societe)
        self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["garage"].queryset = garages
        self.fields["taux_tva"].required = False
        self.fields["kilometrage"].required = True
        self.fields["kilometrage"].help_text = _(
            "Kilométrage au compteur lors de l'intervention (ne peut pas être inférieur au dernier kilométrage connu)."
        )

        # Types de maintenance triés par ordre alphabétique (dans la langue affichée, sans tenir compte des accents)
        def cle_tri(choix):
            texte = unicodedata.normalize("NFKD", str(choix[1])).encode("ascii", "ignore").decode()
            return texte.casefold()

        choix = [c for c in self.fields["type_maintenance"].choices if c[0]]
        self.fields["type_maintenance"].choices = [("", "---------")] + sorted(choix, key=cle_tri)

        # Données pour le formulaire : pays du garage et marque du garage / du véhicule
        self.garages_infos = {
            str(g.pk): {"pays": g.code_pays, "marque": str(g.voiture_marque_id or "")} for g in garages
        }
        self.vehicules_infos = {
            str(v.pk): {
                "km": v.kilometres_chassis or 0,
                "marque": str(v.voiture_marque_id or ""),
                "km_moteur": v.kilometres_moteur or 0,
                "km_boite": v.kilometres_boite or 0,
                "km_embrayage": v.kilometres_embrayage or 0,
                "km_entretien": v.kilometres_dernier_entretien or 0,
                "nb_moteurs": v.nombre_remplacements_moteurs or 0,
                "nb_boites": v.nombre_remplacements_boites or 0,
            }
            for v in vehicules
        }
        # Effet de chaque type de maintenance sur les compteurs (affiché dans le formulaire)
        self.effets_types = {
            valeur: MaintenanceExterne.effet_type(valeur)
            for valeur, _libelle in self.fields["type_maintenance"].choices if valeur
        }

    CHAMPS_COMPTEURS = ("voiture_exemplaire", "type_maintenance", "kilometrage", "date_facture")

    def compteurs_modifies(self):
        return not self.instance.pk or any(c in self.changed_data for c in self.CHAMPS_COMPTEURS)

    def clean(self):
        cleaned = super().clean()
        vehicule = cleaned.get("voiture_exemplaire")
        km = cleaned.get("kilometrage")
        if vehicule is None or km is None or not self.compteurs_modifies():
            return cleaned

        # Kilométrage minimum : celui du véhicule avant cette intervention
        instance = self.instance
        if (
            instance.pk and instance.compteurs_appliques
            and instance.voiture_exemplaire_id == vehicule.pk
            and (vehicule.kilometres_chassis or 0) == (instance.kilometrage or 0)
        ):
            minimum = instance.km_chassis_avant or 0
        elif instance.pk and instance.voiture_exemplaire_id == vehicule.pk and not instance.compteurs_appliques:
            minimum = 0   # ancienne maintenance : pas de contrôle rétroactif
        else:
            minimum = vehicule.kilometres_chassis or 0

        if km < minimum:
            self.add_error(
                "kilometrage",
                _("Le kilométrage ne peut pas être inférieur au dernier kilométrage du véhicule (%(km)s km).")
                % {"km": minimum},
            )
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if commit:
            instance.save()
        return instance


# =====================================================================
# CARROSSERIE EXTERNE
# =====================================================================
class CarrosserieExterneForm(forms.ModelForm):
    TAILLE_MAX_PDF = 10 * 1024 * 1024  # 10 Mo

    class Meta:
        model = CarrosserieExterne
        fields = (
            "voiture_exemplaire", "carrossier", "statut", "kilometrage", "description",
            "devis_numero", "devis_date", "devis_htva", "devis_pdf",
            "facture_numero", "facture_date", "pays", "taux_tva",
            "pieces_htva", "peinture_htva", "main_oeuvre_htva", "facture_pdf",
            "prise_en_charge_assurance", "sinistre", "numero_sinistre", "franchise", "montant_assurance",
            "assurance_paie_carrossier", "date_paiement",
        )
        widgets = {
            "devis_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "facture_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_paiement": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "taux_tva": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "100"}),
            "devis_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "pieces_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "peinture_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "main_oeuvre_htva": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "franchise": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "montant_assurance": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "devis_pdf": forms.FileInput(attrs={"accept": "application/pdf"}),
            "facture_pdf": forms.FileInput(attrs={"accept": "application/pdf"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        from carrosserie.models import Carrosserie
        from assurance_police.models import Sinistre
        societe = getattr(self.user, "societe", None)

        vehicules = VoitureExemplaire.objects.select_related("voiture_marque", "voiture_modele").order_by(
            "voiture_marque__nom_marque", "voiture_modele__nom_modele", "immatriculation")
        carrossiers = Carrosserie.objects.order_by("nom_societe")
        sinistres = Sinistre.objects.select_related("police", "police__voiture_exemplaire").order_by("-date_sinistre")
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)
            carrossiers = carrossiers.filter(societe=societe)
            sinistres = sinistres.filter(police__societe=societe)
        self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["carrossier"].queryset = carrossiers
        self.fields["carrossier"].required = True
        self.fields["sinistre"].queryset = sinistres
        self.fields["sinistre"].required = False
        self.fields["taux_tva"].required = False
        self.fields["sinistre"].help_text = _("Sinistre déclaré dans les assurances du véhicule (facultatif).")
        # Sinistres par véhicule (filtrage dans le formulaire)
        self.sinistres_par_vehicule = {}
        for s in sinistres:
            vid = str(getattr(s.police, "voiture_exemplaire_id", "") or "")
            self.sinistres_par_vehicule.setdefault(vid, []).append(str(s.pk))

    def _clean_pdf(self, champ):
        from django.utils.translation import gettext as _t
        fichier = self.cleaned_data.get(champ)
        if not fichier or not hasattr(fichier, "read") or getattr(fichier, "_committed", False):
            return fichier  # aucun nouveau fichier envoyé
        if not (getattr(fichier, "name", "") or "").lower().endswith(".pdf"):
            raise forms.ValidationError(_t("Seuls les fichiers PDF sont acceptés."))
        if getattr(fichier, "size", 0) > self.TAILLE_MAX_PDF:
            raise forms.ValidationError(_t("Le fichier dépasse la taille maximale de 10 Mo."))
        debut = fichier.read(5)
        fichier.seek(0)
        if debut != b"%PDF-":
            raise forms.ValidationError(_t("Le fichier n'est pas un PDF valide."))
        return fichier

    def clean_devis_pdf(self):
        return self._clean_pdf("devis_pdf")

    def clean_facture_pdf(self):
        return self._clean_pdf("facture_pdf")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("facture_numero") and not cleaned.get("facture_date"):
            self.add_error("facture_date", _("Indiquez la date de la facture."))
        sinistre = cleaned.get("sinistre")
        vehicule = cleaned.get("voiture_exemplaire")
        if sinistre and vehicule and getattr(sinistre.police, "voiture_exemplaire_id", None) not in (None, vehicule.pk):
            self.add_error("sinistre", _("Ce sinistre concerne un autre véhicule."))
        if not cleaned.get("prise_en_charge_assurance"):
            cleaned["sinistre"] = None
            cleaned["montant_assurance"] = 0
            cleaned["franchise"] = 0
        return cleaned
