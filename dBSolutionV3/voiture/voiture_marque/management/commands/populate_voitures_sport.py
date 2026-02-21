from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe  # ton modèle de tenant
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques et variantes sportives pour le tenant 'dbsolution'"

    def handle(self, *args, **options):

        # Récupère le tenant 'dbsolution'
        try:
            tenant = Societe.objects.get(schema_name='dbsolution')  # ou schema_name='dbsolutions'
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        # Liste des marques/variantes sportives
        sportives = [
            # 🇫🇷 France
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

        # Active le tenant pour insérer les données dans le schema correct
        with tenant_context(tenant):
            for marque in sportives:
                _, created = VoitureMarque.objects.get_or_create(nom_marque=marque)
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques/variantes sportives ajoutées pour le tenant '{tenant.schema_name}'"
        ))
