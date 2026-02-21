from django.core.management.base import BaseCommand
from django.db.models import Count, ForeignKey, OneToOneField
from django.apps import apps
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Supprime les doublons de VoitureModele en réassignant automatiquement toutes les FK"

    def handle(self, *args, **options):

        related_fields = []

        # 🔍 uniquement les vraies FK/O2O
        for model in apps.get_models():
            for field in model._meta.get_fields():
                if isinstance(field, (ForeignKey, OneToOneField)) and field.related_model == VoitureModele:
                    related_fields.append((model, field.name))

        self.stdout.write(self.style.WARNING(f"{len(related_fields)} FK trouvées"))

        for tenant in Societe.objects.exclude(schema_name="public"):
            self.stdout.write(self.style.WARNING(f"Tenant: {tenant.schema_name}"))

            with tenant_context(tenant):

                doublons = (
                    VoitureModele.objects
                    .values("nom_modele", "nom_variante", "voiture_marque", "societe")
                    .annotate(nb=Count("id"))
                    .filter(nb__gt=1)
                )

                total_deleted = 0

                for d in doublons:
                    qs = VoitureModele.objects.filter(
                        nom_modele=d["nom_modele"],
                        nom_variante=d["nom_variante"],
                        voiture_marque=d["voiture_marque"],
                        societe=d["societe"],
                    ).order_by("id")

                    keep = qs.first()
                    duplicates = qs.exclude(id=keep.id)

                    for dup in duplicates:

                        for model, field_name in related_fields:
                            model.objects.filter(**{field_name: dup}).update(**{field_name: keep})

                        dup.delete()
                        total_deleted += 1

                self.stdout.write(
                    self.style.SUCCESS(f"Doublons supprimés: {total_deleted}")
                )