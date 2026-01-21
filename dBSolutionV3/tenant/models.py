from django.db import models

# Create your models here.
# tenant/utils.py ou un script shell
from django_tenants.utils import get_tenant_model

def create_tenant():
    TenantModel = get_tenant_model()  # ✅ ici, dans une fonction
    tenant = TenantModel(
        schema_name='dbsolution',
        name='DB Solution',
        paid_until='2030-01-01',
        on_trial=False,
        auto_create_schema=True
    )
    tenant.save()

