"""
Formules de l'application des particuliers et achats intégrés (App Store / Google Play).

    Gratuit 1 véhicule · Bronze 2 · Silver 5 · Gold 10 (seuls les véhicules non archivés comptent)

Attribution d'une formule :
  - par l'administration (page « Particuliers – administration » ou admin Django), source « admin » ;
  - par un achat dans l'application : l'app envoie la preuve d'achat à POST /api/v1/abonnement/achat/,
    le serveur la vérifie auprès d'Apple / Google puis enregistre la formule et sa date de fin ;
  - renouvellements, résiliations et remboursements : notifications des stores
    (Apple « App Store Server Notifications V2 », Google « Real-time developer notifications »).

Facturation : période mensuelle ou annuelle (d'après l'identifiant produit), date du premier achat,
date de la dernière facturation et date de renouvellement (= date_fin si le renouvellement est actif).

Paiement refusé (statut_paiement) :
  - « grace »  : le store réessaie le paiement, la formule reste active jusqu'à date_fin_grace ;
  - « echec »  : délai de grâce dépassé ou compte suspendu par le store, retour à la formule gratuite.
  Formule gratuite avec plus de véhicules actifs que la limite : les véhicules au-delà (les plus récents)
  passent en lecture seule ; rien n'est supprimé, tout redevient modifiable dès que le paiement passe.
  Notifications (e-mail, push) : voir notifications.py et la commande « notifier_abonnements ».

Réglages (.env → settings.py) :
  PARTICULIERS_ACHATS_MODE      "test" (développement : achats de test acceptés sans store)
                                ou "store" (production : seules les preuves vérifiées par les stores)
  PARTICULIERS_ACHATS_SANDBOX   accepter les achats « Sandbox » des stores (testeurs) – défaut : DEBUG
  PARTICULIERS_PRODUITS         identifiant produit → formule (même identifiants dans les deux stores)
  APPLE_BUNDLE_ID, APPLE_ROOT_CA_G3 (chemin de AppleRootCA-G3.cer)
  GOOGLE_PACKAGE_NAME, GOOGLE_SERVICE_ACCOUNT_FILE (clé JSON du compte de service Play Console),
  GOOGLE_RTDN_JETON (secret ajouté à l'URL de la notification Pub/Sub)
"""
import base64
import json
import logging
import time
from datetime import datetime, timedelta, timezone as dt_timezone

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import (AbonnementParticulier, Formule, PeriodeFacturation, SourceAbonnement, StatutPaiement,
                     Vehicule)

log = logging.getLogger(__name__)

LIMITES = {Formule.GRATUIT: 1, Formule.BRONZE: 2, Formule.SILVER: 5, Formule.GOLD: 10}
ORDRE = [Formule.GRATUIT, Formule.BRONZE, Formule.SILVER, Formule.GOLD]

PRODUITS_DEFAUT = {
    "carscosts_bronze_mensuel": Formule.BRONZE,
    "carscosts_silver_mensuel": Formule.SILVER,
    "carscosts_gold_mensuel": Formule.GOLD,
    "carscosts_bronze_annuel": Formule.BRONZE,
    "carscosts_silver_annuel": Formule.SILVER,
    "carscosts_gold_annuel": Formule.GOLD,
}
MOTS_ANNUELS = ("annuel", "annual", "yearly", "annee", "year")


class AchatRefuse(Exception):
    """Preuve d'achat invalide, expirée ou déjà liée à un autre compte (message pour l'utilisateur)."""

    def __init__(self, message, statut=400):
        super().__init__(message)
        self.statut = statut


# ------------------------------------------------------------------ réglages
def mode_achats():
    return getattr(settings, "PARTICULIERS_ACHATS_MODE", None) or ("test" if settings.DEBUG else "store")


def sandbox_accepte():
    valeur = getattr(settings, "PARTICULIERS_ACHATS_SANDBOX", None)
    return settings.DEBUG if valeur is None else bool(valeur)


def produits():
    return dict(getattr(settings, "PARTICULIERS_PRODUITS", None) or PRODUITS_DEFAUT)


def formule_du_produit(produit):
    formule = produits().get(produit)
    if formule not in LIMITES:
        raise AchatRefuse(_("Produit inconnu : %s") % produit)
    return formule


def periode_du_produit(produit):
    """Période de facturation d'après l'identifiant produit (…_annuel → annuel, sinon mensuel)."""
    if not produit:
        return PeriodeFacturation.AUCUNE
    nom = produit.lower()
    return PeriodeFacturation.ANNUEL if any(m in nom for m in MOTS_ANNUELS) else PeriodeFacturation.MENSUEL


def _moins_une_periode(date_fin, periode):
    """Date de la dernière facturation déduite de la date de renouvellement (Google ne la donne pas)."""
    if not date_fin or not periode:
        return None
    from .calculs import ajouter_mois
    mois = 12 if periode == PeriodeFacturation.ANNUEL else 1
    jour = ajouter_mois(date_fin.date(), -mois)
    return date_fin.replace(year=jour.year, month=jour.month, day=jour.day)


# ------------------------------------------------------------------ formule d'un compte
def abonnement(user):
    return AbonnementParticulier.objects.filter(utilisateur=user).first()


def formule_effective(user, ab=None, maintenant=None):
    """ab=None : lu en base ; ab=False : compte sans abonnement (déjà vérifié par l'appelant)."""
    ab = ab if ab is not None else abonnement(user)
    if not ab or ab.formule not in LIMITES:
        return Formule.GRATUIT
    maintenant = maintenant or timezone.now()
    if ab.statut_paiement == StatutPaiement.ECHEC:
        return Formule.GRATUIT
    # Paiement refusé, le store réessaie : la formule reste active pendant le délai de grâce
    if ab.statut_paiement == StatutPaiement.GRACE and ab.date_fin_grace and ab.date_fin_grace > maintenant:
        return ab.formule
    if ab.date_fin and ab.date_fin <= maintenant:
        return Formule.GRATUIT
    return ab.formule


def vehicules_lecture_seule(user, formule=None):
    """Véhicules actifs au-delà de la limite de la formule (les plus récents) : consultables, non modifiables."""
    limite = LIMITES[formule or formule_effective(user)]
    ids = list(Vehicule.objects.filter(proprietaire=user, archive=False)
               .order_by("created_at", "pk").values_list("pk", flat=True))
    return ids[limite:]


def est_en_lecture_seule(user, vehicule_id):
    return any(str(v) == str(vehicule_id) for v in vehicules_lecture_seule(user))


def vehicules_actifs(user, sauf=None):
    qs = Vehicule.objects.filter(proprietaire=user, archive=False)
    if sauf is not None:
        qs = qs.exclude(pk=sauf.pk)
    return qs.count()


def etat(user):
    """État de l'abonnement pour l'application (GET abonnement/, moi/, tableau-de-bord/)."""
    ab = abonnement(user)
    formule = formule_effective(user, ab)
    limite = LIMITES[formule]
    actifs = vehicules_actifs(user)
    echue = bool(ab and ab.formule != Formule.GRATUIT and formule == Formule.GRATUIT)
    par_formule, par_periode = {}, {}
    for produit, f in produits().items():
        par_formule.setdefault(f, []).append(produit)
        par_periode.setdefault((f, periode_du_produit(produit)), []).append(produit)
    lecture_seule = vehicules_lecture_seule(user, formule) if actifs > limite else []
    statut = ab.statut_paiement if ab and ab.formule != Formule.GRATUIT else StatutPaiement.OK
    payant = bool(ab and ab.source in (SourceAbonnement.APPLE, SourceAbonnement.GOOGLE, SourceAbonnement.TEST))

    def iso(d):
        return d.isoformat() if d else None
    return {
        "formule": formule,
        "libelle": Formule(formule).label,
        "limite": limite,
        "vehicules_actifs": actifs,
        "peut_ajouter": actifs < limite,
        "date_fin": ab.date_fin.isoformat() if ab and ab.date_fin and not echue else None,
        "source": (ab.source or None) if ab and not echue else None,
        "renouvellement_auto": bool(ab and ab.renouvellement_auto and not echue),
        "echue": echue,
        "formule_echue": ab.formule if echue else None,
        # Facturation (abonnements achetés dans l'application)
        "periode": (ab.periode or None) if ab and payant else None,
        "date_debut": iso(ab.date_debut) if ab and payant else None,
        "date_derniere_facturation": iso(ab.date_derniere_facturation) if ab and payant else None,
        "date_renouvellement": iso(ab.date_fin) if ab and payant and ab.renouvellement_auto
                               and statut == StatutPaiement.OK and not echue else None,
        "statut_paiement": statut,
        "date_fin_grace": iso(ab.date_fin_grace) if ab and statut == StatutPaiement.GRACE else None,
        "vehicules_lecture_seule": [str(v) for v in lecture_seule],
        "alerte": alerte(ab, formule, limite, lecture_seule),
        "formules": [{"code": f.value, "libelle": f.label, "limite": LIMITES[f], "produits": par_formule.get(f, []),
                      "produits_mensuels": par_periode.get((f, PeriodeFacturation.MENSUEL), []),
                      "produits_annuels": par_periode.get((f, PeriodeFacturation.ANNUEL), [])}
                     for f in ORDRE],
        "mode_achats": mode_achats(),
    }


def nom_store(source):
    return {SourceAbonnement.APPLE: "App Store", SourceAbonnement.GOOGLE: "Google Play"}.get(source, _("votre store"))


def date_courte(d):
    return timezone.localtime(d).strftime("%d/%m/%Y") if d else ""


def alerte(ab, formule, limite, lecture_seule, maintenant=None):
    """Bandeau affiché dans l'application : {niveau: info|avertissement|erreur, code, message} ou None."""
    if not ab or ab.formule == Formule.GRATUIT:
        return None
    maintenant = maintenant or timezone.now()
    libelle = Formule(ab.formule).label
    if formule != Formule.GRATUIT and ab.statut_paiement == StatutPaiement.GRACE:
        return {"niveau": "avertissement", "code": "paiement_refuse", "message": _(
            "Le paiement de votre formule %(f)s a été refusé. Mettez à jour votre moyen de paiement dans "
            "%(store)s avant le %(date)s pour conserver toutes les fonctions.")
            % {"f": libelle, "store": nom_store(ab.source), "date": date_courte(ab.date_fin_grace)}}
    if formule == Formule.GRATUIT:
        if ab.statut_paiement in (StatutPaiement.ECHEC, StatutPaiement.GRACE):
            message = _("Le paiement de votre formule %(f)s n'a pas abouti : elle est suspendue.") % {"f": libelle}
        else:
            message = _("Votre formule %(f)s est arrivée à échéance.") % {"f": libelle}
        if lecture_seule:
            message += " " + _("Les véhicules au-delà de %(n)d sont en lecture seule jusqu'au renouvellement.") % {
                "n": limite}
        return {"niveau": "erreur", "code": "acces_limite", "message": message}
    if not ab.renouvellement_auto and ab.date_fin and ab.date_fin - maintenant <= timedelta(days=7):
        return {"niveau": "info", "code": "fin_proche", "message": _(
            "Votre formule %(f)s se termine le %(date)s et ne sera pas renouvelée.")
            % {"f": libelle, "date": date_courte(ab.date_fin)}}
    return None


def verifier_limite(user, sauf=None):
    """Lève LimiteAtteinte si l'utilisateur ne peut pas avoir un véhicule actif de plus."""
    formule = formule_effective(user)
    limite = LIMITES[formule]
    actifs = vehicules_actifs(user, sauf=sauf)
    if actifs >= limite:
        raise LimiteAtteinte(formule, limite, actifs)


class LimiteAtteinte(Exception):
    def __init__(self, formule, limite, actifs):
        self.formule, self.limite, self.actifs = formule, limite, actifs
        suivante = next((f for f in ORDRE if LIMITES[f] > limite), None)
        if suivante:
            message = (_("Votre formule %(f)s permet %(n)d véhicule(s) actif(s). Passez à la formule %(s)s "
                       "pour en ajouter (jusqu'à %(m)d), ou archivez un véhicule vendu.")
                       % {"f": Formule(formule).label, "n": limite, "s": Formule(suivante).label,
                          "m": LIMITES[suivante]})
        else:
            message = (_("La formule %(f)s permet au maximum %(n)d véhicules actifs : archivez un véhicule vendu "
                       "pour en ajouter un.") % {"f": Formule(formule).label, "n": limite})
        super().__init__(message)
        self.message = message
        self.suivante = suivante


# ------------------------------------------------------------------ attribution
def attribuer(user, formule, date_fin=None, source=SourceAbonnement.ADMIN, note=""):
    """Attribution par l'administration (ou retour à la formule gratuite)."""
    ab, _c = AbonnementParticulier.objects.get_or_create(utilisateur=user)
    ab.formule = formule
    ab.date_fin = date_fin
    ab.source = source if formule != Formule.GRATUIT else ""
    ab.note = note or ab.note
    if source == SourceAbonnement.ADMIN:
        ab.produit, ab.reference_store, ab.environnement, ab.renouvellement_auto = "", None, "", False
        ab.periode, ab.date_debut, ab.date_derniere_facturation = "", None, None
        ab.statut_paiement, ab.date_fin_grace = StatutPaiement.OK, None
    ab.save()
    return ab


def _enregistrer(user, achat):
    """achat : dict(source, produit, reference, date_fin, environnement, renouvellement_auto, revoque,
    et facultatifs : date_debut, date_facturation, statut_paiement, date_fin_grace)."""
    formule = formule_du_produit(achat["produit"])
    with transaction.atomic():
        autre = (AbonnementParticulier.objects.select_for_update()
                 .filter(reference_store=achat["reference"]).exclude(utilisateur=user).first())
        if autre is not None:
            raise AchatRefuse(_("Cet abonnement est déjà utilisé par un autre compte CarsCosts."), statut=409)
        ab, _c = AbonnementParticulier.objects.select_for_update().get_or_create(utilisateur=user)
        avant = {"formule": formule_effective(user, ab), "statut": ab.statut_paiement, "formule_ab": ab.formule}
        # Un abonnement attribué par l'administration, sans fin ou plus long, n'est pas remplacé.
        if (ab.source == SourceAbonnement.ADMIN and formule_effective(user, ab) != Formule.GRATUIT
                and ORDRE.index(ab.formule) >= ORDRE.index(formule)
                and (ab.date_fin is None or (achat["date_fin"] and ab.date_fin >= achat["date_fin"]))):
            return ab
        ab.formule = formule
        ab.date_fin = achat["date_fin"]
        if achat.get("revoque"):
            ab.date_fin = timezone.now()
        ab.source = achat["source"]
        ab.produit = achat["produit"]
        ab.reference_store = achat["reference"]
        ab.environnement = achat.get("environnement", "")
        ab.renouvellement_auto = bool(achat.get("renouvellement_auto")) and not achat.get("revoque")
        ab.periode = periode_du_produit(achat["produit"])
        ab.date_debut = achat.get("date_debut") or ab.date_debut or timezone.now()
        statut = achat.get("statut_paiement")
        if statut is None:
            # Preuve envoyée par l'application : payée si la date de fin est future, sinon statut inchangé
            statut = StatutPaiement.OK if ab.date_fin and ab.date_fin > timezone.now() else ab.statut_paiement
        ab.statut_paiement = statut
        ab.date_fin_grace = achat.get("date_fin_grace") if statut == StatutPaiement.GRACE else None
        # Dernière facturation : donnée par Apple ; Google : date de renouvellement moins une période
        ab.date_derniere_facturation = (
            achat.get("date_facturation")
            or (_moins_une_periode(ab.date_fin, ab.periode) if statut == StatutPaiement.OK else None)
            or ab.date_derniere_facturation)
        try:
            ab.save()
        except IntegrityError:
            raise AchatRefuse(_("Cet abonnement est déjà utilisé par un autre compte CarsCosts."), statut=409)
        ab_id = ab.pk
        transaction.on_commit(lambda: _notifier(ab_id, avant))
    return ab


def _notifier(ab_id, avant):
    from . import notifications
    try:
        notifications.apres_changement(ab_id, avant)
    except Exception:       # une notification ratée ne doit jamais bloquer l'achat
        log.exception("Notification d'abonnement impossible (%s)", ab_id)


def valider_achat(user, plateforme, produit, jeton):
    """Vérifie une preuve d'achat et met à jour la formule du compte. Renvoie l'abonnement."""
    plateforme = (plateforme or "").lower()
    if not jeton:
        raise AchatRefuse(_("Preuve d'achat manquante."))
    if plateforme == "test":
        if mode_achats() != "test":
            raise AchatRefuse(_("Les achats de test ne sont pas acceptés sur ce serveur."), statut=403)
        maintenant = timezone.now()
        jours = 365 if periode_du_produit(produit) == PeriodeFacturation.ANNUEL else 30
        achat = {"source": SourceAbonnement.TEST, "produit": produit, "reference": "test-%s" % user.pk,
                 "date_fin": maintenant + timedelta(days=jours), "environnement": "Test",
                 "renouvellement_auto": False, "date_facturation": maintenant,
                 "statut_paiement": StatutPaiement.OK}
    elif plateforme == "apple":
        achat = transaction_apple(jeton)
    elif plateforme == "google":
        achat = abonnement_google(produit, jeton)
    else:
        raise AchatRefuse(_("Plateforme inconnue."))
    if achat["environnement"].lower() == "sandbox" and not sandbox_accepte():
        raise AchatRefuse(_("Achat de test (Sandbox) refusé par le serveur de production."), statut=403)
    if achat["date_fin"] and achat["date_fin"] <= timezone.now():
        # Achat restauré mais échu : on l'enregistre (historique), la formule effective reste gratuite.
        log.info("Abonnement échu restauré pour %s", user.pk)
    return _enregistrer(user, achat)


def mettre_a_jour_par_reference(reference, achat, anciennes_references=()):
    """Notification d'un store : met à jour l'abonnement lié à cette référence (s'il existe)."""
    refs = [reference, *[r for r in anciennes_references if r]]
    ab = AbonnementParticulier.objects.filter(reference_store__in=refs).select_related("utilisateur").first()
    if ab is None:
        return None
    return _enregistrer(ab.utilisateur, achat)


# ==================================================================
# APPLE – transactions signées StoreKit 2 (JWS) vérifiées localement
# ==================================================================
OID_FEUILLE_APPLE = "1.2.840.113635.100.6.11.1"
OID_INTERMEDIAIRE_APPLE = "1.2.840.113635.100.6.2.1"


def _b64url(donnee):
    return base64.urlsafe_b64decode(donnee + "=" * (-len(donnee) % 4))


def verifier_jws_apple(jws):
    """Vérifie la signature d'un JWS Apple (chaîne x5c jusqu'à Apple Root CA G3) et renvoie le contenu."""
    import jwt
    from cryptography import x509

    chemin_racine = getattr(settings, "APPLE_ROOT_CA_G3", "")
    if not chemin_racine:
        raise AchatRefuse(_("Vérification Apple non configurée (APPLE_ROOT_CA_G3)."), statut=503)
    try:
        entete = json.loads(_b64url(jws.split(".")[0]))
        chaine = [x509.load_der_x509_certificate(base64.b64decode(c)) for c in entete["x5c"]]
    except Exception:
        raise AchatRefuse(_("Preuve d'achat Apple illisible."))
    if len(chaine) != 3:
        raise AchatRefuse(_("Chaîne de certificats Apple invalide."))
    with open(chemin_racine, "rb") as f:
        donnees = f.read()
    try:
        racine = x509.load_der_x509_certificate(donnees)
    except ValueError:
        racine = x509.load_pem_x509_certificate(donnees)
    feuille, intermediaire, racine_jws = chaine
    try:
        if racine_jws.fingerprint(racine_jws.signature_hash_algorithm) != racine.fingerprint(racine.signature_hash_algorithm):
            raise ValueError("racine")
        intermediaire.verify_directly_issued_by(racine)
        feuille.verify_directly_issued_by(intermediaire)
        maintenant = datetime.now(dt_timezone.utc)
        for c in (feuille, intermediaire):
            if not (c.not_valid_before_utc <= maintenant <= c.not_valid_after_utc):
                raise ValueError("expiré")
        oids_f = {e.oid.dotted_string for e in feuille.extensions}
        oids_i = {e.oid.dotted_string for e in intermediaire.extensions}
        if OID_FEUILLE_APPLE not in oids_f or OID_INTERMEDIAIRE_APPLE not in oids_i:
            raise ValueError("oid")
        return jwt.decode(jws, key=feuille.public_key(), algorithms=["ES256"], options={"verify_aud": False})
    except AchatRefuse:
        raise
    except Exception as e:
        log.warning("JWS Apple refusé : %s", e)
        raise AchatRefuse(_("Preuve d'achat Apple invalide."))


def _ms(valeur):
    return datetime.fromtimestamp(valeur / 1000, tz=dt_timezone.utc) if valeur else None


def _achat_apple(info):
    bundle = getattr(settings, "APPLE_BUNDLE_ID", "")
    if bundle and info.get("bundleId") != bundle:
        raise AchatRefuse(_("Achat d'une autre application."))
    return {
        "source": SourceAbonnement.APPLE,
        "produit": info.get("productId", ""),
        "reference": str(info.get("originalTransactionId") or info.get("transactionId")),
        "date_fin": _ms(info.get("expiresDate")),
        "date_debut": _ms(info.get("originalPurchaseDate")),
        "date_facturation": _ms(info.get("purchaseDate")),
        "environnement": info.get("environment", ""),
        "renouvellement_auto": True,
        "revoque": bool(info.get("revocationDate")),
    }


def transaction_apple(jws):
    return _achat_apple(verifier_jws_apple(jws))


def statut_paiement_apple(renouvellement, type_notification=None, maintenant=None):
    """Statut du paiement d'après les informations de renouvellement Apple (JWSRenewalInfo)."""
    maintenant = maintenant or timezone.now()
    fin_grace = _ms(renouvellement.get("gracePeriodExpiresDate"))
    if fin_grace and fin_grace > maintenant:
        return {"statut_paiement": StatutPaiement.GRACE, "date_fin_grace": fin_grace}
    if renouvellement.get("isInBillingRetryPeriod") or type_notification in ("GRACE_PERIOD_EXPIRED",):
        return {"statut_paiement": StatutPaiement.ECHEC}
    return {"statut_paiement": StatutPaiement.OK}


def notification_apple(signed_payload):
    """App Store Server Notifications V2 → mise à jour de l'abonnement concerné."""
    contenu = verifier_jws_apple(signed_payload)
    donnees = contenu.get("data") or {}
    if donnees.get("signedTransactionInfo"):
        achat = transaction_apple(donnees["signedTransactionInfo"])
        if donnees.get("signedRenewalInfo"):
            renouvellement = verifier_jws_apple(donnees["signedRenewalInfo"])
            achat["renouvellement_auto"] = renouvellement.get("autoRenewStatus") == 1
            achat.update(statut_paiement_apple(renouvellement, contenu.get("notificationType")))
        if contenu.get("notificationType") in ("REFUND", "REVOKE"):
            achat["revoque"] = True
        try:
            mettre_a_jour_par_reference(achat["reference"], achat)
        except AchatRefuse as e:
            log.warning("Notification Apple ignorée : %s", e)
    return contenu.get("notificationType")


# ==================================================================
# GOOGLE PLAY – API Google Play Developer (purchases.subscriptionsv2)
# ==================================================================
_jeton_google = {"valeur": None, "expire": 0}


def _acces_google():
    chemin = getattr(settings, "GOOGLE_SERVICE_ACCOUNT_FILE", "")
    if not chemin:
        raise AchatRefuse(_("Vérification Google Play non configurée (GOOGLE_SERVICE_ACCOUNT_FILE)."), statut=503)
    return jeton_compte_service(chemin, "https://www.googleapis.com/auth/androidpublisher", _jeton_google)


def jeton_compte_service(chemin, scope, cache):
    """Jeton OAuth2 d'un compte de service Google (Play Console, Firebase…), mis en cache dans `cache`."""
    import jwt
    import requests

    if cache.get("valeur") and cache.get("expire", 0) > time.time() + 60:
        return cache["valeur"]
    with open(chemin) as f:
        compte = json.load(f)
    maintenant = int(time.time())
    assertion = jwt.encode({
        "iss": compte["client_email"], "scope": scope,
        "aud": compte.get("token_uri", "https://oauth2.googleapis.com/token"), "iat": maintenant, "exp": maintenant + 3600,
    }, compte["private_key"], algorithm="RS256")
    r = requests.post(compte.get("token_uri", "https://oauth2.googleapis.com/token"), timeout=15, data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion})
    r.raise_for_status()
    d = r.json()
    cache.update(valeur=d["access_token"], expire=time.time() + int(d.get("expires_in", 3600)))
    return d["access_token"]


# Résilié (CANCELED) ou expiré : valable jusqu'à expiryTime (date_fin) ; achat en attente : pas d'accès
ETATS_GOOGLE_SANS_ACCES = {"SUBSCRIPTION_STATE_PENDING", "SUBSCRIPTION_STATE_PENDING_PURCHASE_CANCELED"}
# Paiement refusé : délai de grâce (accès conservé jusqu'à expiryTime, prolongé par Google) puis suspension
ETATS_GOOGLE_ECHEC = {"SUBSCRIPTION_STATE_ON_HOLD", "SUBSCRIPTION_STATE_PAUSED"}


def _iso(valeur):
    return datetime.fromisoformat(valeur.replace("Z", "+00:00")) if valeur else None


def statut_paiement_google(etat_g, date_fin):
    if etat_g == "SUBSCRIPTION_STATE_IN_GRACE_PERIOD":
        return {"statut_paiement": StatutPaiement.GRACE, "date_fin_grace": date_fin}
    if etat_g in ETATS_GOOGLE_ECHEC:
        return {"statut_paiement": StatutPaiement.ECHEC}
    return {"statut_paiement": StatutPaiement.OK}


def abonnement_google(produit, purchase_token):
    import requests

    package = getattr(settings, "GOOGLE_PACKAGE_NAME", "")
    if not package:
        raise AchatRefuse(_("Vérification Google Play non configurée (GOOGLE_PACKAGE_NAME)."), statut=503)
    url = ("https://androidpublisher.googleapis.com/androidpublisher/v3/applications/%s/purchases/"
           "subscriptionsv2/tokens/%s" % (package, purchase_token))
    try:
        r = requests.get(url, headers={"Authorization": "Bearer " + _acces_google()}, timeout=15)
    except requests.RequestException:
        raise AchatRefuse(_("Google Play injoignable, réessayez plus tard."), statut=503)
    if r.status_code in (400, 404, 410):
        raise AchatRefuse(_("Preuve d'achat Google Play invalide."))
    if r.status_code >= 300:
        log.warning("Google Play %s : %s", r.status_code, r.text[:300])
        raise AchatRefuse(_("Google Play injoignable, réessayez plus tard."), statut=503)
    d = r.json()
    lignes = d.get("lineItems") or []
    ligne = next((l for l in lignes if l.get("productId") == produit), lignes[0] if lignes else {})
    date_fin = _iso(ligne.get("expiryTime"))
    etat_g = d.get("subscriptionState", "")
    return {
        "source": SourceAbonnement.GOOGLE,
        "produit": ligne.get("productId", produit),
        "reference": purchase_token,
        "anciennes": [d.get("linkedPurchaseToken")],
        "date_fin": date_fin,
        "date_debut": _iso(d.get("startTime")),
        **statut_paiement_google(etat_g, date_fin),
        "environnement": "Sandbox" if "testPurchase" in d else "Production",
        "renouvellement_auto": etat_g in ("SUBSCRIPTION_STATE_ACTIVE", "SUBSCRIPTION_STATE_IN_GRACE_PERIOD")
                               and bool((ligne.get("autoRenewingPlan") or {}).get("autoRenewEnabled")),
        # Achat en attente de paiement : pas d'accès à la formule
        "revoque": etat_g in ETATS_GOOGLE_SANS_ACCES,
    }


def notification_google(message):
    """Notification Pub/Sub (RTDN) : on relit l'état de l'abonnement auprès de Google."""
    d = json.loads(base64.b64decode(message.get("data") or "e30=") or b"{}")
    notif = d.get("subscriptionNotification")
    if not notif:
        return None     # testNotification, achats ponctuels…
    achat = abonnement_google(notif.get("subscriptionId", ""), notif["purchaseToken"])
    try:
        mettre_a_jour_par_reference(achat["reference"], achat, achat.get("anciennes", ()))
    except AchatRefuse as e:
        log.warning("Notification Google ignorée : %s", e)
    return notif.get("notificationType")
