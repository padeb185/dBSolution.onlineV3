from utilisateurs.models import Utilisateur
from django import forms

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import PaieUtilisateur, Utilisateur
from adresse.models import Adresse


from .mot_de_passe import ComplexiteValidator, verifier_confirmation, widget_confirmation, widget_nouveau  # noqa: E402


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Adresse e-mail"),
        widget=forms.EmailInput(
            attrs={
                "placeholder": _("Adresse e-mail"),
                "autocomplete": "email",
            }
        ),
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Mot de passe"),
                "autocomplete": "current-password",
            }
        ),
    )

    totp_code = forms.CharField(
        label=_("Code TOTP"),
        max_length=6,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Code à 6 chiffres"),
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
                "pattern": "[0-9]{6}",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]

        return email.strip().lower()

    def clean_totp_code(self):
        totp_code = (
            self.cleaned_data.get("totp_code") or ""
        ).strip()

        if totp_code and not totp_code.isdigit():
            raise forms.ValidationError(
                _("Le code TOTP doit contenir uniquement des chiffres.")
            )

        if totp_code and len(totp_code) != 6:
            raise forms.ValidationError(
                _("Le code TOTP doit contenir exactement 6 chiffres.")
            )

        return totp_code


class UtilisateurCreationForm(forms.ModelForm):
    societe = forms.CharField(
        label=_("Société"),
        required=False,
        disabled=True,
    )

    schema_name = forms.CharField(
        label=_("Schéma"),
        required=False,
        disabled=True,
    )

    password = forms.CharField(
        label=_("Mot de passe"),
        widget=widget_nouveau(_("Mot de passe")),
        strip=False,
        help_text=ComplexiteValidator().get_help_text(),
    )

    password_confirmation = forms.CharField(
        label=_("Confirmer le mot de passe"),
        widget=widget_confirmation(_("Confirmer le mot de passe")),
        strip=False,
    )

    rue = forms.CharField(
        label=_("Rue"),
    )

    numero = forms.CharField(
        label=_("Numéro"),
    )

    code_postal = forms.CharField(
        label=_("Code postal"),
    )

    ville = forms.CharField(
        label=_("Ville"),
    )

    pays = forms.CharField(
        label=_("Pays"),
    )

    field_order = [
        "societe", "schema_name", "nom", "prenom", "email", "email_entreprise", "telephone", "date_naissance",
        "numero_compte_bancaire", "role", "password", "password_confirmation",
    ]

    class Meta:
        model = Utilisateur

        fields = [
            "nom",
            "prenom",
            "email",
            "email_entreprise",
            "telephone",
            "date_naissance",
            "numero_compte_bancaire",
            "role",
            "password",
        ]

        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "placeholder": _("Nom de l’utilisateur"),
                }
            ),
            "prenom": forms.TextInput(
                attrs={
                    "placeholder": _("Prénom"),
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": _("Adresse e-mail utilisateur"),
                    "autocomplete": "email",
                }
            ),
            "email_entreprise": forms.EmailInput(
                attrs={
                    "placeholder": _("Adresse e-mail professionnelle"),
                }
            ),
            "telephone": forms.TextInput(
                attrs={
                    "placeholder": _("Téléphone"),
                }
            ),
            "date_naissance": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "numero_compte_bancaire": forms.TextInput(
                attrs={
                    "placeholder": "BE68 5390 0754 7034",
                    "autocomplete": "off",
                    "class": "font-mono uppercase",
                }
            ),
        }

    def clean_numero_compte_bancaire(self):
        # IBAN : nettoyage (sans espaces, majuscules), longueur du pays et clé mod 97
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(self.cleaned_data.get("numero_compte_bancaire"))

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe", None)

        super().__init__(*args, **kwargs)

        self.fields["email_entreprise"].label = _("E-mail entreprise (récupération du mot de passe)")
        self.fields["email_entreprise"].help_text = _(
            "Le lien « Mot de passe oublié » est envoyé à cette adresse ; à défaut, à l'e-mail de connexion."
        )

        self.societe_courante = societe

        if societe is not None:
            self.fields["societe"].initial = (
                getattr(societe, "nom", "")
            )

            self.fields["schema_name"].initial = (
                getattr(societe, "schema_name", "")
            )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        queryset = Utilisateur.objects.filter(
            email__iexact=email
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                _("Un utilisateur possède déjà cette adresse e-mail.")
            )

        return email

    def clean(self):
        cleaned = super().clean()
        utilisateur = Utilisateur(email=cleaned.get("email"), nom=cleaned.get("nom") or "",
                                  prenom=cleaned.get("prenom") or "")
        verifier_confirmation(self, "password", "password_confirmation", utilisateur)
        return cleaned

    def save(self, commit=True):
        utilisateur = super().save(commit=False)

        password = self.cleaned_data["password"]

        # Indispensable :
        # chiffre le mot de passe avec le système Django.
        utilisateur.set_password(password)

        if self.societe_courante is not None:
            utilisateur.societe = self.societe_courante

        if commit:
            utilisateur.save()
            self.save_m2m()

        return utilisateur


class PaieUtilisateurForm(forms.ModelForm):
    # Champs calculés automatiquement (affichés en lecture seule)
    CHAMPS_CALCULES = [
        "montant_heures_sup",
        "salaire_brut_majore",
        "taux_onss",
        "bonus_emploi",
        "montant_onss",
        "atn_voiture",
        "atn_total",
        "salaire_imposable",
        "taux_precompte_professionnel",
        "montant_precompte",
        "csss",
        "double_pecule_brut",
        "double_pecule_net",
        "treizieme_mois_brut",
        "treizieme_mois_net",
        "conges_jours_solde",
        "conges_simple_pecule",
        "conges_pecule_ouvrier_annuel",
        "salaire_net_mois",
        "cotisations_patronales",
        "reduction_structurelle",
        "cotisations_vacances",
        "cotisation_co2",
        "salaire_brut_mensuel_employeur",
        "salaire_total",
    ]

    # Champs recopiés depuis la dernière paie du travailleur (nouvelle paie)
    CHAMPS_REPRIS = [
        "statut_travailleur", "commission_paritaire", "categorie_cp", "classe_cp200",
        "annees_experience", "anciennete_un_an", "regime_travail",
        "situation_familiale", "parent_isole", "nombre_enfants_charge",
        "nombre_enfants_handicapes", "beneficiaire_handicape", "conjoint_handicape",
        "salaire_brut_heure", "salaire_brut_mensuel", "taux_charges_patronales",
        "reduction_groupe_cible", "atn_autres", "voiture_societe",
        "voiture_valeur_catalogue", "voiture_co2", "voiture_carburant",
        "voiture_date_immatriculation", "voiture_commandee_apres_07_2023",
        "voiture_contribution_personnelle", "conges_jours_droit",
    ]

    SECTIONS = [
        (_("Travailleur et commission paritaire"), [
            "utilisateur", "statut_travailleur", "commission_paritaire", "categorie_cp",
            "classe_cp200", "annees_experience", "anciennete_un_an", "regime_travail",
        ]),
        (_("Situation familiale (précompte professionnel)"), [
            "situation_familiale", "parent_isole", "nombre_enfants_charge",
            "nombre_enfants_handicapes", "beneficiaire_handicape", "conjoint_handicape",
        ]),
        (_("Prestations et salaire"), [
            "salaire_brut_heure", "nombre_jours_preste", "nombre_heures_preste",
            "salaire_brut_mensuel", "heures_supplementaires", "majoration_heures_sup",
            "taux_charges_patronales", "reduction_groupe_cible",
        ]),
        (_("Congés payés et pécule de vacances"), [
            "conges_jours_droit", "conges_jours_pris", "conges_payes", "double_pecule_ce_mois",
        ]),
        (_("Prime de fin d'année (13e mois)"), [
            "treizieme_mois_ce_mois", "treizieme_mois_mois_prestes", "treizieme_mois_reference",
        ]),
        (_("Avantages en nature"), [
            "atn_autres", "voiture_societe", "voiture_valeur_catalogue", "voiture_co2",
            "voiture_carburant", "voiture_date_immatriculation",
            "voiture_commandee_apres_07_2023", "voiture_contribution_personnelle",
        ]),
        (_("Calcul du salaire"), CHAMPS_CALCULES),
    ]

    class Meta:
        model = PaieUtilisateur
        exclude = [
            "date_paiement",
            "double_pecule_onss",
            "double_pecule_precompte",
            "treizieme_mois_onss",
            "treizieme_mois_precompte",
        ]
        widgets = {
            "voiture_date_immatriculation": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        societe = kwargs.pop("societe", None)

        super().__init__(*args, **kwargs)

        for nom in self.CHAMPS_CALCULES:
            if nom in self.fields:
                self.fields[nom].disabled = True
                self.fields[nom].required = False

        if "salaire_brut_mensuel" in self.fields:
            self.fields["salaire_brut_mensuel"].help_text = _(
                "Calculé automatiquement (heures × taux horaire) si des heures sont saisies."
            )
        if "conges_payes" in self.fields:
            self.fields["conges_payes"].label = _("Autres congés payés à charge de l'employeur")
            self.fields["conges_payes"].help_text = _(
                "Montant ajouté au coût total employeur (ex. pécule de vacances de sortie). "
                "Le simple pécule des jours pris est compris dans le salaire du mois."
            )
        if "taux_charges_patronales" in self.fields:
            self.fields["taux_charges_patronales"].help_text = _(
                "En %. Laisser vide pour le taux facial de 25 %."
            )

        # Travailleurs de la société du tenant uniquement (ce bloc était placé après le « return »
        # de sections() et n'était donc jamais exécuté : tous les utilisateurs de tous les tenants apparaissaient)
        if societe is not None:
            qs = (
                Utilisateur.objects
                .filter(
                    societe=societe,
                    is_active=True,
                )
                # Les comptes administrateurs de la plateforme (superutilisateurs, ex. « Admin Campus »)
                # ne sont pas des travailleurs du garage : pas de paie.
                .exclude(is_superuser=True)
            )
            # Modification : garder le travailleur de la paie même s'il a été désactivé depuis
            if self.instance.pk and self.instance.utilisateur_id:
                qs = qs | Utilisateur.objects.filter(pk=self.instance.utilisateur_id, societe=societe)
            self.fields["utilisateur"].queryset = qs.distinct().order_by("nom", "prenom")
        else:
            self.fields["utilisateur"].queryset = (
                Utilisateur.objects.none()
            )

    def sections(self):
        return [
            (titre, [self[nom] for nom in noms if nom in self.fields])
            for titre, noms in self.SECTIONS
        ]




class UtilisateurIbanForm(forms.ModelForm):
    """Modification de l'IBAN d'un utilisateur (contrôle pays + clé mod 97, mise en forme par 4)."""

    class Meta:
        model = Utilisateur
        fields = ["numero_compte_bancaire"]
        labels = {"numero_compte_bancaire": _("IBAN")}
        widgets = {
            "numero_compte_bancaire": forms.TextInput(attrs={
                "placeholder": "BE68 5390 0754 7034", "autocomplete": "off",
                "class": "input border rounded px-3 py-2 w-full font-mono uppercase",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from core.iban import formater_iban
        if self.instance and self.instance.numero_compte_bancaire and not self.is_bound:
            self.initial["numero_compte_bancaire"] = formater_iban(self.instance.numero_compte_bancaire)

    def clean_numero_compte_bancaire(self):
        from core.iban import nettoyer_iban_formulaire
        return nettoyer_iban_formulaire(self.cleaned_data.get("numero_compte_bancaire"))


class UtilisateurProfilForm(forms.ModelForm):
    """Édition du profil d'un utilisateur par la direction / le super-admin."""

    class Meta:
        model = Utilisateur
        fields = [
            "nom", "prenom", "role", "email", "email_entreprise", "telephone",
            "date_naissance", "numero_registre_national", "salaire_brut_heure", "is_active",
        ]
        labels = {
            "nom": _("Nom"),
            "prenom": _("Prénom"),
            "email": _("E-mail"),
            "email_entreprise": _("E-mail entreprise"),
            "telephone": _("Téléphone"),
            "date_naissance": _("Date de naissance"),
            "numero_registre_national": _("Numéro de registre national"),
            "is_active": _("Compte actif"),
        }
        widgets = {
            "date_naissance": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, editeur=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.editeur = editeur
        for nom in ("email", "email_entreprise"):
            self.fields[nom].required = False
        # Un utilisateur ne peut pas se retirer lui-même le rôle direction ni désactiver son compte
        if editeur is not None and self.instance.pk == editeur.pk and not editeur.is_superuser:
            self.fields["role"].disabled = True
            self.fields["is_active"].disabled = True

    def clean_email(self):
        return self.cleaned_data.get("email") or None

    def clean_email_entreprise(self):
        return self.cleaned_data.get("email_entreprise") or None


class AdresseUtilisateurForm(forms.ModelForm):
    class Meta:
        model = Adresse
        fields = ["rue", "numero", "boite", "code_postal", "ville", "pays", "code_pays"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.required = False

    def est_vide(self):
        return not any(self.cleaned_data.get(n) for n in ("rue", "numero", "code_postal", "ville"))

    def clean(self):
        cleaned = super().clean()
        if not self.est_vide():
            for n in ("rue", "numero", "code_postal", "ville"):
                if not cleaned.get(n):
                    self.add_error(n, _("Ce champ est obligatoire."))
        return cleaned

    def _post_clean(self):
        # Pas de validation du modèle (doublons) si l'adresse est laissée vide
        if self.is_bound and hasattr(self, "cleaned_data") and self.est_vide():
            return
        super()._post_clean()
