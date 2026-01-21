


from django_tenants.utils import get_tenant_model, tenant_context
Tenant = get_tenant_model()
tenant = Tenant.objects.get(schema_name='dbsolution')

with tenant_context(tenant):
    from utilisateurs.models import Utilisateur
    print(Utilisateur.objects.all())










from societe.models import Societe  # ou le modèle que tu utilises comme tenant
from django_tenants.utils import get_tenant_model

TenantModel = get_tenant_model()

# Créer le tenant s'il n'existe pas
tenant, created = TenantModel.objects.get_or_create(
    schema_name='dbsolution',
    defaults={
        'nom': 'DB Solution',
        'paid_until': '2030-01-01',
        'on_trial': False,
        'auto_create_schema': True,
    }
)

if created:
    print("✅ Tenant dbsolution créé !")
else:
    print("⚠️ Tenant dbsolution existait déjà.")













from django_tenants.utils import get_tenant_model

TenantModel = get_tenant_model()

# Vérifier si le tenant existe déjà
try:
    tenant = TenantModel.objects.get(schema_name='dbsolution')
    print("⚠️ Tenant dbsolution existait déjà.")
except TenantModel.DoesNotExist:
    tenant = TenantModel(
        schema_name='dbsolution',  # nom du schéma
        name='DB Solution',
        paid_until='2030-01-01',
        on_trial=False,
        auto_create_schema=True  # ✅ ok ici, pas dans get_or_create
    )
    tenant.save()
    print("✅ Tenant dbsolution créé avec succès !")





from django_tenants.utils import get_tenant_model, tenant_context
from django.core.management import call_command
from utilisateurs.models import Utilisateur  # ton modèle user custom
from adresse.models import Adresse  # si nécessaire

TenantModel = get_tenant_model()  # => Societe

# 1️⃣ Créer le tenant s'il n'existe pas
try:
    tenant = TenantModel.objects.get(schema_name='rsrspa')
    print("⚠️ Tenant rsrspa existait déjà.")
except TenantModel.DoesNotExist:
    # Ici on crée le tenant en utilisant les bons champs
    tenant = TenantModel(
        schema_name='rsrspa',
        nom='rsrspa',
        paid_until='2030-01-01',
        on_trial=False,
        directeur='Fred',  # exemple
        numero_tva='BE0000000000',
        # adresse peut rester None si tu n'as pas encore d'adresse
    )
    tenant.save()  # ✅ crée le schéma automatiquement
    print("✅ Tenant rsrspa créé avec succès !")






# 2️⃣ Appliquer les migrations pour ce tenant
with tenant_context(tenant):
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
