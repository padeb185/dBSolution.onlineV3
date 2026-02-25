import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

from django_tenants.utils import get_tenant_model, schema_context
from django.core.management import call_command

TenantModel = get_tenant_model()

# Créer le tenant si inexistant
tenant, created = TenantModel.objects.get_or_create(
    schema_name='rsrspa',
    defaults={'paid_until': '2030-01-01', 'on_trial': False}
)

if created:
    print("✅ Tenant rsrspa créé !")
else:
    print("⚠️ Tenant rsrspa existait déjà.")

# 2️⃣ Créer le schema manuellement si auto_create_schema = False
tenant.save()  # ⚠️ Cela crée le schema vide

# 3️⃣ Appliquer les migrations dans le schema du tenant
with schema_context(tenant.schema_name):
    print("🚀 Migration des tables du tenant rsrspa...")
    call_command("migrate", interactive=False, run_syncdb=True)
    print("✅ Migrations terminées !")

