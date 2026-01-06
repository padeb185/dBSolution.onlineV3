from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Ajoute des modèles pour d'autres marques mondiales pour le tenant 'db-solution'"

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(slug='db-solution')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'db-solution' introuvable !"))
            return

        # Marques restantes avec quelques modèles représentatifs
        marques_modeles = {
            # Italie
            "Fiat": [
                {"modele": "500", "variante": "Pop", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "Panda", "variante": "City", "portes": 5, "places": 5, "reservoir": 40},
            ],
            "Alfa Romeo": [
                {"modele": "Giulia", "variante": "Veloce", "portes": 4, "places": 5, "reservoir": 48},
                {"modele": "Stelvio", "variante": "Quadrifoglio", "portes": 5, "places": 5, "reservoir": 60},
            ],
            "Lancia": [
                {"modele": "Ypsilon", "variante": "Gold", "portes": 5, "places": 5, "reservoir": 40},
            ],
            "Maserati": [
                {"modele": "Ghibli", "variante": None, "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Levante", "variante": None, "portes": 5, "places": 5, "reservoir": 80},
            ],
            "Pagani": [
                {"modele": "Huayra", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            ],
            "De Tomaso": [
                {"modele": "Pantera", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
            ],

            # UK
            "Mini": [
                {"modele": "Cooper", "variante": "S", "portes": 3, "places": 4, "reservoir": 40},
            ],
            "Rolls-Royce": [
                {"modele": "Ghost", "variante": None, "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "Cullinan", "variante": None, "portes": 5, "places": 5, "reservoir": 105},
            ],
            "Bentley": [
                {"modele": "Continental GT", "variante": None, "portes": 2, "places": 4, "reservoir": 90},
            ],
            "Aston Martin": [
                {"modele": "DB11", "variante": None, "portes": 2, "places": 4, "reservoir": 78},
            ],
            "Lotus": [
                {"modele": "Evora", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
            ],

            # Espagne
            "SEAT": [
                {"modele": "Ibiza", "variante": "FR", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "Leon", "variante": "FR", "portes": 5, "places": 5, "reservoir": 55},
            ],
            "Cupra": [
                {"modele": "Formentor", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            ],
            "Hispano-Suiza": [
                {"modele": "Carmen", "variante": None, "portes": 2, "places": 2, "reservoir": 0},
            ],

            # Suède
            "Saab": [
                {"modele": "9-3", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
            ],
            "Koenigsegg": [
                {"modele": "Jesko", "variante": None, "portes": 2, "places": 2, "reservoir": 100},
            ],

            # Corée
            "Hyundai": [
                {"modele": "i20", "variante": "N", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "Tucson", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            ],
            "Kia": [
                {"modele": "Sorento", "variante": "GT Line", "portes": 5, "places": 7, "reservoir": 70},
            ],
            "Genesis": [
                {"modele": "G70", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
            ],

            # Chine
            "Geely": [
                {"modele": "Atlas", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            ],
            "NIO": [
                {"modele": "ES8", "variante": None, "portes": 5, "places": 7, "reservoir": 0},
            ],

            # Inde
            "Tata": [
                {"modele": "Nexon", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
            ],
            "Mahindra": [
                {"modele": "XUV700", "variante": None, "portes": 5, "places": 7, "reservoir": 60},
            ],

            # Brésil
            "Gurgel": [
                {"modele": "BR-800", "variante": None, "portes": 2, "places": 4, "reservoir": 35},
            ],

            # Australie
            "Holden": [
                {"modele": "Commodore", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
            ],

            # Russie / URSS
            "Lada": [
                {"modele": "Niva", "variante": None, "portes": 3, "places": 4, "reservoir": 42},
            ],
            "GAZ": [
                {"modele": "Volga", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
            ],
            "UAZ": [
                {"modele": "Hunter", "variante": None, "portes": 3, "places": 5, "reservoir": 70},
            ],

            # Iran
            "Iran Khodro": [
                {"modele": "Dena", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
            ],
            "SAIPA": [
                {"modele": "Tiba", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
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
