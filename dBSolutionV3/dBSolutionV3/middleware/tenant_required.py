# dBSolutionV3/middleware/tenant_required.py

from django.contrib.auth import logout
from django.shortcuts import redirect
from django_tenants.utils import get_public_schema_name


class TenantRequiredMiddleware:
    """
    Vérifie qu'un utilisateur connecté possède une société
    et qu'il appartient au tenant actuellement demandé.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        tenant = getattr(request, "tenant", None)

        if not user or not user.is_authenticated:
            return self.get_response(request)

        # Utilisateur connecté sans société associée
        if not getattr(user, "societe_id", None):
            logout(request)
            return redirect("connexion_globale")

        # Sur le schéma public, on laisse passer la connexion globale
        if (
            tenant is None
            or tenant.schema_name == get_public_schema_name()
        ):
            return self.get_response(request)

        # L'utilisateur tente d'accéder au mauvais tenant
        if user.societe_id != tenant.pk:
            logout(request)
            return redirect("connexion_globale")

        return self.get_response(request)