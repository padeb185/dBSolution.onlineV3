from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_embrayage.models import (
    VoitureEmbrayage,
    TypeEmbrayage,
    TypeVolantMoteur,
    TypePlateauPression,
)
from voiture.voiture_modele.models import VoitureModele

class Command(BaseCommand):
    help = "Crée tous les embrayages génériques pour la marque Mini"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(slug="dbsolution")
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        with tenant_context(tenant):
            # 1️⃣ Récupère un modèle Mini existant pour récupérer la marque
            mini_modele = VoitureModele.objects.filter(voiture_marque__nom_marque="Mini").first()
            if not mini_modele:
                self.stdout.write(self.style.ERROR("Aucun modèle Mini trouvé !"))
                return

            # 2️⃣ Crée un modèle "Générique" lié à la même marque que Mini
            modele_generic, _ = VoitureModele.objects.get_or_create(
                nom_modele="Générique",
                voiture_marque=mini_modele.voiture_marque,
                defaults={
                    "nbre_places": 0,
                    "nombre_portes": 0,
                    "taille_reservoir": 0,
                }
            )

            created_count = 0

            # 3️⃣ Crée tous les embrayages génériques
            for type_embrayage in TypeEmbrayage.values:
                for volant_moteur in TypeVolantMoteur.values:
                    for plateau_pression in TypePlateauPression.values:
                        embrayage, created = VoitureEmbrayage.objects.get_or_create(
                            voiture_modele=modele_generic,
                            voiture_exemplaire=None,
                            fabricant="Générique",
                            numero_embrayage=1,
                            defaults={
                                "type_embrayage": type_embrayage,
                                "volant_moteur": volant_moteur,
                                "plateau_pression": plateau_pression,
                                "kilometrage_embrayage": 0,
                                "oem": None,
                            }
                        )
                        if created:
                            created_count += 1

            self.stdout.write(self.style.SUCCESS(
                f"✅ {created_count} embrayages génériques créés pour Mini (tenant '{tenant.schema_name}')"
            ))
