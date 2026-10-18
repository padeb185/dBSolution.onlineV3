from django.apps import apps
from django.conf import settings
from django.shortcuts import redirect
from django.urls import Resolver404, resolve
from django_tenants.utils import get_public_schema_name


def _apps_tenant_seulement():
    partagees = set(getattr(settings, "SHARED_APPS", ()))
    return {a for a in getattr(settings, "TENANT_APPS", ()) if a not in partagees}


def _vue_app_tenant(request, path):
    """True si l'URL appartient à une app présente uniquement dans les schémas des tenants."""
    try:
        match = resolve(path, urlconf=getattr(request, "urlconf", None))
    except Resolver404:
        return False
    func = match.func
    module = getattr(getattr(func, "view_class", None), "__module__", None) or getattr(func, "__module__", "")
    config = apps.get_containing_app_config(module)
    if config is None:
        return False
    tenant_apps = _apps_tenant_seulement()
    # INSTALLED_APPS peut contenir le chemin de l'AppConfig (…apps.XxxConfig)
    return any(config.name == a or a.startswith(config.name + ".apps.") for a in tenant_apps)


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

        # Schéma public : une page d'app « tenant » (achats, maintenances…) n'y a pas de table.
        # On renvoie vers la même page dans le tenant de l'utilisateur (/tenant/<schema>/…).
        if schema_requete == get_public_schema_name():
            schema_cible = request.session.get("tenant_schema")
            if not schema_cible and request.user.is_authenticated:
                schema_cible = getattr(getattr(request.user, "societe", None), "schema_name", None)
            if (
                schema_cible
                and schema_cible != get_public_schema_name()
                and request.method in ("GET", "HEAD")
                and _vue_app_tenant(request, path)
            ):
                prefixe = getattr(settings, "TENANT_SUBFOLDER_PREFIX", "tenant").strip("/")
                cible = f"/{prefixe}/{schema_cible}{path}"
                if request.META.get("QUERY_STRING"):
                    cible += "?" + request.META["QUERY_STRING"]
                return redirect(cible)
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