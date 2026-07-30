from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques automobiles mondiales depuis 1950 pour le tenant 'campus'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(schema_name='campus')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'campus' introuvable !"))
            return

        marques = [
            # 🇫🇷 France
            "Peugeot", "Renault", "Citroën", "DS Automobiles", "Alpine",
            "Bugatti", "Simca", "Talbot", "Venturi", "Ford",

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
            "Hyundai", "Kia", "Genesis", "Daewoo", "SsangYong", "Aiways","Renault RS", "Volkswagen R"

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

                       "Renault RS", "Peugeot Sport", "Citroën Sport", "Alpine", "Venturi", "Matra",
            "Ligier", "Ginetta", "Bugatti (ancien)", "Panhard Racing", "Talbot-Lago",

            # 🇩🇪 Allemagne
            "BMW M", "Mercedes-AMG", "Audi S", "Audi RS", "Porsche", "Opel OPC", "Mercedes-Benz Maybach",
            "Wiesmann", "Artega", "Porsche 918 Spyder", "BMW i8", "Alpina",

            # 🇮🇹 Italie
            "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo", "Abarth", "Pagani",
            "Lancia HF", "De Tomaso", "Mazzanti", "Dallara", "Pininfarina Battista",

            # 🇬🇧 Royaume-Uni
            "Jaguar R", "Aston Martin Vantage", "Lotus Exige", "McLaren", "Caterham",
            "Bentley Continental GT", "TVR", "Noble", "Morgan Aero", "Gordon Murray Automotive",

            # 🇯🇵 Japon
            "Nissan Nismo", "Toyota GR", "Honda Type R", "Mazda Speed", "Subaru STI",
            "Mitsubishi Evo", "Lexus F", "Acura NSX", "Toyota Supra", "Honda S2000",

            # 🇰🇷 Corée du Sud
            "Hyundai N", "Kia GT", "Genesis G70 Sport", "Kia Stinger GT", "Hyundai Veloster N",

            # 🇺🇸 États-Unis
            "Ford GT", "Chevrolet Corvette", "Chevrolet Camaro ZL1", "Dodge SRT", "Tesla Performance",
            "Cadillac V-Series", "Shelby", "Hennessey Venom", "Saleen", "SSC Tuatara",

            # 🇸🇪 Suède
            "Koenigsegg", "Volvo Polestar", "NEVS", "Scania Racing", "Svenska Supercars",

            # 🌍 Autres / électriques & hypercars
            "Rimac", "Lotus", "Bugatti", "Pagani", "Vector", "Apollo", "Czinger", "Drako GTE",
            "Porsche Taycan Turbo S", "Tesla Roadster",

            # Petites marques historiques ou courses
            "Brabham", "Lola", "Ginetta", "Ligier", "Osella", "March Engineering", "Caparo",
            "Marcos", "Spania GTA", "BAC Mono", "Radical", "Caterham 7", "Ultima Sports"
        ]

        created_count = 0

        with tenant_context(tenant):
            for marque in marques:
                # ✅ associer nom et societe dans le get_or_create
                _, created = VoitureMarque.objects.get_or_create(
                    nom_marque=marque,
                    societe=tenant  # obligatoire si societe_id est NOT NULL
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques ajoutées avec succès pour le tenant '{tenant.schema_name}'"
        ))

