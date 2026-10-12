"""
Langue lue dans l'URL après le préfixe du tenant.

Avec django-tenants en sous-dossier, les URLs ont la forme
    /tenant/<schema>/<langue>/...
Le LocaleMiddleware de Django ne cherche la langue qu'au tout début du chemin
(/<langue>/...) : il ne la trouve pas et se rabat sur le cookie / le navigateur.
Si ce cookie vaut « en », toutes les URLs en /fr/ donnent une 404.

Ce middleware (placé juste après LocaleMiddleware) active la langue présente
dans l'URL et met le cookie de langue à jour.
"""
import re

from django.conf import settings
from django.utils import translation

PREFIXE = getattr(settings, "TENANT_SUBFOLDER_PREFIX", "tenant").strip("/")
MOTIF = re.compile(r"^/%s/[^/]+/([\w@-]+)(?:/|$)" % re.escape(PREFIXE))


def langue_depuis_chemin(chemin):
    correspondance = MOTIF.match(chemin or "")
    if not correspondance:
        return None
    try:
        return translation.get_supported_language_variant(correspondance.group(1), strict=True)
    except LookupError:
        return None


class TenantLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        langue = langue_depuis_chemin(request.path_info)
        if langue:
            translation.activate(langue)
            request.LANGUAGE_CODE = langue

        response = self.get_response(request)

        if langue:
            nom_cookie = settings.LANGUAGE_COOKIE_NAME
            if request.COOKIES.get(nom_cookie) != langue:
                response.set_cookie(
                    nom_cookie,
                    langue,
                    max_age=settings.LANGUAGE_COOKIE_AGE,
                    path=settings.LANGUAGE_COOKIE_PATH,
                    domain=settings.LANGUAGE_COOKIE_DOMAIN,
                    secure=settings.LANGUAGE_COOKIE_SECURE,
                    httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                    samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                )
            response.headers.setdefault("Content-Language", langue)
        return response
