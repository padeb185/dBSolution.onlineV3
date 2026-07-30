# dBSolutionV3/middleware/tenant_required.py

from django.contrib.auth import logout
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


# dBSolutionV3/middleware/tenant_required.py

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import translation
from django_tenants.utils import get_public_schema_name
from django.urls import get_script_prefix, reverse
from django.utils import translation


class TenantRequiredMiddleware:
    """
    Vérifie qu'un utilisateur connecté possède une société
    et qu'il appartient au tenant actuellement demandé.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("========== URL REVERSE DEBUG ==========")
        print("REQUEST PATH :", repr(request.path))
        print("PATH INFO :", repr(request.path_info))
        print("SCRIPT_NAME :", repr(request.META.get("SCRIPT_NAME")))
        print("SCRIPT PREFIX :", repr(get_script_prefix()))
        print("LANGUAGE :", repr(translation.get_language()))
        print(
            "DASHBOARD REVERSE :",
            repr(reverse("utilisateurs:dashboard")),
        )
        print(
            "LOGOUT REVERSE :",
            repr(reverse("utilisateurs:logout")),
        )
        # ==========================================================
        # NORMALISATION TEMPORAIRE DE LA LANGUE
        # ==========================================================
        language = (
            getattr(request, "LANGUAGE_CODE", None)
            or translation.get_language()
            or settings.LANGUAGE_CODE
        )

        language = str(language).strip("/")

        available_languages = dict(settings.LANGUAGES)

        if language not in available_languages:
            language = settings.LANGUAGE_CODE

        translation.activate(language)
        request.LANGUAGE_CODE = language

        print("========== TENANT / LANG DEBUG ==========")
        print("PATH :", repr(request.path))
        print("PATH_INFO :", repr(request.path_info))
        print("SCRIPT_NAME :", repr(request.META.get("SCRIPT_NAME")))
        print("LANGUAGE_CODE request :", repr(request.LANGUAGE_CODE))
        print("LANGUAGE active :", repr(translation.get_language()))
        print(
            "LANGUAGE cookie :",
            repr(
                request.COOKIES.get(
                    settings.LANGUAGE_COOKIE_NAME
                )
            ),
        )
        print("=========================================")

        # ==========================================================
        # CONTRÔLE DU TENANT
        # ==========================================================
        user = getattr(request, "user", None)
        tenant = getattr(request, "tenant", None)

        if not user or not user.is_authenticated:
            return self.get_response(request)

        if not getattr(user, "societe_id", None):
            logout(request)

            translation.activate(settings.LANGUAGE_CODE)

            return redirect("connexion_globale")

        if (
            tenant is None
            or tenant.schema_name == get_public_schema_name()
        ):
            return self.get_response(request)

        if user.societe_id != tenant.pk:
            logout(request)

            translation.activate(settings.LANGUAGE_CODE)

            return redirect("connexion_globale")

        return self.get_response(request)