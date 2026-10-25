"""
En-têtes de sécurité ajoutés à toutes les réponses HTML :
- Content-Security-Policy : n'autorise que le site lui-même et les CDN réellement utilisés
  (jQuery, DataTables, SweetAlert2). Bloque les scripts / styles / cadres venant d'ailleurs,
  les plugins (object), la modification de <base>, l'envoi de formulaires vers un autre site
  et l'affichage du site dans un cadre externe.
  Le JavaScript et les styles écrits dans les pages (inline) restent autorisés ('unsafe-inline')
  tant qu'ils n'ont pas été déplacés dans des fichiers .js / .css.
- Permissions-Policy : caméra, micro, géolocalisation, paiement… désactivés (non utilisés).

Réglages (.env) : CSP_REPORT_ONLY=True pour seulement signaler les blocages dans la console
du navigateur sans rien bloquer.
"""
from django.conf import settings

CDN = "https://cdn.jsdelivr.net https://cdn.datatables.net https://code.jquery.com"


def _politique():
    directives = [
        "default-src 'self'",
        f"script-src 'self' 'unsafe-inline' {CDN}",
        f"style-src 'self' 'unsafe-inline' {CDN}",
        f"img-src 'self' data: blob: {CDN}",
        f"font-src 'self' data: {CDN}",
        "connect-src 'self'",
        "frame-src 'self'",
        "media-src 'self'",
        "worker-src 'self' blob:",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
    if not settings.DEBUG:
        directives.append("upgrade-insecure-requests")
    return "; ".join(directives)


PERMISSIONS = (
    "camera=(), microphone=(), geolocation=(), payment=(), usb=(), serial=(), "
    "bluetooth=(), magnetometer=(), gyroscope=(), accelerometer=(), interest-cohort=()"
)


class EnTetesSecuriteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.politique = _politique()
        self.en_tete_csp = (
            "Content-Security-Policy-Report-Only"
            if getattr(settings, "CSP_REPORT_ONLY", False) else "Content-Security-Policy"
        )

    def __call__(self, request):
        response = self.get_response(request)
        # La page d'erreur de debug (DEBUG=True) et l'admin restent utilisables
        if "Content-Security-Policy" not in response and "text/html" in response.get("Content-Type", ""):
            response.setdefault(self.en_tete_csp, self.politique)
        response.setdefault("Permissions-Policy", PERMISSIONS)
        return response
