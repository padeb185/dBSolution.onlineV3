from django.shortcuts import redirect
from django.conf import settings
from django.apps import apps



class TOTPRequiredMiddleware:
    """
    Middleware TOTP compatible i18n.
    Protège toutes les vues sauf login, login_totp, totp_setup, logout, admin, static, media.
    """

    EXCLUDED_PATHS = (
        "/login/",
        "/logout/",
        "/admin/",
        "/static/",
        "/media/",
        "/login/totp/",
        "/login/totp/setup/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Skip si utilisateur non connecté
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip si TOTP déjà vérifié
        if request.session.get("totp_verified", False):
            return self.get_response(request)

        # Skip si l'URL commence par un des chemins exclus (gère i18n)
        for p in self.EXCLUDED_PATHS:
            if path.startswith(p) or path.startswith(f"/fr{p}"):
                return self.get_response(request)

        # Redirige vers la page de TOTP seulement si l'utilisateur a TOTP activé
        if getattr(request.user, "totp_enabled", False):
            return redirect("login_totp")

        return self.get_response(request)
