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
    from .models import JournalAbonnement
    try:
        return JournalAbonnement.objects.create(
            categorie=categorie, type=(type or "")[:60], utilisateur=utilisateur, message=message or "",
            succes=succes, destinataire=(destinataire or "")[:255],
            details=_texte({k: v for k, v in details.items() if v not in (None, "", [], {})}))
    except Exception:
        log.exception("Journal d'abonnement non écrit (%s %s)", categorie, type)
        return None


def purger(jours=365):
    """Supprime les entrées de plus d'un an (appelé par la tâche quotidienne)."""
    from datetime import timedelta
    from django.utils import timezone
    from .models import JournalAbonnement
    return JournalAbonnement.objects.filter(date__lt=timezone.now() - timedelta(days=jours)).delete()[0]
