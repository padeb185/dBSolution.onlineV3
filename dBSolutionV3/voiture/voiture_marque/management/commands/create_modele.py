from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Enrichit la base de données avec les modèles pour toutes les marques pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(slug='db-solution')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return

        # Marques avec modèles représentatifs
        marques_modeles = {
            "Peugeot": [
                {"modele": "208", "variante": "Active", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "308", "variante": "GT", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "508", "variante": "Allure", "portes": 5, "places": 5, "reservoir": 55},
            ],
            "Renault": [
                {"modele": "Clio", "variante": "Zen", "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "Megane", "variante": "RS", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Talisman", "variante": "Intens", "portes": 5, "places": 5, "reservoir": 60},
            ],
            "Citroën": [
                {"modele": "C1", "variante": "Feel", "portes": 5, "places": 4, "reservoir": 35},
                {"modele": "C3", "variante": "Shine", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "C5 Aircross", "variante": "Feel", "portes": 5, "places": 5, "reservoir": 60},
            ],
            "Volkswagen": [
                {"modele": "Golf", "variante": "GTI", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Polo", "variante": "Trendline", "portes": 5, "places": 5, "reservoir": 45},
            ],
            "BMW": [
                {"modele": "Serie 1", "variante": "M Sport", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Serie 3", "variante": "Luxury", "portes": 4, "places": 5, "reservoir": 60},
            ],
            "Mercedes-Benz": [
                {"modele": "C-Class", "variante": "C200", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "E-Class", "variante": "E300", "portes": 4, "places": 5, "reservoir": 66},
            ],
            "Toyota": [
                {"modele": "Corolla", "variante": "Hybrid", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "RAV4", "variante": "Adventure", "portes": 5, "places": 5, "reservoir": 55},
            ],
            "Ford": [
                {"modele": "Focus", "variante": "ST", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Mustang", "variante": "GT", "portes": 2, "places": 4, "reservoir": 61},
            ],
            "Tesla": [
                {"modele": "Model S", "variante": "Plaid", "portes": 4, "places": 5, "reservoir": 0},  # électrique
                {"modele": "Model 3", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 0},
            ],
            "Nissan": [
                {"modele": "Leaf", "variante": "E+", "portes": 5, "places": 5, "reservoir": 0},
            ],
            "Honda": [
                {"modele": "Civic", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
            ],
            "Abarth": [
                {"modele": "500", "variante": "595", "portes": 3, "places": 2, "reservoir": 40},
                {"modele": "124 Spider", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 45},
            ],
            "Porsche": [
                {"modele": "911", "variante": "Carrera", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Cayenne", "variante": "S", "portes": 5, "places": 5, "reservoir": 75},
                {"modele": "Taycan", "variante": "Turbo", "portes": 4, "places": 4, "reservoir": 0},  # électrique
            ],
            "Audi": [
                {"modele": "A3", "variante": "Sportback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Q5", "variante": "S line", "portes": 5, "places": 5, "reservoir": 70},
            ],
            "Lamborghini": [
                {"modele": "Huracan", "variante": "EVO", "portes": 2, "places": 2, "reservoir": 60},
            ],
            "Ferrari": [
                {"modele": "F8 Tributo", "variante": None, "portes": 2, "places": 2, "reservoir": 78},
            ],
            "Jaguar": [
                {"modele": "F-Type", "variante": "R", "portes": 2, "places": 2, "reservoir": 60},
            ],
            "Land Rover": [
                {"modele": "Range Rover", "variante": "Autobiography", "portes": 5, "places": 5, "reservoir": 90},
            ],
            "Volvo": [
                {"modele": "XC90", "variante": "Inscription", "portes": 5, "places": 7, "reservoir": 71},
            ],
            "Hyundai": [
                {"modele": "i30", "variante": "N", "portes": 5, "places": 5, "reservoir": 50},
            ],
            "Kia": [
                {"modele": "Sportage", "variante": "GT Line", "portes": 5, "places": 5, "reservoir": 62},
            ],
            "Mazda": [
                {"modele": "CX-5", "variante": "Signature", "portes": 5, "places": 5, "reservoir": 56},
            ],
            "Skoda": [
                {"modele": "Octavia", "variante": "RS", "portes": 5, "places": 5, "reservoir": 55},
            ],
            "Dacia": [
                {"modele": "Duster", "variante": "Prestige", "portes": 5, "places": 5, "reservoir": 50},
            ],
        }

        created_count = 0

        with tenant_context(tenant):
            for marque_nom, modeles in marques_modeles.items():
                try:
                    marque_obj = VoitureMarque.objects.get(nom_marque=marque_nom)
                except VoitureMarque.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Marque '{marque_nom}' non trouvée."))
                    continue

                for m in modeles:
                    _, created = VoitureModele.objects.get_or_create(
                        nom_modele=m["modele"],
                        nom_variante=m.get("variante"),
                        voiture_marque=marque_obj,
                        nombre_portes=m.get("portes", 5),
                        nbre_places=m.get("places", 5),
                        taille_reservoir=m.get("reservoir", 50),
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} modèles ajoutés ou enrichis pour le tenant '{tenant.schema_name}'"
        ))
