"""
Socle de l'API particuliers : jeton (DRF TokenAuthentication), schéma du tenant partagé
« particuliers », permission « particulier » et filtrage par propriétaire.
"""
from django.conf import settings
from django.http import FileResponse, Http404
from django_tenants.utils import schema_context
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

ROLE_PARTICULIER = "particulier"


def schema_particuliers():
    return getattr(settings, "PARTICULIERS_SCHEMA", "particuliers")


def est_particulier(user):
    return bool(user and user.is_authenticated and getattr(user, "role", None) == ROLE_PARTICULIER
                and getattr(getattr(user, "societe", None), "schema_name", None) == schema_particuliers())


class EstParticulier(permissions.BasePermission):
    message = "Compte particulier requis."

    def has_permission(self, request, view):
        return est_particulier(request.user)


class LimiteConnexion(AnonRateThrottle):
    rate = "20/min"


class LimiteUtilisateur(UserRateThrottle):
    rate = "600/min"


class SchemaParticuliersMixin:
    """Toute la requête s'exécute dans le schéma du tenant des particuliers."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [EstParticulier]
    throttle_classes = [LimiteUtilisateur]

    def dispatch(self, request, *args, **kwargs):
        with schema_context(schema_particuliers()):
            return super().dispatch(request, *args, **kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        noter_activite(request.user)


def noter_activite(user):
    """Dernière utilisation de l'application (last_login), au plus une écriture toutes les 10 minutes."""
    from datetime import timedelta
    from django.utils import timezone
    if not getattr(user, "is_authenticated", False):
        return
    maintenant = timezone.now()
    if user.last_login is None or maintenant - user.last_login > timedelta(minutes=10):
        type(user).objects.filter(pk=user.pk).update(last_login=maintenant)
        user.last_login = maintenant


def servir_fichier(champ):
    """Fichier privé (ticket, document) : uniquement via l'API, après contrôle du propriétaire."""
    if not champ:
        raise Http404
    try:
        return FileResponse(champ.open("rb"), filename=champ.name.rsplit("/", 1)[-1])
    except FileNotFoundError:
        raise Http404
