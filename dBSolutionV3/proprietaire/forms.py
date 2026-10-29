from django.core.exceptions import ValidationError
from django import forms
from .models import Proprietaire
from .models import ProprietaireVoiture, TypeProprietaire
from decimal import Decimal
from django.utils.translation import gettext_lazy as _





def choix_titulaires(societe):
    """
    Titulaires possibles d'une part, regroupés : notre société, les propriétaires existants,
    les clients particuliers (repris comme propriétaires) et les sociétés partenaires.
    """
    from client_particulier.models import ClientParticulier
    from societe_cliente.models import SocieteCliente

    proprietaires = Proprietaire.objects.filter(societe=societe).order_by("nom", "prenom") if societe else []
    deja = {((p.nom or "").strip().lower(), (p.prenom or "").strip().lower()) for p in proprietaires}
    clients = [
        c for c in (ClientParticulier.objects.filter(societe=societe).order_by("nom", "prenom") if societe else [])
        if ((c.nom or "").strip().lower(), (c.prenom or "").strip().lower()) not in deja
    ]
    societes = SocieteCliente.objects.filter(societe=societe).order_by("nom_societe_cliente") if societe else []
    nom_tenant = getattr(societe, "nom", "") or _("Notre société")
    return [
        ("", "---------"),
        (_("Notre société"), [("tenant", f"{nom_tenant} – {_('notre société')}")]),
        (_("Propriétaires"), [(f"proprietaire:{p.pk}", f"{p.nom} {p.prenom}") for p in proprietaires]),
        (_("Clients particuliers (repris comme propriétaires)"),
         [(f"client:{c.pk}", f"{c.nom} {c.prenom}") for c in clients]),
        (_("Sociétés partenaires"),
         [(f"societe:{s.pk}", s.nom_societe_cliente or str(s.pk)) for s in societes]),
    ]


def proprietaire_depuis_client(client, societe):
    """
    Reprend un client particulier comme propriétaire : réutilise la fiche propriétaire existante
    (même email, ou même nom et prénom) ou en crée une, avec une copie de l'adresse
    (l'adresse d'un propriétaire est supprimée avec lui : elle n'est jamais partagée).
    """
    from django.db.models import Q
    from adresse.models import Adresse

    filtre = Q(nom__iexact=client.nom, prenom__iexact=client.prenom)
    if client.email:
        filtre |= Q(email__iexact=client.email)
    existant = Proprietaire.objects.filter(societe=societe).filter(filtre).first()
    if existant:
        return existant

    adresse = None
    source = client.adresse
    if source:
        adresse = Adresse.objects.create(
            societe=societe,
            rue=source.rue, numero=source.numero, boite=source.boite,
            code_postal=source.code_postal, ville=source.ville,
            pays=source.pays, code_pays=getattr(source, "code_pays", "") or "BE",
        )
    return Proprietaire.objects.create(
        societe=societe,
        nom=client.nom,
        prenom=client.prenom,
        adresse=adresse,
        email=client.email,
        numero_telephone=client.numero_telephone,
        numero_permis=client.numero_permis,
        date_naissance=client.date_naissance,
    )


class ProprietaireVoitureForm(forms.ModelForm):
    """Une part : titulaire (notre société, propriétaire, client ou société partenaire), pourcentage et marges."""

    titulaire = forms.ChoiceField(label=_("Propriétaire"))

    class Meta:
        model = ProprietaireVoiture
        fields = [
            "voiture_exemplaire",
            "part_proprietaire_pourcent",
            "marge_pieces",
            "marge_main_oeuvre",
            "commission_location",
            "remarques",
        ]
        widgets = {
            "part_proprietaire_pourcent": forms.NumberInput(attrs={
                "step": "0.01", "min": "0.01", "max": "100", "placeholder": "Ex: 50.00", "class": "input part-pourcent",
            }),
            "marge_pieces": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "input"}),
            "marge_main_oeuvre": forms.NumberInput(attrs={"step": "0.01", "min": "0", "class": "input"}),
            "commission_location": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "100", "class": "input"}),
            "remarques": forms.Textarea(attrs={"rows": 2, "class": "input"}),
        }

    def __init__(self, *args, societe=None, voiture=None, en_lot=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.societe = societe
        self.voiture = voiture
        if en_lot:
            self.instance.verifier_parts = False
        self.fields["titulaire"].choices = choix_titulaires(societe)
        self.fields["titulaire"].widget.attrs.update({"class": "input titulaire"})
        self.fields["marge_pieces"].required = False
        self.fields["marge_main_oeuvre"].required = False
        self.fields["commission_location"].required = False
        self.fields["remarques"].required = False

        from voiture.voiture_exemplaire.models import VoitureExemplaire
        if voiture is not None:
            # Page « propriétaires du véhicule » : le véhicule est fixé
            del self.fields["voiture_exemplaire"]
        else:
            self.fields["voiture_exemplaire"].queryset = (
                VoitureExemplaire.objects.filter(societe=societe) if societe else VoitureExemplaire.objects.none()
            ).select_related("voiture_marque", "voiture_modele")
            self.fields["voiture_exemplaire"].widget.attrs.setdefault("class", "input")

        inst = self.instance
        if inst and inst.pk:
            if inst.est_tenant:
                self.initial["titulaire"] = "tenant"
            elif inst.est_societe_cliente and inst.societe_cliente_id:
                self.initial["titulaire"] = f"societe:{inst.societe_cliente_id}"
            elif inst.proprietaire_id:
                self.initial["titulaire"] = f"proprietaire:{inst.proprietaire_id}"

    def clean_titulaire(self):
        from client_particulier.models import ClientParticulier
        from societe_cliente.models import SocieteCliente

        valeur = self.cleaned_data.get("titulaire") or ""
        if valeur == "tenant":
            return ("tenant", None)
        genre, _sep, pk = valeur.partition(":")
        modeles = {"proprietaire": Proprietaire, "client": ClientParticulier, "societe": SocieteCliente}
        modele = modeles.get(genre)
        if modele is None:
            raise forms.ValidationError(_("Propriétaire invalide."))
        try:
            obj = modele.objects.get(pk=pk, societe=self.societe)
        except (modele.DoesNotExist, ValueError, ValidationError):
            raise forms.ValidationError(_("Propriétaire introuvable."))
        return (genre, obj)

    def _post_clean(self):
        # Le titulaire choisi est affecté avant la validation du modèle (total des parts, doublons)
        choix = self.cleaned_data.get("titulaire")
        inst = self.instance
        if self.voiture is not None:
            inst.voiture_exemplaire = self.voiture
        if self.societe is not None:
            inst.societe = self.societe
        for champ in ("marge_pieces", "marge_main_oeuvre", "commission_location"):
            if self.cleaned_data.get(champ) is None and champ in self.cleaned_data:
                self.cleaned_data[champ] = Decimal("0.00")
        if not choix:
            # Titulaire absent ou invalide : l'erreur est déjà sur le champ « Propriétaire »
            return
        if choix:
            genre, obj = choix
            inst.proprietaire = None
            inst.societe_cliente = None
            inst.proprietaire_a_creer = False
            self._client_a_reprendre = None
            if genre == "tenant":
                inst.type_proprietaire = TypeProprietaire.TENANT
            elif genre == "societe":
                inst.type_proprietaire = TypeProprietaire.SOCIETE_CLIENTE
                inst.societe_cliente = obj
            elif genre == "proprietaire":
                inst.type_proprietaire = TypeProprietaire.PROPRIETAIRE
                inst.proprietaire = obj
            else:
                # Client particulier : fiche propriétaire existante réutilisée, sinon créée à l'enregistrement
                inst.type_proprietaire = TypeProprietaire.PROPRIETAIRE
                existant = self._proprietaire_existant(obj)
                if existant is not None:
                    inst.proprietaire = existant
                else:
                    self._client_a_reprendre = obj
                    inst.proprietaire_a_creer = True
        super()._post_clean()

    def _proprietaire_existant(self, client):
        from django.db.models import Q
        filtre = Q(nom__iexact=client.nom, prenom__iexact=client.prenom)
        if client.email:
            filtre |= Q(email__iexact=client.email)
        return Proprietaire.objects.filter(societe=self.societe).filter(filtre).first()

    def save(self, commit=True):
        inst = super().save(commit=False)
        client = getattr(self, "_client_a_reprendre", None)
        if client is not None and inst.proprietaire_id is None:
            inst.proprietaire = proprietaire_depuis_client(client, self.societe)
            inst.proprietaire_a_creer = False
        if commit:
            inst.save()
        return inst


class BasePartsVehiculeFormSet(forms.BaseModelFormSet):
    """Toutes les parts d'un véhicule : total ≤ 100 %, un titulaire une seule fois."""

    def __init__(self, *args, societe=None, voiture=None, **kwargs):
        self.societe = societe
        self.voiture = voiture
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs.update({"societe": self.societe, "voiture": self.voiture, "en_lot": True})
        return kwargs

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix("__prefix__"),
            empty_permitted=True,
            use_required_attribute=False,
            societe=self.societe,
            voiture=self.voiture,
            en_lot=True,
        )
        self.add_fields(form, None)
        return form

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        total = Decimal("0")
        vus = set()
        for form in self.forms:
            if not getattr(form, "cleaned_data", None) or form.cleaned_data.get("DELETE"):
                continue
            if not form.has_changed() and not form.instance.pk:
                continue
            part = form.cleaned_data.get("part_proprietaire_pourcent") or Decimal("0")
            total += part
            choix = form.cleaned_data.get("titulaire")
            if choix:
                genre, obj = choix
                cle = ("tenant",) if genre == "tenant" else (genre, str(obj.pk))
                if cle in vus:
                    raise forms.ValidationError(_("Un même propriétaire ne peut avoir qu'une seule part."))
                vus.add(cle)
        if total > Decimal("100"):
            raise forms.ValidationError(
                _("Le total des parts (%(total)s %%) dépasse 100 %%.") % {"total": total}
            )
        self.total = total


class ProprietaireForm(forms.ModelForm):
    prenom = forms.CharField(
        label=_("Prénom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    nom = forms.CharField(
        label=_("Nom"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    email = forms.EmailField(
        label = _("Email"),
        widget = forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )

    numero_telephone = forms.CharField(
        label=_("Numéro de téléphone"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_carte_id = forms.CharField(
        label=_("Numéro de carte d'identité"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_compte = forms.CharField(
        label=_("Numéro de compte"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    numero_carte_bancaire = forms.CharField(
        label=_("Numéro de carte bancaire"),
        widget=forms.TextInput(attrs={"class": "border rounded px-4 py-2 w-full"})
    )
    date_naissance = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "border rounded px-4 py-2 w-full",
            }, format="%Y-%m-%d"
        )
    )


    rue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    numero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    boite = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_postal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    ville = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    pays = forms.CharField(
        required=False,
        initial="Belgique",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )

    code_pays = forms.CharField(
        required=False,
        initial="BE",
        widget=forms.TextInput(attrs={
            "class": "border rounded px-4 py-2 w-full"
        })
    )
    class Meta:
        model = Proprietaire
        exclude = ["societe"]
        fields = [
            "prenom",
            "nom",
            "numero_telephone",
            "numero_permis",
            "numero_carte_id",
            "numero_compte",
            "numero_carte_bancaire",
            "email",
            "date_naissance",

            "rue",
            "numero",
            "boite",
            "code_postal",
            "ville",
            "pays",
            "code_pays",
            "remarques",
        ]

        widgets = {

            "numero_telephone": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_permis": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_carte_id": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "numero_compte": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "BE12 3456 7890 1234"
            }),

            "numero_carte_bancaire": forms.TextInput(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "placeholder": "5389 3456 7890 1234"
            }),

            "email": forms.EmailInput(attrs={
                "class": "border rounded px-4 py-2 w-full"
            }),

            "remarques": forms.Textarea(attrs={
                "class": "border rounded px-4 py-2 w-full",
                "rows": 3
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            self.fields["prenom"].initial = self.instance.prenom
            self.fields["nom"].initial = self.instance.nom
            self.fields["email"].initial = self.instance.email
            self.fields["numero_telephone"].initial = self.instance.numero_telephone
            self.fields["numero_carte_id"].initial = self.instance.numero_carte_id
            self.fields["numero_compte"].initial = self.instance.numero_compte
            self.fields["numero_carte_bancaire"].initial = self.instance.numero_carte_bancaire
            self.fields["date_naissance"].initial = self.instance.date_naissance


            if self.instance.adresse:

                adresse = self.instance.adresse

                self.fields["rue"].initial = adresse.rue
                self.fields["numero"].initial = adresse.numero
                self.fields["boite"].initial = adresse.boite
                self.fields["code_postal"].initial = adresse.code_postal
                self.fields["ville"].initial = adresse.ville
                self.fields["pays"].initial = adresse.pays
                self.fields["code_pays"].initial = adresse.code_pays


    def clean_nom(self):
        nom = self.cleaned_data.get("nom")
        if nom and len(nom) < 2:
            raise forms.ValidationError("Le nom doit contenir au moins 2 caractères.")
        return nom

    def clean_prenom(self):
        prenom = self.cleaned_data.get("prenom")
        if prenom and len(prenom) < 2:
            raise forms.ValidationError("Le prénom doit contenir au moins 2 caractères.")
        return prenom

    def clean_numero_compte(self):
        # IBAN : nettoyage (sans espaces, majuscules), longueur du pays et clé mod 97
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(self.cleaned_data.get("numero_compte"))