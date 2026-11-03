"""
Envoi des notifications internes (et, si activé, par e-mail).

    from notifications.services import notifier
    notifier(societe, roles=["direction"], type="vente", titre="…", message="…",
             url_name="facture:detail", url_kwargs={"pk": str(f.pk)})

Les notifications ne doivent jamais bloquer l'action qui les déclenche : toute erreur est journalisée.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _

from .middleware import utilisateur_courant

log = logging.getLogger(__name__)

# Qui reçoit quoi par défaut (modifiable par la direction : page Paramètres des notifications)
from .models import ROLES_PAR_DEFAUT as ROLES  # noqa: E402


def destinataires(societe, roles, exclure=None):
    from django.contrib.auth import get_user_model
    U = get_user_model()
    qs = U.objects.filter(societe=societe, role__in=roles, is_active=True)
    if exclure is not None and getattr(exclure, "pk", None):
        qs = qs.exclude(pk=exclure.pk)
    return list(qs)


def adresse_email(utilisateur):
    return getattr(utilisateur, "email_entreprise", None) or getattr(utilisateur, "email", None) or ""


def expediteur(parametres=None):
    """« Nom de la société <no-reply@carscosts.com> » : l'adresse reste celle du domaine vérifié chez Brevo."""
    from email.utils import formataddr, parseaddr
    nom_defaut, adresse = parseaddr(settings.DEFAULT_FROM_EMAIL)
    nom = (getattr(parametres, "nom_expediteur", "") or "").strip()
    return formataddr((nom, adresse)) if nom else settings.DEFAULT_FROM_EMAIL


def _envoyer_email(destinataire, titre, message, lien, nom_emetteur, parametres, notif=None):
    adresse = adresse_email(destinataire)
    if not adresse:
        return
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    corps = f"{titre}\n\n{message}\n\n" + (f"{_('Voir')} : {base}{lien}\n\n" if lien else "") + \
        f"{_('Envoyé par')} : {nom_emetteur}\n"
    reponse = [parametres.email_reponse] if getattr(parametres, "email_reponse", "") else None
    EmailMessage(f"[CarsCosts] {titre}", corps, expediteur(parametres), [adresse], reply_to=reponse).send(
        fail_silently=True)
    if notif is not None:
        type(notif).objects.filter(pk=notif.pk).update(email_envoye=True)


def canaux(regle, preference):
    """(application, e-mail) pour un destinataire : la règle de la direction, puis son choix personnel."""
    app = regle.canal_app and (preference is None or preference.recevoir_app)
    email = regle.canal_email and (preference is None or preference.recevoir_email)
    return app, email


def notifier(societe, roles=None, type="autre", titre="", message="", url_name="", url_kwargs=None, url="",
             destinataires_explicites=None):
    """Crée une notification par destinataire (après validation de la transaction), selon les paramètres."""
    if societe is None:
        return

    emetteur = utilisateur_courant()

    def creer():
        try:
            from .models import Notification, ParametresNotifications, PreferenceNotification, RegleNotification
            regle = RegleNotification.pour(type)
            if not regle.actif:
                return
            liste = destinataires_explicites or destinataires(societe, roles or regle.roles, exclure=emetteur)
            if not liste:
                return
            parametres = ParametresNotifications.charger()
            prefs = {p.utilisateur_id: p for p in PreferenceNotification.objects.filter(
                type=type, utilisateur__in=[d.pk for d in liste])}
            lien = ""
            if url_name:
                try:
                    lien = reverse(url_name, kwargs=url_kwargs or {})
                except NoReverseMatch:
                    lien = url
            lien = lien or url
            emetteur_ok = emetteur if getattr(emetteur, "pk", None) else None
            for d in liste:
                app, email = canaux(regle, prefs.get(d.pk))
                n = None
                if app:
                    n = Notification.objects.create(
                        destinataire=d, emetteur=emetteur_ok, type=type, titre=str(titre)[:200],
                        message=str(message), url_name=url_name, url_kwargs=url_kwargs or {}, url=lien,
                    )
                if email:
                    nom = n.nom_emetteur if n else Notification(emetteur=emetteur_ok).nom_emetteur
                    _envoyer_email(d, str(titre), str(message), lien, nom, parametres, notif=n)
        except Exception:  # une notification ne doit jamais casser l'action métier
            log.exception("Notification non créée : %s", titre)

    transaction.on_commit(creer)
