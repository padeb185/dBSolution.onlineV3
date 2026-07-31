from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


CONNEXION_GLOBALE_URL = "/fr/connexion/"


def get_connexion_globale_url(request):
    """
    Retourne l'URL globale de connexion dans la langue active,
    sans préfixe tenant.
    """

    language_code = getattr(
        request,
        "LANGUAGE_CODE",
        "fr",
    ) or "fr"

    language_code = (
        language_code
        .split("-")[0]
        .strip()
        .lower()
    )

    langues_autorisees = {
        "fr",
        "en",
        "de",
        "es",
        "it",
        "nl",
        "el",
    }

    if language_code not in langues_autorisees:
        language_code = "fr"

    return f"/{language_code}/connexion/"


class TOTPRequiredMiddleware:

    """
    Vérifie que le TOTP a été validé pendant la session
    courante pour l'utilisateur connecté.
    """

    EXCLUDED_PATH_PARTS = (
        "/connexion/",
        "/logout/",
        "/admin/",
        "/static/",
        "/media/",
        "/totp/setup/",
        "/i18n/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path_info or "/"
        user = getattr(request, "user", None)

        # ---------------------------------------------
        # Routes publiques et techniques
        # ---------------------------------------------

        if any(
            part in path
            for part in self.EXCLUDED_PATH_PARTS
        ):
            return self.get_response(request)

        # ---------------------------------------------
        # Utilisateur non authentifié
        # ---------------------------------------------

        if user is None or not user.is_authenticated:
            return self.get_response(request)

        # ---------------------------------------------
        # Aucun TOTP configuré
        # ---------------------------------------------

        totp_enabled = bool(
            getattr(
                user,
                "totp_enabled",
                False,
            )
        )

        if not totp_enabled:
            return self.get_response(request)

        # ---------------------------------------------
        # Vérification de la session TOTP
        # ---------------------------------------------

        totp_verified = (
            request.session.get("totp_verified")
            is True
        )

        totp_user_id = str(
            request.session.get("totp_user_id")
            or ""
        )

        current_user_id = str(user.pk)

        validation_correcte = (
            totp_verified
            and totp_user_id == current_user_id
        )

        if validation_correcte:
            return self.get_response(request)

        # ---------------------------------------------
        # Session TOTP invalide
        # ---------------------------------------------

        logout(request)

        messages.error(
            request,
            "Votre session TOTP doit être validée.",
        )

        return redirect(
            get_connexion_globale_url(request)
        )


class TenantUserAccessMiddleware:
    """
    Vérifie que l'utilisateur connecté accède uniquement
    au tenant associé à sa session.

    La comparaison se fait entre :

        request.tenant.schema_name

    et :

        request.session["tenant_schema"]

    Cela évite de recharger user.societe depuis le schéma
    tenant courant.
    """

    EXCLUDED_PATH_PARTS = (
        "/connexion/",
        "/logout/",
        "/admin/",
        "/static/",
        "/media/",
        "/totp/setup/",
        "/i18n/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = getattr(request, "tenant", None)
        societe = getattr(request.user, "societe", None)


        print("SCHEMA REQUEST :", getattr(tenant, "schema_name", None))
        print("SCHEMA USER :", getattr(societe, "schema_name", None))

        # votre code actuel

        if not request.user.is_authenticated:
            return self.get_response(request)

        tenant_requete = getattr(request, "tenant", None)

        # Le schéma public n'est pas soumis au contrôle tenant.
        if not tenant_requete:
            return self.get_response(request)

        if tenant_requete.schema_name == "public":
            return self.get_response(request)

        societe_utilisateur = getattr(
            request.user,
            "societe",
            None,
        )

        schema_utilisateur = getattr(
            societe_utilisateur,
            "schema_name",
            None,
        )

        schema_requete = getattr(
            tenant_requete,
            "schema_name",
            None,
        )

        if schema_utilisateur != schema_requete:
            request.session.flush()
            print(">>> REDIRECTION DEPUIS TENANT USER ACCESS")
            return redirect("/fr/connexion/")

        return self.get_response(request)