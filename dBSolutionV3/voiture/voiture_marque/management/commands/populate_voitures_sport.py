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
            "Ligier", "Ginetta", "Panhard Racing", "Talbot-Lago",

            # 🇩🇪 Allemagne
            "BMW M", "Mercedes-AMG", "Audi S", "Audi RS", "Porsche", "Opel OPC",
            "Wiesmann", "Artega", "BMW i8", "Alpina",

            # 🇮🇹 Italie
            "Ferrari", "Lamborghini", "Maserati", "Alfa Romeo", "Abarth", "Pagani",
            "Lancia HF", "De Tomaso", "Mazzanti", "Dallara", "Pininfarina Battista",

            # 🇬🇧 Royaume-Uni
            "Jaguar R", "Aston Martin Vantage", "Lotus Exige", "McLaren", "Caterham",
            "Bentley", "TVR", "Noble", "Morgan Aero", "Gordon Murray Automotive",

            # 🇯🇵 Japon
            "Nissan Nismo", "Toyota GR", "Honda Type R", "Mazda Speed", "Subaru STI",
            "Mitsubishi Evo", "Lexus F", "Acura", "Honda S2000",

            # 🇰🇷 Corée du Sud
            "Hyundai N", "Kia GT", "Genesis G70 Sport",

            # 🇺🇸 États-Unis
            "Ford", "Chevrolet Corvette", "Chevrolet Camaro ZL1", "Dodge SRT", "Tesla",
            "Cadillac V-Series", "Shelby", "Hennessey", "Saleen", "SSC Tuatara",

            # 🇸🇪 Suède
            "Koenigsegg", "Polestar", "NEVS", "Scania Racing", "Svenska Supercars",

            # 🌍 Autres / électriques & hypercars
            "Rimac", "Lotus", "Bugatti", "Pagani", "Vector", "Apollo", "Czinger", "Drako",

            # Petites marques historiques ou courses
            "Brabham", "Lola", "Ginetta", "Ligier", "Osella", "March Engineering", "Caparo",
            "Marcos", "Spania GTA", "BAC Mono", "Radical", "Caterham 7", "Ultima Sports"
        ]

        created_count = 0

        with tenant_context(tenant):
            for marque in sportives:
                # ✅ on précise le tenant pour le champ NOT NULL
                _, created = VoitureMarque.objects.get_or_create(
                    nom_marque=marque,
                    societe=tenant
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques/variantes sportives ajoutées pour le tenant '{tenant.schema_name}'"
        ))