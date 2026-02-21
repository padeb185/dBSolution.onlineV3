from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe  # <--- ton modèle de tenant
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques automobiles mondiales depuis 1950 pour le tenant 'dbsolution'"

    def handle(self, *args, **options):

        # Récupère le tenant 'dbsolution'
        try:
            tenant = Societe.objects.get(schema_name='dbsolution')  # ou schema_name='dbsolution'
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        marques = [
            # 🇫🇷 France
            "Peugeot", "Renault", "Citroën", "DS Automobiles", "Alpine",
            "Bugatti", "Simca", "Talbot", "Venturi",

            # 🇩🇪 Allemagne
            "Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Porsche",
            "Opel", "Maybach", "Smart", "Borgward", "Wartburg",

            # 🇮🇹 Italie
            "Fiat", "Alfa Romeo", "Lancia", "Ferrari", "Lamborghini",
            "Maserati", "Pagani", "Abarth", "De Tomaso", "Innocenti",

            # 🇬🇧 Royaume-Uni
            "Jaguar", "Land Rover", "Range Rover", "Mini", "Rolls-Royce",
            "Bentley", "Aston Martin", "Lotus", "MG", "Rover",
            "Morgan", "TVR", "Triumph",

            # 🇪🇸 Espagne
            "SEAT", "Cupra", "Hispano-Suiza",

            # 🇸🇪 Suède
            "Volvo", "Saab", "Koenigsegg", "Polestar",

            # 🇯🇵 Japon
            "Toyota", "Lexus", "Nissan", "Infiniti", "Honda", "Acura",
            "Mazda", "Subaru", "Mitsubishi", "Suzuki", "Isuzu", "Daihatsu",

            # 🇰🇷 Corée du Sud
            "Hyundai", "Kia", "Genesis", "Daewoo", "SsangYong",

            # 🇺🇸 États-Unis
            "Ford", "Chevrolet", "Cadillac", "Buick", "GMC", "Chrysler",
            "Dodge", "Jeep", "Tesla", "Lincoln", "Pontiac",
            "Oldsmobile", "Mercury", "Hummer", "Ram",

            # 🇨🇳 Chine
            "Geely", "BYD", "Chery", "Great Wall", "Haval", "NIO",
            "XPeng", "Li Auto", "Wuling", "SAIC", "Hongqi",

            # 🇷🇺 URSS / Russie
            "Lada", "GAZ", "UAZ", "Moskvitch", "ZIL",

            # 🇮🇳 Inde
            "Tata", "Mahindra", "Hindustan Motors",

            # 🇨🇿 Tchéquie
            "Skoda", "Tatra",

            # 🇷🇴 Roumanie
            "Dacia",

            "Radical",
            # 🇮🇷 Iran
            "Iran Khodro", "SAIPA",

            # 🇧🇷 Brésil
            "Gurgel",

            # 🇦🇺 Australie
            "Holden",

            # 🌍 Marques mondiales / électriques
            "Rivian", "Lucid", "Fisker", "Polestar",
            "VinFast", "Aiways"
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
