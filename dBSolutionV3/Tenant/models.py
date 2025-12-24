from django.utils import timezone
from tenants.models import Client  # Remplace par ton modèle de tenant si différent

# Vérifie si le tenant existe déjà
tenant_name = 'dbsolution.localhost'
if not Client.objects.filter(schema_name='dbsolution').exists():
    # Créer le tenant
    tenant = Client(
        schema_name='dbsolution',  # nom du schema PostgreSQL
        name='dBSolution',          # nom affiché du tenant
        paid_until=timezone.now() + timezone.timedelta(days=365),  # exemple d'expiration
        on_trial=True
    )
    tenant.save()

    # Créer le domaine associé
    tenant.domains.create(domain=tenant_name)

    print(f"Tenant '{tenant_name}' créé avec succès !")
else:
    print(f"Tenant '{tenant_name}' existe déjà.")
