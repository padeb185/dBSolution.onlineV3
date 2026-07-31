from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


class TenantRequiredMiddleware:

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

        # Routes publiques ou techniques
        if any(
            part in path
            for part in self.EXCLUDED_PATH_PARTS
        ):
            return self.get_response(request)

        tenant = getattr(request, "tenant", None)

        schema_requete = getattr(
            tenant,
            "schema_name",
            None,
        )

        # Pas de tenant identifié
        if tenant is None:
            return self.get_response(request)

        # Le schéma public est autorisé
        if schema_requete == get_public_schema_name():
            return self.get_response(request)

        # Dans un tenant privé, utilisateur obligatoire
        if not request.user.is_authenticated:

            return redirect("/fr/connexion/")

        schema_session = request.session.get(
            "tenant_schema"
        )

        societe = getattr(
            request.user,
            "societe",
            None,
        )

        schema_utilisateur = getattr(
            societe,
            "schema_name",
            None,
        )

        acces_valide = (
            schema_requete == schema_session
            and schema_requete == schema_utilisateur
        )

        if not acces_valide:

            return redirect("/fr/connexion/")

        return self.get_response(request)