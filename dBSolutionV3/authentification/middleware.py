from django.shortcuts import redirect

class TOTPRequiredMiddleware:
    """
    Middleware TOTP compatible i18n.
    Protège toutes les vues sauf login, login_totp, totp_setup, logout, admin, static, media.
    """

    # Exclusions
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

        # Skip si l'URL commence par un des chemins exclus
        # On gère i18n en vérifiant si path contient /fr/ devant
        for p in self.EXCLUDED_PATHS:
            if path.startswith(p) or path.startswith("/fr" + p):
                return self.get_response(request)

        # Sinon, redirige vers TOTP
        return redirect("login_totp")
