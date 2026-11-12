"""
Notifications d'abonnement des particuliers : e-mail (SMTP Brevo) et push (Firebase Cloud Messaging).

Envoyées :
  - aussitôt après un changement signalé par un store (abonnements._enregistrer → apres_changement) :
      paiement_refuse    paiement refusé, délai de grâce en cours
      acces_limite       paiement refusé définitivement : retour à la formule gratuite (lecture seule)
      expiree            formule arrivée à échéance sans renouvellement
      paiement_retabli   paiement passé après un refus
  - chaque jour par la commande « python manage.py notifier_abonnements » (cron) :
      renouvellement_proche  renouvellement annuel dans 7 jours
      fin_proche             formule non renouvelée qui se termine dans 3 jours
      grace_fin_proche       délai de grâce qui se termine dans 2 jours
      acces_limite / expiree si l'échéance est passée sans notification d'un store

Chaque notification n'est envoyée qu'une fois par échéance (modèle NotificationAbonnement).

Réglages (.env → settings.py) :
  FIREBASE_SERVICE_ACCOUNT_FILE  clé JSON d'un compte de service du projet Firebase (vide : pas de push)
  FIREBASE_PROJECT_ID            identifiant du projet Firebase (défaut : project_id de la clé JSON)
"""
import json
import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from . import abonnements
from .models import (AbonnementParticulier, AppareilNotification, Formule, NotificationAbonnement,
                     PeriodeFacturation, PreferencesParticulier, StatutPaiement)

log = logging.getLogger(__name__)

_jeton_firebase = {}


# ------------------------------------------------------------------ déclencheurs
def apres_changement(ab_id, avant):
    """Compare l'état avant / après une mise à jour par un store et notifie l'utilisateur si nécessaire."""
    ab = AbonnementParticulier.objects.select_related("utilisateur").filter(pk=ab_id).first()
    if ab is None or ab.formule == Formule.GRATUIT:
        return
    user = ab.utilisateur
    formule = abonnements.formule_effective(user, ab)
    if ab.statut_paiement == StatutPaiement.GRACE and avant["statut"] != StatutPaiement.GRACE \
            and formule != Formule.GRATUIT:
        notifier(user, ab, "paiement_refuse")
    elif formule == Formule.GRATUIT and avant["formule"] != Formule.GRATUIT:
        notifier(user, ab, "acces_limite" if ab.statut_paiement != StatutPaiement.OK else "expiree")
    elif (ab.statut_paiement == StatutPaiement.OK and avant["statut"] != StatutPaiement.OK
          and formule != Formule.GRATUIT):
        notifier(user, ab, "paiement_retabli")


def tache_quotidienne(maintenant=None):
    """Rappels liés aux dates (commande notifier_abonnements). Renvoie le nombre de notifications envoyées."""
    maintenant = maintenant or timezone.now()
    envoyees = 0
    for ab in AbonnementParticulier.objects.exclude(formule=Formule.GRATUIT).select_related("utilisateur"):
        user = ab.utilisateur
        formule = abonnements.formule_effective(user, ab, maintenant)
        type_ = None
        if formule == Formule.GRATUIT:
            # Échéance passée (délai de grâce terminé, formule non renouvelée…) : prévenir une fois
            recente = bool(ab.date_fin and ab.date_fin > maintenant - timedelta(days=30))
            if recente or ab.statut_paiement != StatutPaiement.OK:
                type_ = "acces_limite" if ab.statut_paiement != StatutPaiement.OK else "expiree"
        elif ab.statut_paiement == StatutPaiement.GRACE and ab.date_fin_grace \
                and ab.date_fin_grace - maintenant <= timedelta(days=2):
            type_ = "grace_fin_proche"
        elif ab.date_fin and ab.statut_paiement == StatutPaiement.OK and ab.date_fin > maintenant:
            reste = ab.date_fin - maintenant
            if ab.renouvellement_auto and ab.periode == PeriodeFacturation.ANNUEL and reste <= timedelta(days=7):
                type_ = "renouvellement_proche"
            elif not ab.renouvellement_auto and reste <= timedelta(days=3):
                type_ = "fin_proche"
        if type_ and notifier(user, ab, type_):
            envoyees += 1
    return envoyees


# ------------------------------------------------------------------ envoi
def cle_echeance(ab, type_):
    """Une notification par type et par échéance (date de fin, ou fin du délai de grâce)."""
    d = ab.date_fin_grace if type_ in ("paiement_refuse", "grace_fin_proche") else ab.date_fin
    return d.date().isoformat() if d else "-"


def notifier(user, ab, type_):
    """Envoie la notification si elle ne l'a pas déjà été pour cette échéance. Renvoie True si envoyée."""
    cle = cle_echeance(ab, type_)
    try:
        with transaction.atomic():
            trace, cree = NotificationAbonnement.objects.get_or_create(utilisateur=user, type=type_, cle=cle)
    except IntegrityError:
        return False
    if not cree:
        return False
    langue = (PreferencesParticulier.objects.filter(utilisateur=user).values_list("langue", flat=True).first()
              or "fr")
    with translation.override(langue):
        sujet, texte = message(ab, type_)
        canaux = []
        if envoyer_email(user, sujet, texte):
            canaux.append("email")
        if envoyer_push(user, sujet, texte, {"type": type_}):
            canaux.append("push")
    trace.canaux = ",".join(canaux)
    trace.save(update_fields=["canaux"])
    return True


def message(ab, type_):
    """(sujet, texte) dans la langue active."""
    f = Formule(ab.formule).label
    contexte = {"f": f, "store": abonnements.nom_store(ab.source), "fin": abonnements.date_courte(ab.date_fin),
                "grace": abonnements.date_courte(ab.date_fin_grace),
                "n": abonnements.LIMITES[Formule.GRATUIT]}
    textes = {
        "paiement_refuse": (
            _("CarsCosts : paiement de votre formule %(f)s refusé"),
            _("Le paiement du renouvellement de votre formule %(f)s a été refusé. %(store)s va réessayer "
              "automatiquement. Mettez à jour votre moyen de paiement dans %(store)s avant le %(grace)s : "
              "après cette date, vos véhicules au-delà de %(n)d passeront en lecture seule.")),
        "grace_fin_proche": (
            _("CarsCosts : votre formule %(f)s sera suspendue le %(grace)s"),
            _("Le paiement de votre formule %(f)s n'a toujours pas abouti. Sans paiement d'ici le %(grace)s, "
              "vos véhicules au-delà de %(n)d passeront en lecture seule. Mettez à jour votre moyen de paiement "
              "dans %(store)s.")),
        "acces_limite": (
            _("CarsCosts : formule %(f)s suspendue"),
            _("Le paiement de votre formule %(f)s n'a pas abouti : elle est suspendue. Vos données sont "
              "conservées, mais les véhicules au-delà de %(n)d sont en lecture seule. Tout redevient modifiable "
              "dès que le paiement est accepté par %(store)s.")),
        "expiree": (
            _("CarsCosts : votre formule %(f)s est terminée"),
            _("Votre formule %(f)s est arrivée à échéance. Vos données sont conservées, mais les véhicules "
              "au-delà de %(n)d sont en lecture seule. Vous pouvez reprendre une formule à tout moment dans "
              "l'application.")),
        "paiement_retabli": (
            _("CarsCosts : paiement reçu, formule %(f)s active"),
            _("Merci ! Le paiement de votre formule %(f)s a été accepté. Toutes les fonctions sont de nouveau "
              "disponibles. Prochain renouvellement : %(fin)s.")),
        "renouvellement_proche": (
            _("CarsCosts : renouvellement de votre formule %(f)s le %(fin)s"),
            _("Votre formule %(f)s (annuelle) sera renouvelée automatiquement le %(fin)s par %(store)s. "
              "Pour la modifier ou la résilier, ouvrez la gestion des abonnements de %(store)s.")),
        "fin_proche": (
            _("CarsCosts : votre formule %(f)s se termine le %(fin)s"),
            _("Votre formule %(f)s se termine le %(fin)s et ne sera pas renouvelée. Après cette date, les "
              "véhicules au-delà de %(n)d passeront en lecture seule. Vous pouvez réactiver le renouvellement "
              "dans l'application.")),
    }
    sujet, texte = textes[type_]
    return sujet % contexte, texte % contexte


def envoyer_email(user, sujet, texte):
    if not getattr(user, "email", ""):
        return False
    corps = "%s\n\n%s\n\n%s" % (_("Bonjour %(prenom)s,") % {"prenom": getattr(user, "prenom", "") or ""},
                                texte, _("L'équipe CarsCosts"))
    try:
        send_mail(sujet, corps, None, [user.email])
        return True
    except Exception:
        log.exception("E-mail d'abonnement non envoyé à %s", user.pk)
        return False


def envoyer_push(user, titre, corps, donnees=None):
    """Push FCM (HTTP v1) vers tous les appareils de l'utilisateur. Jetons invalides supprimés."""
    import requests

    chemin = getattr(settings, "FIREBASE_SERVICE_ACCOUNT_FILE", "")
    appareils = list(AppareilNotification.objects.filter(utilisateur=user))
    if not chemin or not appareils:
        return False
    try:
        projet = getattr(settings, "FIREBASE_PROJECT_ID", "")
        if not projet:
            with open(chemin) as f:
                projet = json.load(f).get("project_id", "")
        jeton = abonnements.jeton_compte_service(chemin, "https://www.googleapis.com/auth/firebase.messaging",
                                                 _jeton_firebase)
    except Exception:
        log.exception("Firebase non configuré correctement")
        return False
    url = "https://fcm.googleapis.com/v1/projects/%s/messages:send" % projet
    envoye = False
    for appareil in appareils:
        try:
            r = requests.post(url, timeout=10, headers={"Authorization": "Bearer " + jeton}, json={"message": {
                "token": appareil.jeton,
                "notification": {"title": titre, "body": corps},
                "data": {k: str(v) for k, v in (donnees or {}).items()},
            }})
        except requests.RequestException:
            log.warning("FCM injoignable")
            continue
        if r.status_code == 200:
            envoye = True
        elif r.status_code == 404 or "UNREGISTERED" in r.text:
            appareil.delete()      # application désinstallée ou jeton périmé
        else:
            log.warning("FCM %s : %s", r.status_code, r.text[:300])
    return envoye
