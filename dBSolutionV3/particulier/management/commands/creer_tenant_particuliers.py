"""
Crée le tenant partagé des particuliers (schéma settings.PARTICULIERS_SCHEMA) :
    python manage.py creer_tenant_particuliers
La création du schéma applique toutes les migrations des apps tenant (quelques minutes).
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django_tenants.utils import get_public_schema_name, schema_context


class Command(BaseCommand):
    help = "Crée le tenant partagé des particuliers (application Flutter)."

    def handle(self, *args, **options):
        from societe.models import Domain, Societe
        schema = getattr(settings, "PARTICULIERS_SCHEMA", "particuliers")
        with schema_context(get_public_schema_name()):
            societe = Societe.objects.filter(schema_name=schema).first()
            if societe:
                self.stdout.write(self.style.WARNING(f"Le tenant « {schema} » existe déjà."))
            else:
                self.stdout.write(f"Création du schéma « {schema} » et migrations…")
                societe = Societe(
                    schema_name=schema, slug=schema, nom="CarsCosts – Particuliers", directeur="CarsCosts",
                    numero_tva="PARTICULIERS", max_utilisateurs=1_000_000, on_trial=False,
                    # Aucun module professionnel : les particuliers n'ont accès qu'à l'API
                    modules=[],
                )
                societe.save()
                self.stdout.write(self.style.SUCCESS(f"Tenant « {schema} » créé."))
            Domain.objects.get_or_create(domain=schema, defaults={"tenant": societe, "is_primary": True})
