# authenfication/middleware.py
from django.shortcuts import redirect


class TOTPRequiredMiddleware:
    """
    Middleware pour obliger la vérification TOTP
    """

    EXCLUDED_PATH_PREFIXES = (
        "/login/",
        "/login/totp/",
        "/logout/",
        "/admin/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si l'utilisateur est connecté et TOTP non validé
        if (
            request.user.is_authenticated
            and not request.session.get("totp_verified", False)
            # Ignore les URLs exclues
            and not any(request.path.startswith(p) for p in self.EXCLUDED_PATH_PREFIXES)
        ):
            return redirect("login_totp")

        # Continuer le traitement
        response = self.get_response(request)
        return response
