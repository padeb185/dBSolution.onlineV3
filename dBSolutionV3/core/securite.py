"""
Outils de sécurité communs.

url_sure(url) : n'accepte qu'une URL interne au site (chemin relatif « /… » ou URL absolue
vers un hôte autorisé en http/https). Bloque les redirections ouvertes (« //site-externe »,
« https://site-externe ») et les liens « javascript: ». Retourne "" si l'URL n'est pas sûre.
"""
from urllib.parse import urlsplit

from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme


def _hotes_autorises(request=None):
    hotes = {h.lstrip(".") for h in getattr(settings, "ALLOWED_HOSTS", []) if h and h != "*"}
    if request is not None:
        try:
            hotes.add(request.get_host())
        except Exception:
            pass
    return hotes


def url_sure(url, request=None):
    url = (str(url or "")).strip()
    if not url:
        return ""
    if url.startswith("/") and not url.startswith("//") and not url.startswith("/\\"):
        return url
    secure = bool(request and request.is_secure())
    if url_has_allowed_host_and_scheme(url, allowed_hosts=_hotes_autorises(request), require_https=secure):
        morceaux = urlsplit(url)
        if morceaux.scheme in ("http", "https"):
            # On ne garde que le chemin : le lien reste sur le site courant
            chemin = morceaux.path or "/"
            return chemin + (f"?{morceaux.query}" if morceaux.query else "")
    return ""
