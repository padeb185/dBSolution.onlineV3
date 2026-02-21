from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe  # <--- ton modèle de tenant
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques automobiles mondiales depuis 1950 pour le tenant 'rsrnurburg'"

    def handle(self, *args, **options):

        # Récupère le tenant 'rsrnurburg'
        try:
            tenant = Societe.objects.get(slug='rsr-nurburg')  # ou schema_name='rsrspa'
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'rsrnurburg' introuvable !"))
            return

        marques = [
            "Peugeot", "Renault", "Citroën", "DS Automobiles", "Alpine",
            "Bugatti",

            # 🇩🇪 Allemagne
            "Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Porsche",
            "Opel", "Maybach",

            # 🇮🇹 Italie
            "Fiat", "Alfa Romeo", "Lancia", "Ferrari", "Lamborghini",
            "Maserati", "Pagani", "Abarth", "De Tomaso",

            # 🇬🇧 Royaume-Uni
            "Jaguar", "Mini", "Bentley", "Aston Martin", "Lotus", "TVR",

            # 🇪🇸 Espagne
            "SEAT", "Cupra",

            # 🇸🇪 Suède
            "Volvo", "Koenigsegg", "Polestar",

            # 🇯🇵 Japon
            "Toyota", "Nissan", "Honda", "Acura",
            "Mazda", "Subaru", "Mitsubishi", "Suzuki",

            # 🇰🇷 Corée du Sud
            "Hyundai", "Hyundai N", "Kia GT",

            # 🇺🇸 États-Unis
            "Ford", "Ford GT", "Chevrolet", "Cadillac", "Jeep", "Dodge", "Dodge SRT", "Tesla Performance",

            # Versions sportives / spéciales
            "Renault RS", "BMW M", "Abarth",
            "Jaguar R", "Aston Martin Vantage", "Lotus Exige", "McLaren",
            "Nissan Nismo", "Toyota GR", "Honda Type R", "Mazda Speed",
            "Subaru STI", "Mitsubishi Evo",  "Peugeot Sport", "Audi S", "Citroën Sport",
            "Mercedes-AMG", "Rolls-Royce", "Audi RS", "Radical", "Skoda",
            "Volkswagen R"
        ]

        created_count = 0

        # Active le tenant pour créer les marques dans le schema correct
        with tenant_context(tenant):
            for marque in marques:
                _, created = VoitureMarque.objects.get_or_create(nom_marque=marque)
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques ajoutées avec succès pour le tenant '{tenant.schema_name}'"
        ))
