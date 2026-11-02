"""
Envoi des notifications internes (et, si activé, par e-mail).

    from notifications.services import notifier
    notifier(societe, roles=["direction"], type="vente", titre="…", message="…",
             url_name="facture:detail", url_kwargs={"pk": str(f.pk)})

Les notifications ne doivent jamais bloquer l'action qui les déclenche : toute erreur est journalisée.
"""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _

from .middleware import utilisateur_courant

log = logging.getLogger(__name__)

# Qui reçoit quoi
ROLES = {
    "maintenance": ["chef_atelier", "direction", "chef_mecanicien"],
    "vente": ["direction", "comptable"],
    "paiement": ["comptable"],
    "achat": ["comptable"],
}


def destinataires(societe, roles, exclure=None):
    from django.contrib.auth import get_user_model
    U = get_user_model()
    qs = U.objects.filter(societe=societe, role__in=roles, is_active=True)
    if exclure is not None and getattr(exclure, "pk", None):
        qs = qs.exclude(pk=exclure.pk)
    return list(qs)


def _envoyer_email(notif, lien):
    adresse = getattr(notif.destinataire, "email_entreprise", None) or getattr(notif.destinataire, "email", None)
    if not adresse:
        return
    base = getattr(settings, "SITE_URL", "").rstrip("/")
    corps = f"{notif.titre}\n\n{notif.message}\n\n" + (f"{_('Voir')} : {base}{lien}\n\n" if lien else "") + \
        f"{_('Envoyé par')} : {notif.nom_emetteur}\n"
    send_mail(f"[CarsCosts] {notif.titre}", corps, None, [adresse], fail_silently=True)
    type(notif).objects.filter(pk=notif.pk).update(email_envoye=True)


def notifier(societe, roles=None, type="autre", titre="", message="", url_name="", url_kwargs=None, url="",
             destinataires_explicites=None):
    """Crée une notification par destinataire (après validation de la transaction)."""
    if societe is None:
        return

    emetteur = utilisateur_courant()
    roles = roles or ROLES.get(type, ["direction"])

    def creer():
        try:
            from .models import Notification
            liste = destinataires_explicites or destinataires(societe, roles, exclure=emetteur)
            lien = ""
            if url_name:
                try:
                    lien = reverse(url_name, kwargs=url_kwargs or {})
                except NoReverseMatch:
                    lien = url
            for d in liste:
                n = Notification.objects.create(
                    destinataire=d, emetteur=emetteur if getattr(emetteur, "pk", None) else None, type=type,
                    titre=str(titre)[:200], message=str(message), url_name=url_name, url_kwargs=url_kwargs or {},
                    url=lien or url,
                )
                if getattr(settings, "NOTIFICATIONS_EMAIL", False):
                    _envoyer_email(n, lien or url)
        except Exception:  # une notification ne doit jamais casser l'action métier
            log.exception("Notification non créée : %s", titre)

    transaction.on_commit(creer)
