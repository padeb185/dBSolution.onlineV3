import re

from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_tenants.utils import get_public_schema_name

from societe.models import Domain, Societe
from .models import Utilisateur

SCHEMAS_RESERVES = {"public", "information_schema", "pg_catalog", "pg_toast", "tenant", "admin", "static", "media"}


from .mot_de_passe import ComplexiteValidator, verifier_confirmation, widget_confirmation, widget_nouveau  # noqa: E402


class TenantCreationForm(forms.Form):
    # ---------------- Société
    nom = forms.CharField(label=_("Nom de la société"), max_length=100)
    directeur = forms.CharField(label=_("Directeur"), max_length=100)
    numero_tva = forms.CharField(label=_("Numéro de TVA"), max_length=20)
    numero_tel = forms.CharField(label=_("Numéro de téléphone"), max_length=30, required=False)
    iban = forms.CharField(label=_("IBAN"), max_length=34, required=False)
    site = forms.URLField(label=_("Site internet"), required=False)

    # ---------------- Tenant
    schema_name = forms.CharField(
        label=_("Nom du schéma (identifiant du tenant)"), max_length=63, required=False,
        help_text=_("Lettres minuscules, chiffres et _ uniquement. Laissez vide pour le générer depuis le nom. "
                    "Il apparaît dans l'adresse : /tenant/<schéma>/"),
    )
    max_utilisateurs = forms.IntegerField(label=_("Nombre maximum d'utilisateurs"), min_value=1, initial=3)
    paid_until = forms.DateField(
        label=_("Abonnement payé jusqu'au"), required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    on_trial = forms.BooleanField(label=_("Période d'essai"), required=False, initial=True)

    # ---------------- Adresse
    rue = forms.CharField(label=_("Rue"), max_length=255)
    numero = forms.CharField(label=_("Numéro"), max_length=10)
    boite = forms.CharField(label=_("Boite"), max_length=10, required=False)
    code_postal = forms.CharField(label=_("Code postal"), max_length=10)
    ville = forms.CharField(label=_("Ville"), max_length=100)
    pays = forms.CharField(label=_("Pays"), max_length=100, initial="Belgique")
    code_pays = forms.CharField(label=_("Code pays"), max_length=5, initial="BE")

    # ---------------- Premier utilisateur (direction)
    admin_prenom = forms.CharField(label=_("Prénom"), max_length=100, required=False)
    admin_nom = forms.CharField(label=_("Nom"), max_length=100, required=False)
    admin_email = forms.EmailField(label=_("Email"), required=False)
    admin_password = forms.CharField(
        label=_("Mot de passe"), required=False, strip=False,
        widget=widget_nouveau(),
        help_text=ComplexiteValidator().get_help_text(),
    )
    admin_password_confirmation = forms.CharField(
        label=_("Confirmer le mot de passe"), required=False, strip=False,
        widget=widget_confirmation(),
    )

    SECTIONS = [
        (_("Société"), ["nom", "directeur", "numero_tva", "numero_tel", "iban", "site"]),
        (_("Tenant"), ["schema_name", "max_utilisateurs", "paid_until", "on_trial"]),
        (_("Adresse"), ["rue", "numero", "boite", "code_postal", "ville", "pays", "code_pays"]),
        (_("Premier utilisateur (direction) – facultatif"), ["admin_prenom", "admin_nom", "admin_email", "admin_password",
                                                                 "admin_password_confirmation"]),
    ]

    def sections(self):
        return [(titre, [self[n] for n in noms]) for titre, noms in self.SECTIONS]

    def clean_nom(self):
        nom = self.cleaned_data["nom"].strip()
        if Societe.objects.filter(nom__iexact=nom).exists():
            raise forms.ValidationError(_("Une société porte déjà ce nom."))
        return nom

    def clean_numero_tva(self):
        tva = self.cleaned_data["numero_tva"].replace(" ", "").replace(".", "").upper()
        if Societe.objects.filter(numero_tva__iexact=tva).exists():
            raise forms.ValidationError(_("Ce numéro de TVA est déjà utilisé."))
        return tva

    def clean_iban(self):
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(self.cleaned_data.get("iban")) or ""

    def clean_admin_email(self):
        email = (self.cleaned_data.get("admin_email") or "").strip().lower()
        if email and Utilisateur.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Un utilisateur utilise déjà cet email."))
        return email

    def clean(self):
        cleaned = super().clean()
        nom = cleaned.get("nom")

        # Schéma : saisi ou généré depuis le nom
        schema = (cleaned.get("schema_name") or "").strip().lower()
        if not schema and nom:
            schema = slugify(nom).replace("-", "_")
        if schema:
            if not re.fullmatch(r"[a-z][a-z0-9_]{1,62}", schema):
                self.add_error("schema_name", _(
                    "Le schéma doit commencer par une lettre et ne contenir que des minuscules, chiffres et _."))
            elif schema in SCHEMAS_RESERVES or schema.startswith("pg_") or schema == get_public_schema_name():
                self.add_error("schema_name", _("Ce nom de schéma est réservé."))
            elif Societe.objects.filter(schema_name=schema).exists() or Domain.objects.filter(domain=schema).exists():
                self.add_error("schema_name", _("Ce schéma existe déjà."))
        cleaned["schema_name"] = schema

        # Slug unique
        if nom:
            base = slugify(nom) or schema
            slug, i = base, 1
            while Societe.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            cleaned["slug"] = slug

        # Premier utilisateur : tout ou rien
        champs_admin = ["admin_prenom", "admin_nom", "admin_email", "admin_password"]
        remplis = [c for c in champs_admin if cleaned.get(c)]
        if remplis and len(remplis) < len(champs_admin):
            for c in champs_admin:
                if not cleaned.get(c):
                    self.add_error(c, _("Obligatoire pour créer le premier utilisateur."))
        if cleaned.get("admin_password"):
            verifier_confirmation(
                self, "admin_password", "admin_password_confirmation",
                Utilisateur(email=cleaned.get("admin_email"), nom=cleaned.get("admin_nom") or "",
                            prenom=cleaned.get("admin_prenom") or ""),
            )
        return cleaned


class TenantModificationForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = ["nom", "directeur", "numero_tva", "numero_tel", "iban", "site",
                  "max_utilisateurs", "paid_until", "on_trial"]
        widgets = {"paid_until": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}

    def sections(self):
        return [
            (_("Société"), [self[n] for n in ["nom", "directeur", "numero_tva", "numero_tel", "iban", "site"]]),
            (_("Tenant"), [self[n] for n in ["max_utilisateurs", "paid_until", "on_trial"]]),
        ]

    def clean_iban(self):
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(self.cleaned_data.get("iban")) or ""
