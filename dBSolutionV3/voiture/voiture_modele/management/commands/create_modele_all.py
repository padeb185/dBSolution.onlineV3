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


        # Marques et modèles à ajouter
        marques_modeles = {

            "Volkswagen": [
                # Golf GTI par générations
                {"modele": "Golf GTI Mk1", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 50},
                {"modele": "Golf GTI Mk2", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf GTI Mk3", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf GTI Mk4", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf GTI Mk5", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf GTI Mk6", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf GTI Mk7", "variante": "GTI", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Golf GTI Mk8", "variante": "GTI", "portes": 5, "places": 5, "reservoir": 50},

                # Golf GTI spéciales
                {"modele": "Golf GTI Clubsport", "variante": "Clubsport", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Golf GTI Clubsport S", "variante": "Clubsport", "portes": 3, "places": 2, "reservoir": 50},
                {"modele": "Golf GTI TCR", "variante": "TCR", "portes": 5, "places": 5, "reservoir": 50},

                # Golf R
                {"modele": "Golf R32 Mk4", "variante": "R32", "portes": 3, "places": 5, "reservoir": 62},
                {"modele": "Golf R32 Mk5", "variante": "R32", "portes": 3, "places": 5, "reservoir": 62},
                {"modele": "Golf R Mk6", "variante": "R", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Golf R Mk7", "variante": "R", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Golf R Mk8", "variante": "R", "portes": 5, "places": 5, "reservoir": 55},

                # Golf G60 / VR6
                {"modele": "Golf G60", "variante": "G60", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf VR6 Mk3", "variante": "VR6", "portes": 3, "places": 5, "reservoir": 55},

                # Polo sport
                {"modele": "Polo GTI Mk3", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo GTI Mk4", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo GTI Mk5", "variante": "GTI", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo GTI Mk6", "variante": "GTI", "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "Polo R WRC", "variante": "R", "portes": 3, "places": 4, "reservoir": 45},

                # Scirocco sport
                {"modele": "Scirocco R", "variante": "R", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Scirocco GTS", "variante": "GTS", "portes": 3, "places": 4, "reservoir": 55},

                # T-Roc sport
                {"modele": "T-Roc R", "variante": "R", "portes": 5, "places": 5, "reservoir": 55},

                # Tiguan sport
                {"modele": "Tiguan R", "variante": "R", "portes": 5, "places": 5, "reservoir": 58},

                # Touareg sport
                {"modele": "Touareg R", "variante": "R Hybrid", "portes": 5, "places": 5, "reservoir": 75},

                # Arteon sport
                {"modele": "Arteon R", "variante": "R", "portes": 5, "places": 5, "reservoir": 66},

                # Modèles historiques / anciens
                {"modele": "Volkswagen Beetle", "variante": None, "portes": 2, "places": 4, "annees": "1938–2003"},
                {"modele": "Volkswagen Karmann Ghia", "variante": None, "portes": 2, "places": 4,
                 "annees": "1955–1974"},
                {"modele": "Volkswagen Type 2", "variante": None, "portes": 3, "places": 7, "annees": "1950–2013"},

                # Compactes / populaires
                {"modele": "Volkswagen Golf", "variante": None, "portes": 5, "places": 5, "annees": "1974–présent"},
                {"modele": "Volkswagen Polo", "variante": None, "portes": 5, "places": 5, "annees": "1975–présent"},

                # Berlines / familiales
                {"modele": "Volkswagen Passat", "variante": None, "portes": 4, "places": 5, "annees": "1973–présent"},
                {"modele": "Volkswagen Jetta", "variante": None, "portes": 4, "places": 5, "annees": "1979–présent"},

                # SUV / crossovers
                {"modele": "Volkswagen Tiguan", "variante": None, "portes": 5, "places": 5, "annees": "2007–présent"},
                {"modele": "Volkswagen Touareg", "variante": None, "portes": 5, "places": 5, "annees": "2002–présent"},
                {"modele": "Volkswagen T-Roc", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                {"modele": "Volkswagen ID.4", "variante": "Électrique", "portes": 5, "places": 5,
                 "annees": "2020–présent"},

                # Sportives / éditions spéciales
                {"modele": "Volkswagen Golf GTI", "variante": "GTI", "portes": 5, "places": 5,
                 "annees": "1976–présent"},
                {"modele": "Volkswagen Golf R", "variante": "R", "portes": 5, "places": 5, "annees": "2002–présent"},

                # Véhicules utilitaires légers
                {"modele": "Volkswagen Caddy", "variante": None, "portes": 5, "places": 5, "annees": "1980–présent"},
                {"modele": "Volkswagen Transporter", "variante": None, "portes": 3, "places": 7,
                 "annees": "1950–présent"},
                {"modele": "Beetle", "variante": "Coccinelle", "portes": 2, "places": 4, "reservoir": 40},

                # Golf (toutes générations)
                {"modele": "Golf 1", "variante": "Mk1", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Golf 2", "variante": "Mk2", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf 3", "variante": "Mk3", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf 4", "variante": "Mk4", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf 5", "variante": "Mk5", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf 6", "variante": "Mk6", "portes": 3, "places": 5, "reservoir": 55},
                {"modele": "Golf 7", "variante": "Mk7", "portes": 3, "places": 5, "reservoir": 50},
                {"modele": "Golf 8", "variante": "Mk8", "portes": 5, "places": 5, "reservoir": 50},

                # Polo
                {"modele": "Polo 1", "variante": "Mk1", "portes": 3, "places": 5, "reservoir": 42},
                {"modele": "Polo 2", "variante": "Mk2", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo 3", "variante": "Mk3", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo 4", "variante": "Mk4", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo 5", "variante": "Mk5", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Polo 6", "variante": "Mk6", "portes": 5, "places": 5, "reservoir": 40},

                # Passat
                {"modele": "Passat B1", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Passat B2", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Passat B3", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Passat B4", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Passat B5", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Passat B6", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Passat B7", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Passat B8", "variante": None, "portes": 4, "places": 5, "reservoir": 66},

                # Scirocco
                {"modele": "Scirocco 1", "variante": None, "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Scirocco 2", "variante": None, "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Scirocco 3", "variante": None, "portes": 3, "places": 4, "reservoir": 55},

                # Corrado
                {"modele": "Corrado", "variante": None, "portes": 3, "places": 4, "reservoir": 55},

                # Jetta / Bora
                {"modele": "Jetta 1", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Jetta 2", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Jetta 3", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Jetta 4", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Bora", "variante": None, "portes": 4, "places": 5, "reservoir": 55},

                # Lupo / Fox / Up
                {"modele": "Lupo", "variante": None, "portes": 3, "places": 4, "reservoir": 34},
                {"modele": "Fox", "variante": None, "portes": 3, "places": 4, "reservoir": 45},
                {"modele": "Up!", "variante": None, "portes": 3, "places": 4, "reservoir": 35},

                # New Beetle / Beetle moderne
                {"modele": "New Beetle", "variante": None, "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Beetle 2011", "variante": None, "portes": 3, "places": 4, "reservoir": 55},

                # Arteon
                {"modele": "Arteon", "variante": None, "portes": 5, "places": 5, "reservoir": 66},

                # ID (électrique)
                {"modele": "ID.3", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "ID.4", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "ID.5", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "ID.Buzz", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},

                # SUV / Crossover récents
                {"modele": "Tiguan", "variante": None, "portes": 5, "places": 5, "reservoir": 58},
                {"modele": "Tiguan Allspace", "variante": None, "portes": 5, "places": 7, "reservoir": 58},
                {"modele": "T-Roc", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "T-Roc Cabriolet", "variante": "Cabriolet", "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "T-Cross", "variante": None, "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "Taigo", "variante": None, "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "Touareg", "variante": None, "portes": 5, "places": 5, "reservoir": 75},

                # Berlines / compactes modernes
                {"modele": "Passat B9", "variante": None, "portes": 5, "places": 5, "reservoir": 66},
                {"modele": "Jetta 7", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Arteon Shooting Brake", "variante": None, "portes": 5, "places": 5, "reservoir": 66},

                # Monospaces / familiales récentes
                {"modele": "Touran", "variante": None, "portes": 5, "places": 7, "reservoir": 58},
                {"modele": "Sharan", "variante": None, "portes": 5, "places": 7, "reservoir": 70},

                # Utilitaires dérivés VP
                {"modele": "Caddy", "variante": "Life", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Multivan", "variante": None, "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "California", "variante": "Camper", "portes": 5, "places": 4, "reservoir": 70},

                # Électriques récentes (plateforme ID déjà commencée)
                {"modele": "ID.7", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0}

            ],
            # Ajouter d'autres marques ici...
        }

        created_count = 0

        # Tout se passe dans le tenant
        with tenant_context(tenant):
            for marque_nom, modeles in marques_modeles.items():
                try:
                    marque_obj = VoitureMarque.objects.get(nom_marque=marque_nom)
                except VoitureMarque.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f"Marque '{marque_nom}' non trouvée dans le tenant."
                    ))
                    continue

                for m in modeles:
                    # get_or_create pour éviter les doublons, avec societe renseigné
                    _, created = VoitureModele.objects.get_or_create(
                        nom_modele=m["modele"],
                        nom_variante=m.get("variante"),
                        voiture_marque=marque_obj,
                        nombre_portes=m.get("portes", 5),
                        nbre_places=m.get("places", 5),
                        taille_reservoir=m.get("reservoir", 50),
                        societe=tenant  # <-- Obligatoire pour éviter l'erreur NOT NULL
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} modèles ajoutés pour le tenant '{tenant.schema_name}'"
        ))