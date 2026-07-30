from django.contrib import messages
from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


CONNEXION_GLOBALE_URL = "/fr/connexion/"


class TOTPRequiredMiddleware:
    """
    Vérifie que le TOTP a été validé pendant la session courante.

    Ce middleware intervient uniquement pour les utilisateurs déjà
    authentifiés et dont le TOTP est activé.
    """

    EXCLUDED_PATH_PARTS = (
        "/connexion/",
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

        # Les routes publiques et techniques restent toujours accessibles.
        if any(
            part in path
            for part in self.EXCLUDED_PATH_PARTS
        ):
            return self.get_response(request)

        # Le middleware d'authentification n'a pas encore fourni
        # d'utilisateur exploitable.
        if user is None or not user.is_authenticated:
            return self.get_response(request)

        # Aucun contrôle TOTP n'est requis si le TOTP n'est pas activé.
        if not getattr(user, "totp_enabled", False):
            return self.get_response(request)

        totp_verified = (
            request.session.get("totp_verified") is True
        )

        totp_user_id = request.session.get("totp_user_id")

        validation_correcte = (
            totp_verified
            and totp_user_id == str(user.pk)
        )

        if validation_correcte:
            return self.get_response(request)

        # La session Django existe, mais le TOTP n'a pas été validé
        # pour cet utilisateur.
        logout(request)

        messages.error(
            request,
            "Votre session TOTP doit être validée.",
        )

        # Redirection absolue afin d'éviter que Django ajoute
        # automatiquement le préfixe du tenant.
        return redirect(CONNEXION_GLOBALE_URL)



class TenantUserAccessMiddleware:
    """
    Vérifie que l'utilisateur connecté appartient bien
    au tenant demandé dans l'URL.

    La comparaison se fait avec schema_name.
    """

    PUBLIC_PATHS = (
        "/fr/connexion/",
        "/en/connexion/",
        "/de/connexion/",
        "/es/connexion/",
        "/it/connexion/",
        "/nl/connexion/",
        "/el/connexion/",
        "/i18n/",
        "/static/",
        "/media/",
        "/admin/",
        "/totp/setup/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Ne pas contrôler les routes publiques.
        if any(
            path.startswith(public_path)
            for public_path in self.PUBLIC_PATHS
        ):
            return self.get_response(request)

        tenant = getattr(request, "tenant", None)
        user = getattr(request, "user", None)

        # Aucun tenant résolu.
        if tenant is None:
            return self.get_response(request)

        # Aucun contrôle sur le schéma public.
        if tenant.schema_name == get_public_schema_name():
            return self.get_response(request)

        # Aucun utilisateur connecté.
        if user is None or not user.is_authenticated:
            return self.get_response(request)

        user_societe = getattr(user, "societe", None)

        if user_societe is None:
            logout(request)

            messages.error(
                request,
                "Aucune société n'est associée à votre compte.",
            )

            return redirect("/fr/connexion/")

        user_schema_name = getattr(
            user_societe,
            "schema_name",
            None,
        )

        tenant_schema_name = getattr(
            tenant,
            "schema_name",
            None,
        )

        if user_schema_name != tenant_schema_name:
            logout(request)

            messages.error(
                request,
                "Vous n'êtes pas autorisé à accéder à cette société.",
            )

            return redirect("/fr/connexion/")

        return self.get_response(request)

