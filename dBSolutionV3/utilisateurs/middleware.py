from django.shortcuts import redirect
from django.urls import reverse

class TOTPRequiredMiddleware:
    """
    Middleware TOTP compatible i18n.
    Ne redirige PAS vers login_totp (supprimé).
    """

    EXCLUDED_PATHS = (
        "/login/",
        "/logout/",
        "/admin/",
        "/static/",
        "/media/",
        "/totp/setup/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        user = getattr(request, "user", None)

        # Non connecté → OK
        if not user or not user.is_authenticated:
            return self.get_response(request)

        # TOTP déjà validé → OK
        if request.session.get("totp_verified", False):
            return self.get_response(request)

        # URLs autorisées (i18n)
        for p in self.EXCLUDED_PATHS:
            if path.startswith(p) or path.startswith(f"/fr{p}"):
                return self.get_response(request)

        # 🔐 Si TOTP requis → retour login
        if getattr(user, "totp_enabled", False):
            return redirect("utilisateurs:login")

        return self.get_response(request)
