from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


class Command(BaseCommand):
    help = "Ajoute des modèles pour d'autres marques mondiales pour le tenant 'dbsolution'"

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(schema_name='dbsolution')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        # Marques et modèles à insérer
        marques_modeles = {
            "Ferrari": [
                {"modele": "125 S", "variante": "Base", "portes": 0, "places": 2, "reservoir": 120},
                {"modele": "166 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "166 MM", "variante": "Barchetta", "portes": 0, "places": 2, "reservoir": 120},
                {"modele": "195 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "212 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "348 Spider", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "348 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "348 GTS", "variante": "Targa", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "365 GT", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "365 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "400", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "412", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "456", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "550 Maranello", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "550 Barchetta", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "599", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "599 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "599 GTO", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "612", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 120},
                {"modele": "812 GTS", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 110},
                {"modele": "812 Superfast", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 110},
                {"modele": "Daytona SP3", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 110},
                {"modele": "Dino 246 GT", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Dino GT4", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "F12 Berlinetta", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 110},
                {"modele": "FF", "variante": "Shooting Brake", "portes": 5, "places": 4, "reservoir": 120},
                {"modele": "GTB/GTS Turbo Trage", "variante": "Coupe/Targa", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "LaFerrari F150", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "LaFerrari Aperta Spider", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Monza SP1", "variante": "Roadster", "portes": 0, "places": 1, "reservoir": 75},
                {"modele": "Monza SP2", "variante": "Roadster", "portes": 0, "places": 2, "reservoir": 75},
                {"modele": "Portofino Cabrio", "variante": "Cabriolet", "portes": 2, "places": 2, "reservoir": 90}
            ],
        }

        created_count = 0

        # Contexte tenant
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
                        societe_id=2, # id_société =========================================
                        defaults={
                            "nombre_portes": m.get("portes", 5),
                            "nbre_places": m.get("places", 5),
                            "taille_reservoir": m.get("reservoir", 50),
                        }
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} modèles ajoutés ou enrichis pour le tenant '{tenant.schema_name}'"
        ))
