# create_dbsolution_tenant.py
import os
import django

# ⚠️ nécessaire si tu exécutes en dehors du manage.py shell
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dBSolutionV3.settings")
django.setup()

from django_tenants.utils import get_tenant_model, tenant_context
from utilisateurs.models import Utilisateur

# 1️⃣ Créer le tenant
TenantModel = get_tenant_model()

# Vérifier si le tenant existe déjà
tenant, created = TenantModel.objects.get_or_create(
    schema_name='dbsolution',
    defaults={
        'scema_name': 'dbsolution',
        'paid_until': '2030-01-01',
        'on_trial': False,
        'auto_create_schema': True,
    }
)

if created:
    print("✅ Tenant dbsolution créé avec succès !")
else:
    print("⚠️ Tenant dbsolution existait déjà.")

# 2️⃣ Appliquer les migrations pour le tenant
# Avec tenant_context, Django appliquera le schéma correct
with tenant_context(tenant):
    from django.core.management import call_command

    print("🚀 Migration des tables du tenant dbsolution...")
    call_command("migrate", run_syncdb=True, interactive=False)
    print("✅ Migrations du tenant dbsolution terminées !")

    # 3️⃣ Créer un superuser tenant si nécessaire
    email_admin = "admin@dbsolution.localhost"
    if not Person.objects.filter(email=email_admin).exists():
        Person.objects.create_superuser(
            email=email_admin,
            prenom="Admin",
            last_name="Tenant",
            password="MotDePasseSuperSecure"
        )
        print(f"✅ Superuser {email_admin} créé pour le tenant dbsolution !")
    else:
        print(f"⚠️ Superuser {email_admin} existe déjà dans le tenant.")


#python manage.py shell < create_dbsolution_tenant.py






from django_tenants.utils import get_tenant_model

TenantModel = get_tenant_model()

tenant, created = TenantModel.objects.get_or_create(
    schema_name='dbsolution',
    defaults={
        'nom': 'dbsolution',
        'paid_until': '2030-01-01',
        'on_trial': False,
        'auto_create_schema': True
    }
)

print("✅ Tenant créé" if created else "⚠️ Tenant existait déjà")


