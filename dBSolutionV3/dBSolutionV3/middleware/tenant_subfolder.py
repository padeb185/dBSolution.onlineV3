"""
Résolution du tenant par sous-dossier (/tenant/<schéma>/…), tolérante à un domaine manquant.

django-tenants cherche le tenant via la table des domaines (Domain.domain == <schéma>).
Si ce domaine n'existe pas (tenant créé par un ancien script, création interrompue après le schéma…),
toute page du tenant renvoie une 404, y compris la configuration du TOTP à la première connexion.
Ici, le tenant est alors retrouvé par son nom de schéma et le domaine manquant est créé.
"""
import logging

from django.db import IntegrityError
from django_tenants.middleware import TenantSubfolderMiddleware
from django_tenants.utils import get_public_schema_name, get_tenant_model

logger = logging.getLogger(__name__)


class TenantSubfolderTolerantMiddleware(TenantSubfolderMiddleware):

    def get_tenant(self, domain_model, hostname):
        try:
            return super().get_tenant(domain_model, hostname)
        except domain_model.DoesNotExist:
            schema = (hostname or "").strip().lower()
            if not schema or schema == get_public_schema_name():
                raise
            try:
                tenant = get_tenant_model().objects.get(schema_name=schema)
            except get_tenant_model().DoesNotExist:
                raise domain_model.DoesNotExist(f"Aucun tenant pour le sous-dossier « {hostname} »")
            try:
                domain_model.objects.get_or_create(
                    domain=schema, defaults={"tenant": tenant,
                                             "is_primary": not domain_model.objects.filter(tenant=tenant).exists()})
                logger.warning("Domaine manquant créé pour le tenant %s", schema)
            except IntegrityError:
                logger.exception("Impossible de créer le domaine du tenant %s", schema)
            return tenant
