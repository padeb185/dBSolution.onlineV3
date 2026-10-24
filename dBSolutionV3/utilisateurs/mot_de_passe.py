"""
Mots de passe des utilisateurs : règles de complexité, formulaires (confirmation),
réinitialisation par e-mail.

Règles : au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.
Adresse de récupération : l'e-mail entreprise de l'utilisateur s'il est renseigné, sinon son e-mail de connexion.
"""
import re

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _, ngettext

LONGUEUR_MIN = 12


def erreurs_complexite(password, longueur_min=LONGUEUR_MIN):
    """Liste des règles non respectées (messages traduits)."""
    erreurs = []
    password = password or ""
    if len(password) < longueur_min:
        erreurs.append(ngettext(
            "Le mot de passe doit contenir au moins %(n)d caractère.",
            "Le mot de passe doit contenir au moins %(n)d caractères.", longueur_min) % {"n": longueur_min})
    if not re.search(r"[A-Z]", password):
        erreurs.append(_("Le mot de passe doit contenir au moins une majuscule."))
    if not re.search(r"[a-z]", password):
        erreurs.append(_("Le mot de passe doit contenir au moins une minuscule."))
    if not re.search(r"\d", password):
        erreurs.append(_("Le mot de passe doit contenir au moins un chiffre."))
    if not re.search(r"[^\w\s]|_", password):
        erreurs.append(_("Le mot de passe doit contenir au moins un caractère spécial (! ? @ # $ % & * …)."))
    if re.search(r"\s", password):
        erreurs.append(_("Le mot de passe ne peut pas contenir d'espace."))
    return erreurs


class ComplexiteValidator:
    """Validateur Django (AUTH_PASSWORD_VALIDATORS) : longueur, majuscule, minuscule, chiffre, caractère spécial."""

    def __init__(self, min_length=LONGUEUR_MIN):
        self.min_length = min_length

    def validate(self, password, user=None):
        erreurs = erreurs_complexite(password, self.min_length)
        if erreurs:
            raise ValidationError(erreurs, code="password_complexite")

    def get_help_text(self):
        return _("Au moins %(n)d caractères, dont une majuscule, une minuscule, un chiffre et un caractère spécial.") % {
            "n": self.min_length}


def adresse_recuperation(utilisateur):
    """E-mail de récupération : e-mail entreprise s'il est renseigné, sinon e-mail de connexion."""
    return (utilisateur.email_entreprise or utilisateur.email or "").strip()


# ---------------------------------------------------------------------------
# Widgets avec contrôle en direct (theme/static/js/mot_de_passe.js)
# ---------------------------------------------------------------------------
def widget_nouveau(placeholder=None):
    attrs = {"autocomplete": "new-password", "data-mdp": "nouveau"}
    if placeholder:
        attrs["placeholder"] = placeholder
    return forms.PasswordInput(attrs=attrs)


def widget_confirmation(placeholder=None):
    attrs = {"autocomplete": "new-password", "data-mdp": "confirmation"}
    if placeholder:
        attrs["placeholder"] = placeholder
    return forms.PasswordInput(attrs=attrs)


def verifier_confirmation(form, champ, champ_confirmation, user=None):
    """Compare les deux saisies puis applique les validateurs de mot de passe."""
    mdp = form.cleaned_data.get(champ)
    confirmation = form.cleaned_data.get(champ_confirmation)
    if mdp and confirmation is not None and mdp != confirmation:
        form.add_error(champ_confirmation, _("Les deux mots de passe ne sont pas identiques."))
        return
    if mdp:
        try:
            password_validation.validate_password(mdp, user)
        except ValidationError as e:
            form.add_error(champ, e)


# ---------------------------------------------------------------------------
# Formulaires
# ---------------------------------------------------------------------------
class ReinitialisationForm(PasswordResetForm):
    """« Mot de passe oublié » : e-mail de connexion ou e-mail entreprise ; lien envoyé à l'adresse de récupération."""

    email = forms.EmailField(
        label=_("Adresse e-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True,
                                       "placeholder": _("E-mail de connexion ou e-mail entreprise")}),
    )

    def get_users(self, email):
        from .models import Utilisateur
        utilisateurs = Utilisateur.objects.filter(
            Q(email__iexact=email) | Q(email_entreprise__iexact=email), is_active=True,
        )
        return (u for u in utilisateurs if u.has_usable_password() and adresse_recuperation(u))

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        utilisateur = context.get("user")
        destinataire = adresse_recuperation(utilisateur) if utilisateur else to_email
        super().send_mail(subject_template_name, email_template_name, context, from_email, destinataire,
                          html_email_template_name)


class NouveauMotDePasseForm(SetPasswordForm):
    """Nouveau mot de passe (lien reçu par e-mail) : saisie + confirmation, règles de complexité."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = widget_nouveau()
        self.fields["new_password2"].widget = widget_confirmation()
        self.fields["new_password1"].help_text = ComplexiteValidator().get_help_text()


class ChangementMotDePasseForm(PasswordChangeForm):
    """Changement par l'utilisateur connecté : ancien mot de passe, nouveau, confirmation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = widget_nouveau()
        self.fields["new_password2"].widget = widget_confirmation()
        self.fields["new_password1"].help_text = ComplexiteValidator().get_help_text()
