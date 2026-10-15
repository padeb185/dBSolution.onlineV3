from django import forms
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from utilisateurs.models import Utilisateur
from voiture.voiture_exemplaire.models import VoitureExemplaire
from .models import Location
from client_particulier.models import ClientParticulier
from client_pilotage.models import ClientPilotage
from societe_cliente.models import SocieteCliente

# Rôles pouvant être indiqués comme vendeur d'une location
ROLES_VENDEUR = ("vendeur", "direction", "chef_mecanicien")


# préfixe -> (modèle, champ de Location)
TYPES_CLIENT = {
    "client": (ClientParticulier, "client"),
    "societe": (SocieteCliente, "societe_cliente"),
    "pilotage": (ClientPilotage, "client_pilotage"),
}


class LocationForm(forms.ModelForm):
    locataire = forms.ChoiceField(
        label=_("Client"),
        required=False,
    )

    class Meta:
        model = Location
        fields = (
            "voiture_exemplaire",
            "type_location",
            "circuit",
            "route",
            "date_debut",
            "date_fin",
            "nombre_tours",
            "kilometrage",
            "prix",
            "remarques",
        )
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "nombre_tours": forms.NumberInput(attrs={"min": "1"}),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "prix": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "remarques": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        societe = getattr(self.user, "societe", None)

        # Véhicules triés par marque, puis modèle, puis immatriculation
        vehicules = (
            VoitureExemplaire.objects
            .select_related("voiture_marque", "voiture_modele")
            .order_by(
                "voiture_marque__nom_marque",
                "voiture_modele__nom_modele",
                "voiture_modele__nom_variante",
                "immatriculation",
            )
        )
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)

        self.fields["voiture_exemplaire"].queryset = vehicules

        # Liste des clients : particuliers, sociétés clientes, clients pilotage
        def _filtre(qs):
            return qs.filter(societe=societe) if societe is not None else qs

        clients = _filtre(ClientParticulier.objects.all()).order_by("nom", "prenom")
        societes = _filtre(SocieteCliente.objects.all()).order_by("nom_societe_cliente")
        pilotes = (
            _filtre(ClientPilotage.objects.select_related("client_particulier"))
            .order_by("client_particulier__nom", "client_particulier__prenom")
        )
        self.fields["locataire"].choices = [
            ("", "---------"),
            (_("Clients"), [(f"client:{c.pk}", str(c)) for c in clients]),
            (_("Sociétés clientes"), [(f"societe:{c.pk}", str(c)) for c in societes]),
            (_("Clients pilotage"), [(f"pilotage:{c.pk}", str(c)) for c in pilotes]),
        ]

        # Valeur initiale en modification
        inst = self.instance
        if inst.client_pilotage_id:
            self.initial["locataire"] = f"pilotage:{inst.client_pilotage_id}"
        elif inst.societe_cliente_id:
            self.initial["locataire"] = f"societe:{inst.societe_cliente_id}"
        elif inst.client_id:
            self.initial["locataire"] = f"client:{inst.client_id}"

        # Vendeur : choisi par la direction / le super admin, sinon l'utilisateur connecté
        if self.user is not None and (self.user.is_superuser or getattr(self.user, "role", None) == "direction"):
            vendeurs = Utilisateur.objects.filter(is_active=True, role__in=ROLES_VENDEUR)
            if societe is not None:
                vendeurs = vendeurs.filter(societe=societe)
            self.fields["vendeur"] = forms.ModelChoiceField(
                queryset=vendeurs.order_by("nom", "prenom"),
                required=False,
                label=_("Vendeur"),
                initial=self.instance.vendeur_id if self.instance.pk else self.user.pk,
                help_text=_("Utilisé pour les statistiques de ventes."),
            )
            if self.instance.pk:
                self.initial["vendeur"] = self.instance.vendeur_id

        # Le prix de location est saisi TVAC
        self.fields["prix"].label = _("Prix TVAC (€)")
        self.fields["prix"].help_text = _("Prix de la location TVA comprise : la TVA est calculée au taux du pays de la société.")

        # Ordre d'affichage : le client juste après le véhicule
        self.order_fields(["voiture_exemplaire", "locataire"])

    def clean_locataire(self):
        valeur = self.cleaned_data.get("locataire")
        if not valeur:
            return None
        prefixe, _sep, pk = valeur.partition(":")
        if prefixe not in TYPES_CLIENT:
            raise forms.ValidationError(_("Client invalide."))
        modele, champ = TYPES_CLIENT[prefixe]
        try:
            return champ, modele.objects.get(pk=pk)
        except (modele.DoesNotExist, ValueError, DjangoValidationError):
            raise forms.ValidationError(_("Client introuvable."))

    def _post_clean(self):
        # Affecte le bon champ client avant la validation du modèle
        choix = self.cleaned_data.get("locataire") if hasattr(self, "cleaned_data") else None
        self.instance.client = None
        self.instance.societe_cliente = None
        self.instance.client_pilotage = None
        if choix:
            champ, obj = choix
            setattr(self.instance, champ, obj)
        super()._post_clean()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user is not None and not instance.societe_id:
            instance.societe = self.user.societe
        if "vendeur" in self.fields:
            instance.vendeur = self.cleaned_data.get("vendeur")
        elif self.user is not None and not instance.vendeur_id:
            # Nouvelle location : le vendeur est l'utilisateur connecté
            instance.vendeur = self.user
        if commit:
            instance.save()
        return instance
