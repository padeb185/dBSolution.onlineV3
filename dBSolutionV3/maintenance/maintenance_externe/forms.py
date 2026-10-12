import unicodedata

from django import forms
from django.utils.translation import gettext_lazy as _

from garage_officiel.models import GarageOfficiel
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import MaintenanceExterne


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
            str(v.pk): {"km": v.kilometres_chassis or 0, "marque": str(v.voiture_marque_id or "")} for v in vehicules
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if commit:
            instance.save()
        return instance
