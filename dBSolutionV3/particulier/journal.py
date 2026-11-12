"""Journal des actions d'abonnement (page « Abonnements et notifications » du monitoring des particuliers).

Ne bloque jamais l'action journalisée : une erreur d'écriture est seulement consignée dans les logs.
"""
import logging

log = logging.getLogger(__name__)


def _texte(valeur):
    if valeur is None or isinstance(valeur, (bool, int, float, str)):
        return valeur
    if isinstance(valeur, (list, tuple)):
        return [_texte(v) for v in valeur]
    if isinstance(valeur, dict):
        return {str(k): _texte(v) for k, v in valeur.items()}
    return str(valeur)


def noter(categorie, type="", utilisateur=None, message="", succes=True, destinataire="", **details):
    from django.db import transaction
    from .models import JournalAbonnement
    try:
        with transaction.atomic():      # point de sauvegarde : une erreur ici n'annule pas la requête en cours
            return JournalAbonnement.objects.create(
                categorie=categorie, type=(type or "")[:60], utilisateur=utilisateur, message=message or "",
                succes=succes, destinataire=(destinataire or "")[:255],
                details=_texte({k: v for k, v in details.items() if v not in (None, "", [], {})}))
    except Exception:
        log.exception("Journal d'abonnement non écrit (%s %s)", categorie, type)
        return None


def noter_email_compte(utilisateur, type, sujet, succes, destinataires, erreur=""):
    """E-mail envoyé par la connexion web (mot de passe oublié, alerte de sécurité…) : journalisé dans le
    schéma des particuliers, seulement pour les comptes particuliers."""
    if utilisateur is None or getattr(utilisateur, "role", None) != "particulier":
        return None
    try:
        from django_tenants.utils import schema_context
        from .api.base import schema_particuliers
        with schema_context(schema_particuliers()):
            return noter("email", type, utilisateur, sujet, succes,
                         destinataire=", ".join(d for d in destinataires if d), erreur=erreur[:500])
    except Exception:
        log.exception("Journal de l'e-mail %s non écrit", type)
        return None


def purger(jours=365):
    """Supprime les entrées de plus d'un an (appelé par la tâche quotidienne)."""
    from datetime import timedelta
    from django.utils import timezone
    from .models import JournalAbonnement
    return JournalAbonnement.objects.filter(date__lt=timezone.now() - timedelta(days=jours)).delete()[0]
