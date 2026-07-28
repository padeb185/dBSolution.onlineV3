
from datetime import date
from django_tenants.utils import get_tenant_model, tenant_context
from django.contrib.auth import get_user_model

Societe = get_tenant_model()
Utilisateur = get_user_model()

tenant = Societe.objects.get(schema_name="campus")

with tenant_context(tenant):
    admin = Utilisateur.objects.create_superuser(
        email="pierreandre.campus@gmail.com",
        password="",
        nom="Admin",
        prenom="Campus",
        date_naissance=date(1984, 5, 18),
        societe=tenant,
        adresse=tenant.adresse,
        role="direction",
    )

print("Administrateur créé :", admin.email)



from django_tenants.utils import get_tenant_model, tenant_context
from django.contrib.auth import get_user_model

Societe = get_tenant_model()
Utilisateur = get_user_model()

tenant = Societe.objects.get(schema_name="campus")

with tenant_context(tenant):
    admin = Utilisateur.objects.get(
        email="pierreandre.campus@gmail.com"
    )

    admin.nom = "Admin"
    admin.prenom = "Campus"
    admin.societe = tenant
    admin.adresse = tenant.adresse
    admin.role = "direction"

    admin.is_staff = True
    admin.is_superuser = True
    admin.is_active = True

    admin.set_password("vzj@7Obpcx75ISWWJsNo28E")
    admin.save()

    print(
        "Administrateur mis à jour :",
        admin.email,
        admin.societe.schema_name,
        admin.is_superuser,
    )