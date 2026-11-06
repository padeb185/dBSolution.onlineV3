from django import forms
from django.utils.translation import gettext_lazy as _

from .models import VenteVehicule

CHAMPS_PAIEMENT = ["mode_paiement", "date_paiement", "compte_encaissement"]


class VenteVehiculeForm(forms.ModelForm):
    class Meta:
        model = VenteVehicule
        fields = [
            "date_vente", "date_livraison", "kilometrage_vente",
            "type_acheteur", "client_particulier", "societe_cliente",
            "acheteur_nom", "acheteur_adresse", "acheteur_pays", "acheteur_tva", "acheteur_email", "acheteur_telephone",
            "regime_tva", "montant_saisi", "saisie_tvac", "taux_tva", "pourcentage_taxable", "prix_achat_marge",
            "frais_vente_htva", "mention_tva", "immobilisation",
            "mode_paiement", "date_paiement", "compte_encaissement",
            "doc_certificat_immatriculation", "doc_coc", "doc_carnet_entretien", "doc_car_pass",
            "doc_controle_technique", "nombre_cles", "etat_vehicule", "garantie_mois", "remarques",
        ]
        widgets = {
            "date_vente": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_livraison": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_paiement": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "acheteur_adresse": forms.Textarea(attrs={"rows": 3}),
            "etat_vehicule": forms.Textarea(attrs={"rows": 3}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "type_acheteur": forms.RadioSelect,
            "regime_tva": forms.RadioSelect,
        }

    UNITES = {"montant_saisi": "€", "taux_tva": "%", "pourcentage_taxable": "%", "prix_achat_marge": "€",
              "frais_vente_htva": "€", "kilometrage_vente": "km", "garantie_mois": _("mois")}

    def __init__(self, *args, societe=None, exemplaire=None, **kwargs):
        super().__init__(*args, **kwargs)
        from client_particulier.models import ClientParticulier
        from compta.models import CategorieImmobilisation, CompteTresorerie, Immobilisation
        from societe_cliente.models import SocieteCliente

        self.societe = societe
        self.exemplaire = exemplaire
        self.fields["client_particulier"].queryset = ClientParticulier.objects.filter(societe=societe).order_by("nom", "prenom")
        self.fields["societe_cliente"].queryset = SocieteCliente.objects.filter(societe=societe).order_by("nom_societe_cliente")
        self.fields["compte_encaissement"].queryset = CompteTresorerie.objects.filter(societe=societe, actif=True)
        self.fields["compte_encaissement"].empty_label = _("— Banque / caisse par défaut —")
        immos = Immobilisation.objects.filter(
            societe=societe,
            categorie__in=[CategorieImmobilisation.MATERIEL_ROULANT, CategorieImmobilisation.LOCATION_FINANCEMENT],
        )
        if self.instance.immobilisation_id:
            immos = immos.filter(date_cession__isnull=True) | immos.filter(pk=self.instance.immobilisation_id)
        else:
            immos = immos.filter(date_cession__isnull=True)
        self.fields["immobilisation"].queryset = immos.order_by("-date_acquisition")
        self.fields["immobilisation"].empty_label = _("— Aucune (véhicule non immobilisé) —")
        self.fields["client_particulier"].empty_label = _("— Encoder les coordonnées à la main —")
        self.fields["societe_cliente"].empty_label = _("— Encoder les coordonnées à la main —")

        for nom in ("montant_saisi", "prix_achat_marge", "frais_vente_htva"):
            self.fields[nom].widget.attrs.update({"step": "0.01", "min": "0", "inputmode": "decimal"})
        self.fields["taux_tva"].widget.attrs.update({"step": "0.01", "min": "0", "max": "100"})
        self.fields["pourcentage_taxable"].widget.attrs.update({"step": "1", "min": "0", "max": "100"})
        self.fields["acheteur_tva"].widget.attrs["placeholder"] = _("ex. BE0123456789")

        # Facture émise : seuls le paiement et les remarques restent modifiables
        if self.instance.pk and not self.instance.est_brouillon:
            for nom in list(self.fields):
                if nom not in CHAMPS_PAIEMENT + ["remarques"]:
                    self.fields[nom].disabled = True

    def unite(self, nom):
        return self.UNITES.get(nom, "")

    def clean(self):
        c = super().clean()
        if self.instance.pk and not self.instance.est_brouillon:
            return c
        R = VenteVehicule.RegimeTVA
        regime = c.get("regime_tva")
        if c.get("type_acheteur") == VenteVehicule.TypeAcheteur.PROFESSIONNEL:
            c["client_particulier"] = None
        else:
            c["societe_cliente"] = None
        if not (c.get("acheteur_nom") or c.get("client_particulier") or c.get("societe_cliente")):
            self.add_error("acheteur_nom", _("Indiquez l'acheteur (fiche client ou nom)."))
        if regime == R.MARGE and c.get("prix_achat_marge") is None:
            self.add_error("prix_achat_marge", _("Indiquez le prix d'achat TVAC du véhicule."))
        if regime == R.INTRACOM and c.get("type_acheteur") != VenteVehicule.TypeAcheteur.PROFESSIONNEL:
            self.add_error("type_acheteur", _("Une livraison intracommunautaire exonérée suppose un acheteur assujetti (professionnel)."))
        if regime != R.NORMAL:
            c["saisie_tvac"] = False
            c["pourcentage_taxable"] = c.get("pourcentage_taxable") or 100
        ex = self.exemplaire
        km = c.get("kilometrage_vente")
        if ex is not None and km is not None and ex.kilometrage_achat and km < ex.kilometrage_achat:
            self.add_error("kilometrage_vente", _("Le kilométrage est inférieur au kilométrage à l'achat (%(km)s km).") % {"km": ex.kilometrage_achat})
        dv = c.get("date_vente")
        if ex is not None and dv and ex.date_achat and dv < ex.date_achat:
            self.add_error("date_vente", _("La date de vente précède la date d'achat du véhicule."))
        if dv and c.get("date_livraison") and c["date_livraison"] < dv:
            self.add_error("date_livraison", _("La livraison ne peut pas précéder la vente."))
        return c


class AnnulationForm(forms.Form):
    date_annulation = forms.DateField(label=_("Date de la note de crédit"),
                                      widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"))
    motif = forms.CharField(label=_("Motif"), widget=forms.Textarea(attrs={"rows": 3}))
