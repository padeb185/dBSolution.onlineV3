"""Mémorise l'utilisateur de la requête : les notifications indiquent qui a déclenché l'action."""
from contextvars import ContextVar

_utilisateur = ContextVar("utilisateur_courant", default=None)


def utilisateur_courant():
    return _utilisateur.get()


class UtilisateurCourantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        jeton = _utilisateur.set(user if user is not None and user.is_authenticated else None)
        try:
            return self.get_response(request)
        finally:
            _utilisateur.reset(jeton)
