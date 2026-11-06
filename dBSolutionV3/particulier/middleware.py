"""
Les comptes particuliers n'utilisent que l'application (API /api/v1/) : ils partagent un même
tenant, dont les pages web professionnelles ne sont pas filtrées par propriétaire.
Toute tentative d'accès web est refusée (déconnexion).
"""
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import gettext as _

CHEMINS_LIBRES = ("/api/", "/static/", "/media/", "/i18n/")


class ParticulierWebMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        path = request.path_info or "/"
        if (user is not None and user.is_authenticated and getattr(user, "role", None) == "particulier"
                and not any(path.startswith(c) or c in path for c in CHEMINS_LIBRES)
                and "/connexion/" not in path):
            logout(request)
            messages.info(request, _("Les comptes particuliers s'utilisent dans l'application CarsCosts (iPhone, Android, Mac, Windows)."))
            return redirect("/fr/connexion/")
        return self.get_response(request)
