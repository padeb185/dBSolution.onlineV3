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

# Rôles pouvant être choisis comme instructeur
ROLES_INSTRUCTEUR = ("instructeur", "instructeur externe")


# préfixe -> (modèle, champ de Location)
TYPES_CLIENT = {
    "client": (ClientParticulier, "client"),
    "societe": (SocieteCliente, "societe_cliente"),
    "pilotage": (ClientPilotage, "client_pilotage"),
}



def verifier_regles_location(form, societe, exclure_pk=None):
    """Règles de location : pas de double location du véhicule, respect des interdictions."""
    from .regles import conflits
    d = form.cleaned_data
    voiture, debut = d.get("voiture_exemplaire"), d.get("date_debut")
    if not voiture or not debut or form.has_error("date_fin") or form.has_error("heure_fin"):
        return
    for c in conflits(societe, voiture, debut, d.get("date_fin"), d.get("heure_debut"), d.get("heure_fin"),
                      exclure_pk=exclure_pk):
        form.add_error(None, c["message"])


class LocationForm(forms.ModelForm):
    locataire = forms.ChoiceField(
        label=_("Client"),
        required=False,
    )
    deuxieme_pilote = forms.ChoiceField(
        label=_("Deuxième pilote"),
        required=False,
        help_text=_("Facultatif : client ou client pilotage qui partage le véhicule."),
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
            "heure_debut",
            "heure_fin",
            "nombre_tours",
            "kilometrage",
            "prix",
            "acompte",
            "montant_acompte",
            "date_acompte",
            "payee",
            "remarques",
            "instructeur",
            "instructeur_heures",
            "instructeur_prix_heure",
            "prix_deuxieme_pilote",
            "prix_km_supplementaire",
            "carburant_inclus",
            "prix_carburant",
        )
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "nombre_tours": forms.NumberInput(attrs={"min": "1"}),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "prix": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "montant_acompte": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "date_acompte": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "remarques": forms.Textarea(attrs={"rows": 3}),
            "instructeur_heures": forms.NumberInput(attrs={"step": "0.25", "min": "0"}),
            "instructeur_prix_heure": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "prix_deuxieme_pilote": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "prix_km_supplementaire": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "prix_carburant": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
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

        # Deuxième pilote : clients particuliers et clients pilotage
        self.fields["deuxieme_pilote"].choices = [
            ("", "---------"),
            (_("Clients pilotage"), [(f"pilotage:{c.pk}", str(c)) for c in pilotes]),
            (_("Clients"), [(f"client:{c.pk}", str(c)) for c in clients]),
        ]
        if self.instance.deuxieme_client_pilotage_id:
            self.initial["deuxieme_pilote"] = f"pilotage:{self.instance.deuxieme_client_pilotage_id}"
        elif self.instance.deuxieme_client_id:
            self.initial["deuxieme_pilote"] = f"client:{self.instance.deuxieme_client_id}"

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

        # Paiement : « Payée » seulement si la facture de la location est émise
        self.facture_emise = None if self.instance._state.adding else self.instance.facture_emise
        if self.facture_emise is None:
            self.fields["payee"].disabled = True
            self.fields["payee"].help_text = _("Disponible une fois la facture de la location émise.")
        else:
            self.fields["payee"].help_text = _("Facture %(numero)s") % {"numero": self.facture_emise.numero}

        # Instructeur : utilisateurs actifs avec le rôle instructeur (interne ou externe)
        instructeurs = Utilisateur.objects.filter(is_active=True, role__in=ROLES_INSTRUCTEUR)
        if societe is not None:
            instructeurs = instructeurs.filter(societe=societe)
        if self.instance.instructeur_id:
            instructeurs = instructeurs | Utilisateur.objects.filter(pk=self.instance.instructeur_id)
        self.fields["instructeur"].queryset = instructeurs.distinct().order_by("nom", "prenom")
        self.fields["instructeur"].required = False
        self.fields["instructeur"].help_text = _("Facultatif : facturé en plus de la location, sans remise.")

        # Dernier prix à l'heure utilisé pour chaque instructeur (pré-remplissage)
        self.prix_instructeurs = {}
        derniers = (
            Location.objects.filter(instructeur__in=instructeurs, instructeur_prix_heure__isnull=False)
            .order_by("instructeur_id", "-date_debut", "-created_at")
            .values_list("instructeur_id", "instructeur_prix_heure")
        )
        for instructeur_id, prix_heure in derniers:
            self.prix_instructeurs.setdefault(str(instructeur_id), str(prix_heure))

        # Le prix de location est saisi TVAC
        self.fields["prix"].label = _("Prix TVAC (€)")
        self.fields["prix"].help_text = _("Prix de la location TVA comprise : la TVA est calculée au taux du pays de la société.")

        # Ordre d'affichage : le client juste après le véhicule
        self.order_fields(["voiture_exemplaire", "locataire"])

    def clean(self):
        cleaned = super().clean()
        societe = self.instance.societe if self.instance.societe_id else getattr(self.user, "societe", None)
        verifier_regles_location(self, societe, exclure_pk=self.instance.pk if not self.instance._state.adding else None)
        return cleaned

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

    def clean_deuxieme_pilote(self):
        valeur = self.cleaned_data.get("deuxieme_pilote")
        if not valeur:
            return None
        prefixe, _sep, pk = valeur.partition(":")
        if prefixe not in ("client", "pilotage"):
            raise forms.ValidationError(_("Client invalide."))
        modele, champ = TYPES_CLIENT[prefixe]
        try:
            return prefixe, modele.objects.get(pk=pk)
        except (modele.DoesNotExist, ValueError, DjangoValidationError):
            raise forms.ValidationError(_("Client introuvable."))

    def _post_clean(self):
        # Deuxième pilote
        deuxieme = self.cleaned_data.get("deuxieme_pilote") if hasattr(self, "cleaned_data") else None
        self.instance.deuxieme_client = None
        self.instance.deuxieme_client_pilotage = None
        if deuxieme:
            prefixe, obj = deuxieme
            if prefixe == "pilotage":
                self.instance.deuxieme_client_pilotage = obj
            else:
                self.instance.deuxieme_client = obj
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



class LocationVehiculeSupForm(forms.ModelForm):
    """
    Véhicule supplémentaire loué au même client (création multiple) :
    chaque véhicule a son propre lieu, ses dates, ses tours, son kilométrage et son prix.
    Le client, le vendeur et les remarques sont repris de la location principale.
    """

    class Meta:
        model = Location
        fields = (
            "voiture_exemplaire",
            "type_location",
            "circuit",
            "route",
            "date_debut",
            "date_fin",
            "heure_debut",
            "heure_fin",
            "nombre_tours",
            "kilometrage",
            "prix",
        )
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "nombre_tours": forms.NumberInput(attrs={"min": "1"}),
            "kilometrage": forms.NumberInput(attrs={"min": "0"}),
            "prix": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, vehicules=None, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.societe = societe
        if vehicules is not None:
            self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["prix"].label = _("Prix TVAC (€)")

    def clean(self):
        cleaned = super().clean()
        if self.societe is not None:
            verifier_regles_location(self, self.societe)
        return cleaned


# =====================================================================
# BOX EN PIT LANE (un ou plusieurs par location)
# =====================================================================
from .models import LocationBox  # noqa: E402

_C_BOX = "input block w-full border rounded px-3 py-2 bg-white"


class LocationBoxForm(forms.ModelForm):
    class Meta:
        model = LocationBox
        fields = ["numero", "pit_lane", "quantite", "prix_unitaire"]
        widgets = {
            "numero": forms.NumberInput(attrs={"class": _C_BOX, "min": "1", "max": "100", "placeholder": "1 – 100"}),
            "pit_lane": forms.Select(attrs={"class": _C_BOX}),
            "quantite": forms.NumberInput(attrs={"class": _C_BOX, "min": "1"}),
            "prix_unitaire": forms.NumberInput(attrs={"class": _C_BOX, "min": "0", "step": "0.01"}),
        }


class BaseLocationBoxFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        vus = set()
        for f in self.forms:
            if not hasattr(f, "cleaned_data") or not f.cleaned_data or f.cleaned_data.get("DELETE"):
                continue
            cle = (f.cleaned_data.get("pit_lane"), f.cleaned_data.get("numero"))
            if None in cle:
                continue
            if cle in vus:
                f.add_error("numero", _("Ce box est déjà dans la liste."))
            vus.add(cle)


LocationBoxFormSet = forms.inlineformset_factory(
    Location, LocationBox, form=LocationBoxForm, formset=BaseLocationBoxFormSet,
    extra=0, can_delete=True,
)


# =====================================================================
# INTERDICTIONS DE LOCATION
# =====================================================================
from .models import InterdictionLocation  # noqa: E402


class InterdictionLocationForm(forms.ModelForm):
    jours = forms.MultipleChoiceField(
        label=_("Jours de la semaine"), required=False, choices=InterdictionLocation.JOURS,
        widget=forms.CheckboxSelectMultiple, help_text=_("Aucun jour coché : tous les jours de la période."),
    )

    class Meta:
        model = InterdictionLocation
        fields = ["voiture_exemplaire", "date_debut", "date_fin", "heure_debut", "heure_fin", "motif", "description", "actif"]
        widgets = {
            "date_debut": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "date_fin": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "heure_debut": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "heure_fin": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
        }

    def __init__(self, *args, societe=None, **kwargs):
        super().__init__(*args, **kwargs)
        vehicules = VoitureExemplaire.objects.select_related("voiture_marque", "voiture_modele").order_by(
            "voiture_marque__nom_marque", "voiture_modele__nom_modele", "immatriculation")
        if societe is not None:
            vehicules = vehicules.filter(societe=societe)
        self.fields["voiture_exemplaire"].queryset = vehicules
        self.fields["voiture_exemplaire"].required = False
        self.fields["voiture_exemplaire"].empty_label = _("Tous les véhicules")
        self.initial.setdefault("jours", self.instance.jours_liste and [str(j) for j in self.instance.jours_liste])
        self.order_fields(["voiture_exemplaire", "date_debut", "date_fin", "heure_debut", "heure_fin", "jours",
                           "motif", "description", "actif"])

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.jours_semaine = ",".join(sorted(self.cleaned_data.get("jours") or []))
        if commit:
            obj.save()
        return obj
