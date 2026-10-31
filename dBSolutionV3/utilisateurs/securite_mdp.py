"""
Alerte de sécurité après un changement / une réinitialisation du mot de passe :
- e-mail à l'adresse entreprise de l'utilisateur (et à son e-mail de connexion s'il est différent)
  avec la date, l'heure, l'adresse IP et le navigateur ;
- lien « Ce n'était pas moi » (signé, valable 7 jours) qui sécurise le compte :
  mot de passe bloqué (toutes les sessions sont déconnectées), nouveau lien de réinitialisation envoyé
  à l'adresse entreprise, direction de la société prévenue, action journalisée.
"""
import logging

from django.conf import settings
from django.core import signing
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)

SEL = "utilisateurs.mdp.pas_moi"
VALIDITE_SECONDES = 7 * 24 * 3600


def ip_client(request):
    transmis = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return (transmis.split(",")[0].strip() if transmis else request.META.get("REMOTE_ADDR", "")) or "?"


def navigateur(request):
    return (request.META.get("HTTP_USER_AGENT", "") or "?")[:200]


def adresses_alerte(utilisateur):
    """E-mail entreprise en priorité, plus l'e-mail de connexion s'il est différent."""
    adresses = []
    for a in (utilisateur.email_entreprise, utilisateur.email):
        a = (a or "").strip()
        if a and a.lower() not in [x.lower() for x in adresses]:
            adresses.append(a)
    return adresses


def jeton_pas_moi(utilisateur, evenement):
    return signing.dumps({"u": str(utilisateur.pk), "e": evenement}, salt=SEL, compress=True)


def lire_jeton(jeton):
    """{"u": id, "e": événement} ou None (jeton invalide ou expiré)."""
    try:
        return signing.loads(jeton, salt=SEL, max_age=VALIDITE_SECONDES)
    except signing.BadSignature:
        return None


def _envoyer(sujet, gabarit, contexte, destinataires):
    if not destinataires:
        return False
    texte = render_to_string(f"utilisateurs/mot_de_passe/{gabarit}.txt", contexte)
    html = render_to_string(f"utilisateurs/mot_de_passe/{gabarit}.html", contexte)
    message = EmailMultiAlternatives(sujet, texte, settings.DEFAULT_FROM_EMAIL, destinataires)
    message.attach_alternative(html, "text/html")
    try:
        message.send()
        return True
    except Exception:
        logger.exception("Envoi de l'e-mail de sécurité impossible (%s)", gabarit)
        return False


def alerter_changement(request, utilisateur, evenement):
    """evenement : "changement" (utilisateur connecté) ou "reinitialisation" (lien « mot de passe oublié »)."""
    from django.utils.translation import gettext as _
    lien = request.build_absolute_uri(reverse("password_pas_moi", args=[jeton_pas_moi(utilisateur, evenement)]))
    contexte = {
        "user": utilisateur,
        "evenement": evenement,
        "quand": timezone.localtime(),
        "ip": ip_client(request),
        "navigateur": navigateur(request),
        "lien_pas_moi": lien,
        "validite_jours": VALIDITE_SECONDES // 86400,
    }
    sujet = (_("CarsCosts – votre mot de passe a été modifié") if evenement == "changement"
             else _("CarsCosts – votre mot de passe a été réinitialisé"))
    return _envoyer(sujet, "email_alerte_changement", contexte, adresses_alerte(utilisateur))


def securiser_compte(request, utilisateur, evenement):
    """Action « Ce n'était pas moi ». Retourne un dict de ce qui a été fait."""
    from django.utils.translation import gettext as _
    from .models import UserLog, Utilisateur
    from .mot_de_passe import ReinitialisationForm, adresse_recuperation
    from .views_mot_de_passe import GABARITS_EMAIL

    fait = {"bloque": False, "lien": False, "direction": 0}

    # 1) Mot de passe bloqué : le mot de passe inconnu ne fonctionne plus et toutes les sessions
    #    ouvertes sont déconnectées (le hachage de session ne correspond plus).
    utilisateur.set_unusable_password()
    utilisateur.save(update_fields=["password"])
    fait["bloque"] = True

    # 2) Nouveau lien de réinitialisation vers l'adresse entreprise (le formulaire exige un mot de passe
    #    utilisable : mot de passe aléatoire temporaire, aussitôt remplacé par l'utilisateur).
    adresse = adresse_recuperation(utilisateur)
    if adresse and utilisateur.is_active:
        from django.utils.crypto import get_random_string
        utilisateur.set_password(get_random_string(48))
        utilisateur.save(update_fields=["password"])
        form = ReinitialisationForm({"email": utilisateur.email or utilisateur.email_entreprise})
        if form.is_valid():
            try:
                form.save(request=request, use_https=request.is_secure(), **GABARITS_EMAIL)
                fait["lien"] = True
            except Exception:
                logger.exception("Envoi du lien de réinitialisation impossible")

    # 3) Direction de la société prévenue
    direction = []
    if getattr(utilisateur, "societe_id", None):
        for d in Utilisateur.objects.filter(societe_id=utilisateur.societe_id, role="direction", is_active=True) \
                .exclude(pk=utilisateur.pk):
            direction += adresses_alerte(d)[:1]
    contexte = {
        "user": utilisateur, "evenement": evenement, "quand": timezone.localtime(),
        "ip": ip_client(request), "navigateur": navigateur(request),
    }
    if direction and _envoyer(_("CarsCosts – alerte de sécurité sur un compte"), "email_alerte_direction",
                              contexte, direction):
        fait["direction"] = len(direction)

    # 4) Journal
    try:
        UserLog.objects.create(
            utilisateur=utilisateur,
            action=f"Sécurité : « ce n'était pas moi » ({evenement}) – mot de passe bloqué, sessions déconnectées "
                   f"– IP {ip_client(request)}",
        )
    except Exception:
        pass
    return fait
