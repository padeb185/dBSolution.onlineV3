from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe  # ton modèle de tenant
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques et variantes sportives pour le tenant 'rsrspa'"

    def handle(self, *args, **options):

        # Récupère le tenant 'rsrspa'
        try:
            tenant = Societe.objects.get(slug='rsr-nurburg')  # ou schema_name='rsrspa'
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'rsrspa' introuvable !"))
            return

        # Liste des marques/variantes sportives
        sportives = [
            # 🇫🇷 France
            "Renault RS", "Peugeot Sport", "Citroën Sport", "Alpine",

            # 🇩🇪 Allemagne
            "BMW M", "Mercedes-AMG", "Audi S", "Audi RS", "Porsche",
            "Volkswagen R",

            # 🇮🇹 Italie
            "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo",
            "Abarth",

            # 🇬🇧 Royaume-Uni
            "Jaguar R", "Aston Martin Vantage", "Lotus Exige", "McLaren",

            # 🇯🇵 Japon
            "Nissan Nismo", "Toyota GR", "Honda Type R", "Mazda Speed",
            "Subaru STI", "Mitsubishi Evo",

            # 🇰🇷 Corée du Sud
            "Hyundai N", "Kia GT", "Genesis G70 Sport",

            # 🇺🇸 États-Unis
            "Ford Mustang GT", "Chevrolet Corvette", "Dodge SRT", "Tesla Performance",

            # 🌍 Autres / électriques
            "Porsche", "Tesla", "Rimac", "Lotus"
        ]

        created_count = 0

        # Active le tenant pour insérer les données dans le schema correct
        with tenant_context(tenant):
            for marque in sportives:
                _, created = VoitureMarque.objects.get_or_create(nom_marque=marque)
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques/variantes sportives ajoutées pour le tenant '{tenant.schema_name}'"
        ))
