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
    Vérifie qu'un utilisateur connecté appartient bien au tenant courant.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = getattr(request, "tenant", None)
        user = getattr(request, "user", None)

        # Aucun contrôle nécessaire sur les pages publiques.
        if tenant is None:
            return self.get_response(request)

        if tenant.schema_name == get_public_schema_name():
            return self.get_response(request)

        # Aucun utilisateur connecté.
        if user is None or not user.is_authenticated:
            return self.get_response(request)

        user_societe_id = getattr(user, "societe_id", None)
        tenant_id = getattr(tenant, "pk", None)

        appartient_au_tenant = (
            user_societe_id is not None
            and tenant_id is not None
            and str(user_societe_id) == str(tenant_id)
        )

        if appartient_au_tenant:
            return self.get_response(request)

        logout(request)

        messages.error(
            request,
            "Vous n'êtes pas autorisé à accéder à cette société.",
        )

        return redirect(CONNEXION_GLOBALE_URL)


class TenantRequiredMiddleware:
    """
    Vérifie qu'un tenant a été correctement résolu.

    Les pages publiques, les fichiers statiques et les fichiers média
    restent accessibles sans tenant privé.
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
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        # Les routes publiques ne doivent jamais être forcées
        # dans /tenant/<schema>/.
        if any(
            path.startswith(public_path)
            for public_path in self.PUBLIC_PATHS
        ):
            return self.get_response(request)

        tenant = getattr(request, "tenant", None)

        if tenant is None:
            raise Http404(
                "Aucun tenant trouvé pour cette URL."
            )

        return self.get_response(request)

