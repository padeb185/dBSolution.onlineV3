from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Notification, ParametresNotifications, TYPES_PARAMETRABLES

CASE = forms.CheckboxInput(attrs={"class": "h-4 w-4"})


def libelle_type(code):
    return dict(Notification.Type.choices).get(code, code)


class ParametresNotificationsForm(forms.Form):
    """Page de la direction : expéditeur + une ligne de réglages par type de notification."""
    nom_expediteur = forms.CharField(label=_("Nom de l'expéditeur"), max_length=100, required=False,
                                     help_text=ParametresNotifications._meta.get_field("nom_expediteur").help_text)
    email_reponse = forms.EmailField(label=_("Adresse de réponse"), required=False,
                                     help_text=ParametresNotifications._meta.get_field("email_reponse").help_text)

    notifier_auteur = forms.BooleanField(label=_("Notifier aussi l'auteur de l'action"), required=False, widget=CASE,
                                         help_text=ParametresNotifications._meta.get_field("notifier_auteur").help_text)

    def __init__(self, *args, regles=None, **kwargs):
        super().__init__(*args, **kwargs)
        roles = get_user_model().ROLE_CHOICES
        self.lignes = []
        for t in TYPES_PARAMETRABLES:
            r = regles[t]
            self.fields[f"{t}_actif"] = forms.BooleanField(label=_("Actif"), required=False, initial=r.actif, widget=CASE)
            self.fields[f"{t}_app"] = forms.BooleanField(label=_("Application"), required=False, initial=r.canal_app, widget=CASE)
            self.fields[f"{t}_email"] = forms.BooleanField(label=_("E-mail"), required=False, initial=r.canal_email, widget=CASE)
            self.fields[f"{t}_roles"] = forms.MultipleChoiceField(
                label=_("Rôles destinataires"), choices=roles, required=False, initial=r.roles,
                widget=forms.CheckboxSelectMultiple)
            self.lignes.append({"code": t, "nom": libelle_type(t), "actif": self[f"{t}_actif"], "app": self[f"{t}_app"],
                                "email": self[f"{t}_email"], "roles": self[f"{t}_roles"]})

    def clean(self):
        d = super().clean()
        for t in TYPES_PARAMETRABLES:
            if d.get(f"{t}_actif"):
                if not d.get(f"{t}_roles"):
                    self.add_error(f"{t}_roles", _("Choisissez au moins un rôle, ou désactivez ce type."))
                if not (d.get(f"{t}_app") or d.get(f"{t}_email")):
                    self.add_error(f"{t}_app", _("Choisissez au moins un canal (application ou e-mail)."))
        return d


class PreferencesNotificationsForm(forms.Form):
    """Page de chaque utilisateur : couper l'application ou l'e-mail pour les types qu'il reçoit."""

    def __init__(self, *args, types=None, prefs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lignes = []
        for t, regle in types:
            p = prefs.get(t)
            ligne = {"code": t, "nom": libelle_type(t), "app": None, "email": None}
            if regle.canal_app:
                self.fields[f"{t}_app"] = forms.BooleanField(required=False, widget=CASE,
                                                             initial=p.recevoir_app if p else True)
                ligne["app"] = self[f"{t}_app"]
            if regle.canal_email:
                self.fields[f"{t}_email"] = forms.BooleanField(required=False, widget=CASE,
                                                               initial=p.recevoir_email if p else True)
                ligne["email"] = self[f"{t}_email"]
            self.lignes.append(ligne)
