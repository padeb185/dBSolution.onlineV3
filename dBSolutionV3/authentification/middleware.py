from django.shortcuts import redirect


class TOTPRequiredMiddleware:


    EXCLUDED_PATHS = (
        "/login/totp/",
        "/logout/",
        "/admin/login/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
                request.user.is_authenticated
                and not request.session.get("totp_verified", False)
                and not request.path.startswith(self.EXCLUDED_PATHS)
        ):
            return redirect("login_totp")

        return self.get_response(request)

