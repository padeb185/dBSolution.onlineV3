"""
Reprend le véhicule et le kilométrage des fiches main-d'œuvre existantes depuis leur intervention.

django-tenants :
    python manage.py all_tenants_command sync_main_oeuvre
    python manage.py tenant_command sync_main_oeuvre --schema=<schema>
"""
from django.core.management.base import BaseCommand

from maindoeuvre.liaison import synchroniser
from maindoeuvre.models import MainDoeuvre


class Command(BaseCommand):
    help = "Reprend véhicule et kilométrage des fiches main-d'œuvre depuis l'intervention liée."

    def handle(self, *args, **options):
        from django.db import connection

        # Schéma public : pas de tables tenant (main-d'œuvre, interventions) → on passe
        schema = getattr(connection, "schema_name", None)
        try:
            from django_tenants.utils import get_public_schema_name
            public = get_public_schema_name()
        except Exception:
            public = "public"
        if schema == public:
            self.stdout.write(f"Schéma « {schema} » ignoré (pas de main-d'œuvre).")
            return

        total = liees = 0
        for mo in list(MainDoeuvre.objects.all()):
            total += 1
            if synchroniser(mo) is not None:
                liees += 1
        self.stdout.write(self.style.SUCCESS(f"{liees}/{total} fiches main-d'œuvre synchronisées."))
