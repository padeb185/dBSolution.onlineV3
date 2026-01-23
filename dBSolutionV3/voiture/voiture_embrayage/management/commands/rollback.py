from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_embrayage.models import VoitureEmbrayage

class Command(BaseCommand):
    help = "Rollback : supprime tous les embrayages créés par create_embrayage pour le tenant dbsolution"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(slug="dbsolution")
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        with tenant_context(tenant):
            # Filtre exact : tous les embrayages sans exemplaire
            qs = VoitureEmbrayage.objects.filter(
                voiture_exemplaire__isnull=True,
                numero_embrayage=1,
                kilometrage_embrayage=0,
                voiture_modele__isnull=False
            )

            count = qs.count()
            if count == 0:
                self.stdout.write(self.style.WARNING("Aucun embrayage à supprimer."))
                return

            qs.delete()
            self.stdout.write(self.style.SUCCESS(f"✅ {count} embrayages supprimés pour le tenant '{tenant.schema_name}'"))
