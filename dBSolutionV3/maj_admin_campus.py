from django.contrib.auth import get_user_model
from django_tenants.utils import get_tenant_model, schema_context

Societe = get_tenant_model()
Utilisateur = get_user_model()

EMAIL = "pierreandre.campus@gmail.com"
PASSWORD = ("")

with schema_context("public"):
    try:
        tenant = Societe.objects.get(schema_name="campus")
    except Societe.DoesNotExist:
        print("❌ Tenant 'campus' introuvable.")
        raise SystemExit

    try:
        admin = Utilisateur.objects.select_related("societe").get(
            email__iexact=EMAIL
        )
    except Utilisateur.DoesNotExist:
        print("❌ Utilisateur introuvable dans le schéma public :", EMAIL)
        raise SystemExit

    admin.nom = "Admin"
    admin.prenom = "Campus"
    admin.societe = tenant
    admin.adresse = tenant.adresse
    admin.role = "direction"

    admin.is_staff = True
    admin.is_superuser = True
    admin.is_active = True

    admin.set_password(PASSWORD)
    admin.save()

    print("===================================")
    print("Utilisateur mis à jour")
    print("Email        :", admin.email)
    print("Schéma       :", admin.societe.schema_name)
    print("Societe ID   :", admin.societe_id)
    print("Superuser    :", admin.is_superuser)
    print("Staff        :", admin.is_staff)
    print("Actif        :", admin.is_active)
    print("Mot de passe :", admin.check_password(PASSWORD))
    print("===================================")