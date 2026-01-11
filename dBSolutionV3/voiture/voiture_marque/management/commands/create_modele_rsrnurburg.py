from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele



class Command(BaseCommand):
    help = "Ajoute des modèles pour d'autres marques mondiales pour le tenant 'rsr-nurburg'"

    def handle(self, *args, **options):
        # Récupération du tenant
        try:
            tenant = Societe.objects.get(slug='rsr-nurburg')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'rsr-nurburg' introuvable !"))
            return

        # Marques restantes avec quelques modèles représentatifs
        marques_modeles = {

            "Peugeot Sport": [
                {"modele": "Peugeot 205", "variante": "GTI 1.6", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 205", "variante": "GTI 1.9", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 206", "variante": "GTI", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 206", "variante": "RC", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 206", "variante": "S16", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 206", "variante": "206 Rallye", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Peugeot 207", "variante": "GTi", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Peugeot 207", "variante": "RC", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Peugeot 207", "variante": "207 S2000", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Peugeot 208", "variante": "GTi 30th Anniversary", "portes": 3, "places": 4,
                 "reservoir": 45},
                {"modele": "Peugeot 208", "variante": "GTi by Peugeot Sport", "portes": 3, "places": 4,
                 "reservoir": 45},
                {"modele": "Peugeot 208", "variante": "e‑208 GTi", "portes": 3, "places": 4, "reservoir": 0},
                {"modele": "Peugeot 308", "variante": "GTi by Peugeot Sport", "portes": 5, "places": 5,
                 "reservoir": 55},
                {"modele": "Peugeot 508", "variante": "508 PEUGEOT SPORT ENGINEERED", "portes": 5, "places": 5,
                 "reservoir": 60},
                {"modele": "Peugeot 508", "variante": "508 SW PEUGEOT SPORT ENGINEERED", "portes": 5, "places": 5,
                 "reservoir": 60},
                {"modele": "Peugeot 9X8", "variante": "PEUGEOT Hypercar 9X8", "portes": 2, "places": 2,
                 "reservoir": 90},
                {"modele": "Peugeot 208 GTi", "variante": None, "portes": 3, "places": 5, "annees": "2012–2020"},
                {"modele": "Peugeot 208 GT", "variante": None, "portes": 3, "places": 5, "annees": "2020–présent"},

                # Berlines / compactes sportives modernes
                {"modele": "Peugeot 308 GTi", "variante": None, "portes": 5, "places": 5, "annees": "2015–2021"},
                {"modele": "Peugeot 508 PSE", "variante": "PSE", "portes": 4, "places": 5, "annees": "2020–présent"},
                # Peugeot Sport Engineered

                # SUV / crossovers sport
                {"modele": "Peugeot 3008 GT", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},
                {"modele": "Peugeot 5008 GT", "variante": None, "portes": 5, "places": 7, "annees": "2017–présent"},

                # Électriques sportives / hybrides
                {"modele": "Peugeot e-208 GT", "variante": None, "portes": 5, "places": 5, "annees": "2019–présent"},
                {"modele": "Peugeot e-308 GT", "variante": None, "portes": 5, "places": 5, "annees": "2023–présent"},
                {"modele": "Peugeot 508 PSE Hybrid", "variante": "PHEV", "portes": 4, "places": 5,
                 "annees": "2020–présent"},
            ],

            "Porsche": [

                {"modele": "550 Spyder", "nom_variante": None, "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 60},

                {"modele": "911", "nom_variante": "Carrera S", "nombre_portes": 2, "nbre_places": 4,
                 "taille_reservoir": 67},
                {"modele": "911", "nom_variante": "Turbo", "nombre_portes": 2, "nbre_places": 4,
                 "taille_reservoir": 67},

                {"modele": "911", "nom_variante": "GT3", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},
                {"modele": "911", "nom_variante": "GT3 RS", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},
                {"modele": "911", "nom_variante": "GT2 RS", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},

                {"modele": "Cayenne", "nom_variante": "S", "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 75},
                {"modele": "Macan", "nom_variante": None, "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 60},
                {"modele": "Panamera", "nom_variante": "4S", "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 75},

                {"modele": "911", "variante": "996 Carrera", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 Carrera 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 Carrera 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 Turbo", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 Turbo S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 GT3", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "996 GT2", "portes": 2, "places": 4, "reservoir": 64},

                {"modele": "911", "variante": "997 Carrera", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Carrera S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Carrera 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Carrera 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Targa 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Targa 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Turbo", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 Turbo S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 GT3", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 GT3 RS", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 GT2", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "997 GT2 RS", "portes": 2, "places": 4, "reservoir": 64},

                {"modele": "911", "variante": "991 Carrera", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Carrera S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Carrera 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Carrera 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Targa 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Targa 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Turbo", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 Turbo S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 GT3", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 GT3 RS", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "991 GT2 RS", "portes": 2, "places": 4, "reservoir": 64},

                {"modele": "911", "variante": "992 Carrera", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Carrera S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Carrera 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Carrera 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Targa 4", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Targa 4S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Turbo", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 Turbo S", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 GT3", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 GT3 RS", "portes": 2, "places": 4, "reservoir": 64},
                {"modele": "911", "variante": "992 GT2 RS", "portes": 2, "places": 4, "reservoir": 64}
            ],

            "Alfa Romeo": [
                {"modele": "24 HP", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "G1", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 65},
                {"modele": "6C", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "8C 2300", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "8C 2900", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 75},

                {"modele": "Giulietta", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Giulietta Spider", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Giulia", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 48},
                {"modele": "Giulia", "variante": "Veloce", "portes": 4, "places": 5, "reservoir": 48},
                {"modele": "Giulia GTA", "variante": "Performance", "portes": 4, "places": 5, "reservoir": 50},

                {"modele": "Alfa 1300", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 45},
                {"modele": "Alfa 1600", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "Alfa 1750", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Alfa 2000", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Alfa 2600", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Duetto", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 50},

                {"modele": "Alfasud", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 45},
                {"modele": "Alfetta", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Alfetta GTV", "variante": "GTV", "portes": 2, "places": 4, "reservoir": 55},
                {"modele": "75", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "90", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "164", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 65},

                {"modele": "33", "variante": "Standard", "portes": 3, "places": 5, "reservoir": 50},
                {"modele": "145", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "146", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "147", "variante": "Standard", "portes": 3, "places": 5, "reservoir": 50},
                {"modele": "155", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "156", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "159", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},

                {"modele": "GT", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Brera", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Spider", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 50},

                {"modele": "MiTo", "variante": "Standard", "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "4C", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "4C Spider", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 40},

                {"modele": "Stelvio", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Stelvio", "variante": "Quadrifoglio", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Tonale", "variante": "Base", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Milano", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 50}
            ],

            "BMW M": [

                {"modele": "M3 E30", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M5 E28", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},

                {"modele": "M3 E36", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M3 E36", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M3 E36 Convertible", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M5 E34", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},

                {"modele": "M3 E46", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M3 E46 Convertible", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M5 E60", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "M6 E63", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "M6 E64", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 80},

                {"modele": "M3 F80", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M4 F82", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4 F83", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M5 F10", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "M6 F12", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "M6 F13", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "X5 M E70", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X6 M E71", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 80},

                {"modele": "M2 F87", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 52},
                {"modele": "M3 G80", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M4 G82", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4 G83", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M5 G30", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "M8 F91", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "M8 F92", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "X3 M F97", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "X4 M F98", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "X5 M G05", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X6 M G06", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X7 M G07", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 85},

                {"modele": "M1", "variante": "Standard", "portes": 2, "places": 2, "reservoir": 90},

                {"modele": "M2", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "M2", "variante": "Competition", "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "M2", "variante": "CS", "portes": 2, "places": 4, "reservoir": 50},

                {"modele": "M3", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M3", "variante": "Competition", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M3", "variante": "CS", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "M3", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 60},

                {"modele": "M4", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4", "variante": "Competition", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4", "variante": "CS", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4", "variante": "Cabriolet", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "M4", "variante": "Competition Cabriolet", "portes": 2, "places": 4, "reservoir": 60},

                {"modele": "M5", "variante": "Standard", "portes": 4, "places": 5, "reservoir": 68},
                {"modele": "M5", "variante": "Competition", "portes": 4, "places": 5, "reservoir": 68},
                {"modele": "M5", "variante": "CS", "portes": 4, "places": 5, "reservoir": 68},
                {"modele": "M5", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 68},

                {"modele": "M6", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 75},
                {"modele": "M6", "variante": "Competition", "portes": 2, "places": 4, "reservoir": 75},
                {"modele": "M6", "variante": "Gran Coupe", "portes": 4, "places": 5, "reservoir": 75},

                {"modele": "M8", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 78},
                {"modele": "M8", "variante": "Competition", "portes": 2, "places": 4, "reservoir": 78},
                {"modele": "M8", "variante": "Gran Coupe", "portes": 4, "places": 5, "reservoir": 78},
                {"modele": "M8", "variante": "Competition Gran Coupe", "portes": 4, "places": 5, "reservoir": 78},

                {"modele": "X3 M", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "X3 M", "variante": "Competition", "portes": 5, "places": 5, "reservoir": 70},

                {"modele": "X4 M", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "X4 M", "variante": "Competition", "portes": 5, "places": 5, "reservoir": 70},

                {"modele": "X5 M", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "X5 M", "variante": "Competition", "portes": 5, "places": 5, "reservoir": 85},

                {"modele": "X6 M", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "X6 M", "variante": "Competition", "portes": 5, "places": 5, "reservoir": 85},

                {"modele": "XM", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 90},
                {"modele": "XM", "variante": "Label", "portes": 5, "places": 5, "reservoir": 90},
                {"modele": "XM", "variante": "50e", "portes": 5, "places": 5, "reservoir": 90}
            ],

            "Dodge": [

                {"modele": "Charger", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Challenger", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 65},
                {"modele": "Dart", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Neon", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Avenger", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},

                {"modele": "Durango", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},
                {"modele": "Journey", "variante": "SUV / Crossover", "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "Grand Caravan", "variante": "Minivan", "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "Ram 1500", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 95}
            ],

            "Dodge SRT": [

                {"modele": "Challenger SRT Hellcat", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Challenger SRT Demon", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Charger SRT Hellcat", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Charger SRT Widebody", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},

                {"modele": "Durango SRT", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},
                {"modele": "Ram 1500 TRX", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 95}
            ],

            "De Tomaso": [
                {"modele": "Pantera", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Mangusta", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "Valentino", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Longchamp", "variante": "Cabriolet", "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Deauville", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},

                {"modele": "P72", "variante": "Coupé moderne", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "P72 Spider", "variante": "Cabriolet moderne", "portes": 2, "places": 2, "reservoir": 70}
            ],

            "Ferrari": [
                {"modele": "125 S", "variante": "Base", "portes": 0, "places": 2, "reservoir": 120},
                {"modele": "166 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "166 MM", "variante": "Barchetta", "portes": 0, "places": 2, "reservoir": 120},
                {"modele": "195 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "212 Inter", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},

                {"modele": "250 GT", "variante": "Berlinetta", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "250 GTO", "variante": "Berlinetta", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "250 Testa Rossa", "variante": "Spyder", "portes": 0, "places": 2, "reservoir": 120},
                {"modele": "275 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "330 GTC", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "365 GTB/4", "variante": "Daytona Coupe", "portes": 2, "places": 2, "reservoir": 120},

                {"modele": "365 GT4 BB", "variante": "Berlinetta Boxer", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "308 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "308 GTS", "variante": "Targa", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "328 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Testarossa", "variante": "Base", "portes": 2, "places": 2, "reservoir": 120},

                {"modele": "F40", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 95},
                {"modele": "512 TR", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 120},
                {"modele": "F355", "variante": "Berlinetta", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "F355", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 80},

                {"modele": "360 Modena", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "360 Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "430 Scuderia", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "F430", "variante": "Spider", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Enzo", "variante": "Base", "portes": 2, "places": 2, "reservoir": 90},

                {"modele": "458 Italia", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "458 Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "488 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "488 Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "GTC4Lusso", "variante": "Base", "portes": 4, "places": 4, "reservoir": 92},

                {"modele": "F8 Tributo", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "F8 Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "SF90 Stradale", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "296 GTB", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 85},
                {"modele": "296 GTS", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 85},
                {"modele": "Purosangue", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 92},
                {"modele": "Roma", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 86},
                {"modele": "Roma Spider", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 86},
                {"modele": "Amalfi", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 82}
            ],

            "Mazda": [

                {"modele": "R360 Coupé", "variante": "Base", "portes": 2, "places": 4, "reservoir": 30},
                {"modele": "Mazda 1000 / Familia", "variante": "Berline", "portes": 4, "places": 5, "reservoir": 40},
                {"modele": "Cosmo Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "Mazda 121", "variante": "Berline", "portes": 4, "places": 5, "reservoir": 45},
                {"modele": "Mazda RX-7", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Mazda 323", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Mazda MX-5 Miata NA", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Mazda RX-8", "variante": "Coupe", "portes": 4, "places": 4, "reservoir": 60},
                {"modele": "Mazda MX-5 Miata NB", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Mazda MX-5 Miata NC", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "Mazda MX-5 Miata ND", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 50},

                {"modele": "Mazda2", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 42},
                {"modele": "Mazda3", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 51},
                {"modele": "Mazda3", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 51},
                {"modele": "Mazda6", "variante": "Berline", "portes": 4, "places": 5, "reservoir": 62},
                {"modele": "Mazda CX-3", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 48},
                {"modele": "Mazda CX-30", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Mazda CX-5", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 56},
                {"modele": "Mazda CX-50", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 61},
                {"modele": "Mazda CX-60", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "Mazda CX-70", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "Mazda CX-80", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 68},
                {"modele": "Mazda CX-90", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 68},
                {"modele": "Mazda MX-30", "variante": "Crossover EV", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "Mazda 6e", "variante": "Sedan EV", "portes": 4, "places": 5, "reservoir": 0},
                {"modele": "Mazda Vision-X Coupe", "variante": "Concept", "portes": 4, "places": 4, "reservoir": 0}
            ],

            "Bentley": [

                {"modele": "Bentley 3 Litre", "variante": "Tourer", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Bentley 4½ Litre", "variante": "Tourer", "portes": 2, "places": 2, "reservoir": 95},
                {"modele": "Bentley 6½ Litre", "variante": "Speed", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Bentley Mark VI", "variante": "Saloon", "portes": 4, "places": 5, "reservoir": 100},
                {"modele": "Bentley R Type", "variante": "Saloon", "portes": 4, "places": 5, "reservoir": 100},
                {"modele": "Bentley Continental R", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Bentley Continental S", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},

                {"modele": "Bentley Arnage", "variante": "Saloon", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "Bentley Azure", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 95},
                {"modele": "Bentley Continental GT", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Bentley Continental GTC", "variante": "Convertible", "portes": 2, "places": 4,
                 "reservoir": 90},

                {"modele": "Bentley Flying Spur", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "Bentley Mulsanne", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "Bentley Continental GT V8", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Bentley Continental GT Speed", "variante": "Coupe", "portes": 2, "places": 4,
                 "reservoir": 90},
                {"modele": "Bentley Continental GTC V8", "variante": "Convertible", "portes": 2, "places": 4,
                 "reservoir": 90},

                {"modele": "Bentley Continental GT Speed", "variante": "Coupe", "portes": 2, "places": 4,
                 "reservoir": 90},
                {"modele": "Bentley Continental GTC Speed", "variante": "Convertible", "portes": 2, "places": 4,
                 "reservoir": 90},
                {"modele": "Bentley Flying Spur W12", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "Bentley Bentayga", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "Bentley Bentayga Speed", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "Bentley Bacalar", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80}
            ],

            "Audi S": [

                {"modele": "Audi S2", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Audi S4 B5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Audi S4 B5 Avant", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Audi S6 C4", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Audi S6 C4 Avant", "variante": "Break", "portes": 5, "places": 5, "reservoir": 80},

                {"modele": "Audi S3 8L", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Audi S4 B6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Audi S4 B6 Avant", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Audi S6 C5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Audi S8 D3", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "Audi S3 8P", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Audi S4 B8", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Audi S4 B8 Avant", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Audi S5 B8", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Audi S5 B8 Cabriolet", "variante": "Convertible", "portes": 2, "places": 4,
                 "reservoir": 70},
                {"modele": "Audi S6 C6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Audi S7 4G", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "Audi S8 D4", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "Audi S3 8Y", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Audi S4 B9", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Audi S4 Avant B9", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Audi S5 F5", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Audi S5 Cabriolet F5", "variante": "Convertible", "portes": 2, "places": 4,
                 "reservoir": 70},
                {"modele": "Audi S6 C8", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Audi S7 C8", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "Audi S8 D5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "Audi SQ5", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Audi SQ7", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 85},
                {"modele": "Audi SQ8", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 85}
            ],

            "BMW": [

                {"modele": "2002", "variante": "Base", "portes": 2, "places": 4, "reservoir": 55},
                {"modele": "3 Series E21", "variante": "Sedan", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "3 Series E30", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "3 Series E30", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "5 Series E12", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "5 Series E28", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "6 Series E24", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},

                {"modele": "3 Series E36", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "3 Series E36", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "5 Series E34", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "7 Series E32", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "3 Series E46", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "3 Series E46", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "3 Series E46", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "5 Series E60", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "5 Series E61", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "6 Series E63", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "6 Series E64", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "7 Series E65", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "1 Series F20", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "1 Series F21", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "2 Series F22", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 52},
                {"modele": "2 Series F23", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 52},
                {"modele": "3 Series F30", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "3 Series F31", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "4 Series F32", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "4 Series F33", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "5 Series F10", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "5 Series F11", "variante": "Touring", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "6 Series F12", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "6 Series F13", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "7 Series F01", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "X1 E84", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "X3 F25", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "X5 E70", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X6 E71", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 80},

                {"modele": "1 Series F40", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "2 Series G42", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 52},
                {"modele": "3 Series G20", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "4 Series G22", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "5 Series G30", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "6 Series G32", "variante": "Gran Turismo", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "7 Series G11", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "X1 F48", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "X3 G01", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "X5 G05", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X6 G06", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "X7 G07", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 85}
            ],

            "Ford GT": [
                {"modele": "GT40", "variante": "Coupé course", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "GT40 Mk II", "variante": "Coupé course", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "GT40 Mk III", "variante": "Coupé route", "portes": 2, "places": 2, "reservoir": 100},

                {"modele": "Ford GT (2005-2006)", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Ford GT (2016+)", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 90}
            ],

            "Mazda Speed": [

                {"modele": "MX-5 Miata NA", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "MX-5 Miata NB", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Mazda3", "variante": "MazdaSpeed", "portes": 4, "places": 5, "reservoir": 51},
                {"modele": "Mazda6", "variante": "MazdaSpeed", "portes": 4, "places": 5, "reservoir": 62},
                {"modele": "MX-5 Miata NC", "variante": "MazdaSpeed", "portes": 2, "places": 2, "reservoir": 50}
            ],

            "Aston Martin Vantage": [

                {"modele": "Vantage V8", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Vantage V8", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "V8 Vantage S", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "V8 Vantage S", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Vantage V12", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 95},
                {"modele": "Vantage V12", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 95},
                {"modele": "Vantage AMR", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Vantage AMR", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Vantage GT8", "variante": "Edition Limitée", "portes": 2, "places": 2, "reservoir": 80}
            ],

            "Bugatti": [

                {"modele": "Type 35", "variante": "Racing", "portes": 0, "places": 2, "reservoir": 60},
                {"modele": "Type 41 Royale", "variante": "Luxury", "portes": 4, "places": 4, "reservoir": 120},
                {"modele": "Type 57", "variante": "SC Atlantic", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Type 57", "variante": "Ventoux", "portes": 2, "places": 2, "reservoir": 90},

                {"modele": "Veyron 16.4", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Veyron 16.4 Grand Sport", "variante": "Convertible", "portes": 2, "places": 2,
                 "reservoir": 100},
                {"modele": "Chiron", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Chiron Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Chiron Pur Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Chiron Super Sport 300+", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Bolide", "variante": "Hypercar", "portes": 2, "places": 1, "reservoir": 90},
                {"modele": "Divo", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "La Voiture Noire", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Centodieci", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90}
            ],

            "Chevrolet": [

                {"modele": "Bel Air", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Impala", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 75},
                {"modele": "Camaro", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Corvette", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Corvette", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Nova", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 65},

                {"modele": "Malibu", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Cruze", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Spark", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 35},
                {"modele": "Trax", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Equinox", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Blazer", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "Traverse", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "Tahoe", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 85},
                {"modele": "Suburban", "variante": "SUV Long", "portes": 5, "places": 8, "reservoir": 95},
                {"modele": "Colorado", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Silverado", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Corvette C8", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Corvette C8", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 65}
            ],

            "Citroën": [
                {"modele": "2CV", "variante": "Berline", "portes": 4, "places": 4, "reservoir": 25},
                {"modele": "DS", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "CX", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "BX", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "XM", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "C25", "variante": "Fourgon", "portes": 4, "places": 3, "reservoir": 70},

                {"modele": "C1", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "C1", "variante": "Hatchback", "portes": 5, "places": 4, "reservoir": 35},
                {"modele": "C3", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "C3 Aircross", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "C4", "variante": "Sedan", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "C4 Cactus", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "C5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "C5 Aircross", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "C6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "C-Elysée", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Berlingo", "variante": "Van", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Berlingo", "variante": "Van Electrique", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "ë-C4", "variante": "Sedan Electrique", "portes": 5, "places": 5, "reservoir": 0}
            ],

            "Citroën Sport": [

                {"modele": "BX 4TC", "variante": "Rallye", "portes": 5, "places": 4, "reservoir": 70},
                {"modele": "Xsara WRC", "variante": "Rallye", "portes": 5, "places": 4, "reservoir": 60},
                {"modele": "C4 WRC", "variante": "Rallye", "portes": 5, "places": 4, "reservoir": 60},
                {"modele": "DS3 WRC", "variante": "Rallye", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "DS3 R3", "variante": "Rallye / Route", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "DS4 Racing", "variante": "Sportive", "portes": 5, "places": 4, "reservoir": 50},
                {"modele": "DS5 Racing", "variante": "Sportive", "portes": 5, "places": 4, "reservoir": 55},
                {"modele": "C-Elysée WTCC", "variante": "Course", "portes": 4, "places": 4, "reservoir": 50},

                {"modele": "C3 R5", "variante": "Rallye", "portes": 5, "places": 4, "reservoir": 50},
                {"modele": "C3 Sport", "variante": "GT / Edition Limitée", "portes": 5, "places": 4, "reservoir": 45},
                {"modele": "C4 Sport", "variante": "GT", "portes": 5, "places": 4, "reservoir": 50},
                {"modele": "C4 WRC Edition", "variante": "GT / Rallye", "portes": 5, "places": 4, "reservoir": 50}
            ],

            "Cupra": [

                {"modele": "Cupra Ibiza", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "Cupra Leon", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Cupra Leon ST", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Cupra Leon Competición", "variante": "Racing", "portes": 5, "places": 4, "reservoir": 50},

                {"modele": "Cupra Ateca", "variante": "SUV Sport", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Cupra Formentor", "variante": "SUV Coupé Sport", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Cupra Born", "variante": "Hatchback Electrique", "portes": 5, "places": 5, "reservoir": 0},
                {"modele": "Cupra Tavascan", "variante": "SUV Electrique Concept", "portes": 5, "places": 5,
                 "reservoir": 0}
            ],

            "DS Automobiles": [

                {"modele": "DS", "variante": "Sedan Classique", "portes": 4, "places": 5, "reservoir": 50},

                {"modele": "DS3", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 45},
                {"modele": "DS3 Crossback", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "DS4", "variante": "Sedan / Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "DS4 Crossback", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "DS5", "variante": "Hatchback / SUV", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "DS7 Crossback", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "DS9", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},

                {"modele": "DS3 E-Tense", "variante": "Hatchback Electrique", "portes": 5, "places": 4, "reservoir": 0},
                {"modele": "DS7 Crossback E-Tense", "variante": "SUV Hybride Rechargeable", "portes": 5, "places": 5,
                 "reservoir": 55}
            ],

            "Fiat": [

                {"modele": "500", "variante": "Cabriolet Classique", "portes": 2, "places": 4, "reservoir": 20},
                {"modele": "126", "variante": "Hatchback", "portes": 2, "places": 4, "reservoir": 22},
                {"modele": "Panda", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 30},
                {"modele": "Panda", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 30},
                {"modele": "Tipo", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Bravo", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},

                {"modele": "500", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "500", "variante": "Hatchback", "portes": 5, "places": 4, "reservoir": 35},
                {"modele": "500X", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "500L", "variante": "MPV", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "Punto", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 40},
                {"modele": "Punto", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "Doblo", "variante": "MPV / Van", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Fiorino", "variante": "Van", "portes": 3, "places": 2, "reservoir": 40},
                {"modele": "Tipo Cross", "variante": "Sedan / Hatchback", "portes": 5, "places": 5, "reservoir": 50},

                {"modele": "500e", "variante": "Hatchback Electrique", "portes": 3, "places": 4, "reservoir": 0},
                {"modele": "500e", "variante": "Hatchback Electrique", "portes": 5, "places": 4, "reservoir": 0}
            ],

            "Maserati": [

                {"modele": "A6 1500", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "A6G 2000", "variante": "Berline", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "3500 GT", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 95},
                {"modele": "5000 GT", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 95},
                {"modele": "Mexico", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 95},
                {"modele": "Quattroporte I", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 105},
                {"modele": "Ghibli I", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Mistral", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Indy", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Bora", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Merak", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Khamsin", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 100},
                {"modele": "Kyalami", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 100},

                {"modele": "Biturbo", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "228", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "Karif", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Shamal", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},

                {"modele": "Ghibli II", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Quattroporte IV", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "3200 GT", "variante": "Coupe", "portes": 2, "places": 4,
                 "reservoir": 90},

                {"modele": "Maserati Coupé", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Maserati Spyder", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "GranSport", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Quattroporte V", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "MC12", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "GranTurismo", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},

                {"modele": "GranCabrio", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Ghibli (M157)", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Ghibli Trofeo", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "Quattroporte VI", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                {"modele": "Levante", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "Levante Trofeo", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "Grecale", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "Grecale Trofeo", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 80},
                {"modele": "MC20", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "MC20 Cielo", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 75},

                {"modele": "MCPura", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "MCPura Cielo", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "GT2 Stradale", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 75}
            ],

            "Mercedes-AMG": [

                {"modele": "C36", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "E36", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "SL60", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "S70", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "C55", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "E55", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "SL55", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "CLK63", "variante": "AMG", "portes": 2, "places": 4, "reservoir": 80},
                {"modele": "SLK55", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 60},

                {"modele": "C63", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 66},
                {"modele": "E63", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "S63", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "SL63", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "GT", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "GT C", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "GT R", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 70},

                {"modele": "C63 S", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 66},
                {"modele": "E63 S", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "S63", "variante": "AMG", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "GT Black Series", "variante": "AMG", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "GLE 63", "variante": "AMG", "portes": 5, "places": 5, "reservoir": 93},
                {"modele": "GLC 63", "variante": "AMG", "portes": 5, "places": 5, "reservoir": 66},
                {"modele": "AMG ONE", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 65}
            ],

            "McLaren": [
                {"modele": "F1", "variante": "Base", "portes": 2, "places": 3, "reservoir": 90},
                {"modele": "F1 LM", "variante": "Edition Limitée", "portes": 2, "places": 3, "reservoir": 90},
                {"modele": "F1 GTR Road Version", "variante": "Edition Limitée", "portes": 2, "places": 3,
                 "reservoir": 90},

                {"modele": "MP4-12C", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "MP4-12C Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 78},

                {"modele": "650S", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "650S Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "P1", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 68},
                {"modele": "675LT", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "675LT Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 72},

                {"modele": "720S", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "720S Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "765LT", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "765LT Spider", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "Speedtail", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 85},
                {"modele": "Elva", "variante": "Roadster", "portes": 0, "places": 2, "reservoir": 68},
                {"modele": "Artura", "variante": "Coupe Hybride", "portes": 2, "places": 2, "reservoir": 70},

                {"modele": "McLaren Solus", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "McLaren Sabre", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "McLaren Speedtail LM", "variante": "Edition Limitée", "portes": 2, "places": 2,
                 "reservoir": 85}
            ],

            # UK
            "Mini": [
                # Cooper One
                {"modele": "Cooper", "variante": "One", "portes": 3, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": "One", "portes": 5, "places": 4, "reservoir": 40},

                # Cooper
                {"modele": "Cooper", "variante": None, "portes": 3, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": "S", "portes": 3, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": "SE", "portes": 3, "places": 4, "reservoir": 40},  # électrique
                {"modele": "Cooper", "variante": "John Cooper Works", "portes": 3, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": None, "portes": 5, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": "S", "portes": 5, "places": 4, "reservoir": 40},
                {"modele": "Cooper", "variante": "John Cooper Works", "portes": 5, "places": 4, "reservoir": 40},

                # Countryman
                {"modele": "Countryman", "variante": "One", "portes": 5, "places": 5, "reservoir": 51},
                {"modele": "Countryman", "variante": None, "portes": 5, "places": 5, "reservoir": 51},
                {"modele": "Countryman", "variante": "S", "portes": 5, "places": 5, "reservoir": 51},
                {"modele": "Countryman", "variante": "John Cooper Works", "portes": 5, "places": 5, "reservoir": 51},

                # Clubman
                {"modele": "Clubman", "variante": "One", "portes": 5, "places": 4, "reservoir": 48},
                {"modele": "Clubman", "variante": None, "portes": 5, "places": 4, "reservoir": 48},
                {"modele": "Clubman", "variante": "S", "portes": 5, "places": 4, "reservoir": 48},
                {"modele": "Clubman", "variante": "John Cooper Works", "portes": 5, "places": 4, "reservoir": 48},

                # Convertible
                {"modele": "Convertible", "variante": "One", "portes": 2, "places": 4, "reservoir": 40},
                {"modele": "Convertible", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
                {"modele": "Convertible", "variante": "S", "portes": 2, "places": 4, "reservoir": 40},
                {"modele": "Convertible", "variante": "John Cooper Works", "portes": 2, "places": 4, "reservoir": 40},

                # Paceman
                {"modele": "Paceman", "variante": "One", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Paceman", "variante": None, "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Paceman", "variante": "S", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Paceman", "variante": "John Cooper Works", "portes": 3, "places": 4, "reservoir": 50},
            ],

            "Rolls-Royce": [
                {"modele": "Phantom", "variante": None, "portes": 4, "places": 5, "reservoir": 100},
                {"modele": "Phantom EWB", "variante": "Extended Wheelbase", "portes": 4, "places": 5, "reservoir": 100},

                {"modele": "Ghost", "variante": None, "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "Ghost EWB", "variante": "Extended Wheelbase", "portes": 4, "places": 5, "reservoir": 90},

                {"modele": "Wraith", "variante": "wraith", "portes": 2, "places": 4, "reservoir": 83},
                {"modele": "Dawn", "variante": "Cabriolet", "portes": 2, "places": 4, "reservoir": 83},

                {"modele": "Cullinan", "variante": "Cullinan", "portes": 5, "places": 5, "reservoir": 105},
                {"modele": "Cullinan Black Badge", "variante": "Sport Luxe", "portes": 5, "places": 5,
                 "reservoir": 105},

                {"modele": "Spectre", "variante": "Electrique", "portes": 2, "places": 4, "reservoir": 0}
            ],

            "Aston Martin": [
                # DB5 (classique)
                {"modele": "DB5", "variante": None, "portes": 2, "places": 4, "reservoir": 75},
                {"modele": "DB5", "variante": "Goldfinger", "portes": 2, "places": 4, "reservoir": 75},

                # DB6
                {"modele": "DB6", "variante": None, "portes": 2, "places": 4, "reservoir": 75},

                # DBS (ancienne génération)
                {"modele": "DBS", "variante": None, "portes": 2, "places": 4, "reservoir": 78},

                # V8 Vantage classique
                {"modele": "V8 Vantage", "variante": None, "portes": 2, "places": 2, "reservoir": 78},

                # DB7
                {"modele": "DB7", "variante": None, "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "DB7", "variante": "Vantage", "portes": 2, "places": 2, "reservoir": 78},

                # DB9
                {"modele": "DB9", "variante": None, "portes": 2, "places": 4, "reservoir": 78},
                {"modele": "DB9", "variante": "Volante", "portes": 2, "places": 4, "reservoir": 78},

                # DB11
                {"modele": "DB11", "variante": None, "portes": 2, "places": 4, "reservoir": 78},
                {"modele": "DB11", "variante": "AMR", "portes": 2, "places": 4, "reservoir": 78},

                # Vantage moderne
                {"modele": "Vantage", "variante": None, "portes": 2, "places": 2, "reservoir": 78},
                {"modele": "Vantage", "variante": "AMR", "portes": 2, "places": 2, "reservoir": 78},

                # DBS Superleggera
                {"modele": "DBS Superleggera", "variante": None, "portes": 2, "places": 2, "reservoir": 78},

                # Rapide AMR
                {"modele": "Rapide AMR", "variante": None, "portes": 4, "places": 4, "reservoir": 78},

                # DBX (SUV moderne)
                {"modele": "DBX", "variante": None, "portes": 5, "places": 5, "reservoir": 93},
                {"modele": "DBX", "variante": "AMR", "portes": 5, "places": 5, "reservoir": 93},

                # Valhalla (hybride)
                {"modele": "Valhalla", "variante": None, "portes": 2, "places": 2, "reservoir": 68},

                # Vulcan (track-only)
                {"modele": "Vulcan", "variante": None, "portes": 2, "places": 1, "reservoir": 120},
            ],

            "Lotus": [
                {"modele": "Elise", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                # classique léger :contentReference[oaicite:1]{index=1}
                {"modele": "Elise Sport", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                # version sportive :contentReference[oaicite:2]{index=2}
                {"modele": "Exige", "variante": None, "portes": 2, "places": 2, "reservoir": 55},
                # dérivé de Elise, plus performance :contentReference[oaicite:3]{index=3}
                {"modele": "Evora", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                # sport GT plus spacieuse :contentReference[oaicite:4]{index=4}
                {"modele": "Emira", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                # nouvelle génération sport :contentReference[oaicite:5]{index=5}
                {"modele": "Evija", "variante": None, "portes": 2, "places": 2, "reservoir": 0},
                # hypercar électrique (pas de réservoir) :contentReference[oaicite:6]{index=6}
                {"modele": "Eletre", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
                # SUV électrique :contentReference[oaicite:7]{index=7}
                {"modele": "Emeya", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
                # berline électrique :contentReference[oaicite:8]{index=8}
                {"modele": "Esprit", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                # classique sport (historique) :contentReference[oaicite:9]{index=9}
                {"modele": "Elite", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                # modèle historique des années 1950‑60 :contentReference[oaicite:10]{index=10}
                {"modele": "Elan", "variante": None, "portes": 2, "places": 2, "reservoir": 45},
                # cabriolet historique :contentReference[oaicite:11]{index=11}
                {"modele": "3‑Eleven", "variante": None, "portes": 0, "places": 2, "reservoir": 60},
                # version piste/route limitée :contentReference[oaicite:12]{index=12}
            ],
            "Acura": [
                # Modèles actuels
                {"modele": "Integra", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                # hatchback/liftback compacte :contentReference[oaicite:0]{index=0}
                {"modele": "Integra Type S", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                # version sportive :contentReference[oaicite:1]{index=1}

                {"modele": "ADX", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                # sous-compact SUV :contentReference[oaicite:2]{index=2}
                {"modele": "RDX", "variante": None, "portes": 5, "places": 5, "reservoir": 65},
                # SUV compact :contentReference[oaicite:3]{index=3}
                {"modele": "MDX", "variante": None, "portes": 5, "places": 7, "reservoir": 75},
                # SUV 3 rangées :contentReference[oaicite:4]{index=4}

                # Modèles historiques ou discontinués
                {"modele": "TLX", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                # berline (discontinuée en 2025) :contentReference[oaicite:5]{index=5}
                {"modele": "ILX", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                # sous-compact sedan (terminée 2022) :contentReference[oaicite:6]{index=6}
                {"modele": "RLX", "variante": None, "portes": 4, "places": 5, "reservoir": 65},
                # grande berline de luxe (arrêtée 2020) :contentReference[oaicite:7]{index=7}
                {"modele": "Legend", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                # ancien modèle premium :contentReference[oaicite:8]{index=8}
                {"modele": "CSX", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
                # sedan compact Canada uniquement :contentReference[oaicite:9]{index=9}
                {"modele": "ZDX", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
                # SUV EV (production terminée fin 2025) :contentReference[oaicite:10]{index=10}
                {"modele": "CDX", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                # SUV China uniquement :contentReference[oaicite:11]{index=11}

                # Modèles sportifs / spéciaux (historiques)
                {"modele": "NSX", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                # supercar sportive :contentReference[oaicite:12]{index=12}
                {"modele": "TL", "variante": None, "portes": 4, "places": 5, "reservoir": 65},
                # historique (avant TLX) :contentReference[oaicite:13]{index=13}
                {"modele": "TSX", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                # compacte sportive (2004‑2014) :contentReference[oaicite:14]{index=14}
                {"modele": "RSX", "variante": None, "portes": 3, "places": 4, "reservoir": 50},
                # coupé hatchback (2002‑2006) :contentReference[oaicite:15]{index=15}

            ],

            "Renault RS": [
                {"modele": "Clio II RS", "variante": "Phase 1", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio II RS", "variante": "Phase 2", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio II RS", "variante": "RS 172", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio II RS", "variante": "RS 182", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio II RS", "variante": "V6 Phase 1", "portes": 3, "places": 2, "reservoir": 60},
                {"modele": "Clio II RS", "variante": "V6 Phase 2", "portes": 3, "places": 2, "reservoir": 60},

                {"modele": "Clio III RS", "variante": "Phase 1", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio III RS", "variante": "Phase 2", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio III RS", "variante": "Cup", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio III RS", "variante": "Trophy", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio III RS", "variante": "Gordini", "portes": 3, "places": 4, "reservoir": 50},

                {"modele": "Clio IV RS", "variante": "Phase 1", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio IV RS", "variante": "Phase 2", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio IV RS", "variante": "Trophy", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Clio IV RS", "variante": "Trophy R", "portes": 3, "places": 4, "reservoir": 50},

                {"modele": "Megane II RS", "variante": "Phase 1", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane II RS", "variante": "Phase 2", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane II RS", "variante": "R26 F1 Team", "portes": 3, "places": 2, "reservoir": 55},
                {"modele": "Megane II RS", "variante": "R26.R", "portes": 3, "places": 2, "reservoir": 55},

                {"modele": "Megane III RS", "variante": "Base", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane III RS", "variante": "Trophy", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane III RS", "variante": "Trophy-R", "portes": 3, "places": 4, "reservoir": 55},

                {"modele": "Megane IV RS", "variante": "Base", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane IV RS", "variante": "Trophy", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane IV RS", "variante": "Trophy-R", "portes": 3, "places": 4, "reservoir": 55},
                {"modele": "Megane IV RS", "variante": "Ultime", "portes": 3, "places": 4, "reservoir": 55},

                {"modele": "Twingo II RS", "variante": "Phase 1", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "Twingo II RS", "variante": "Phase 2", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "Twingo II RS", "variante": "Gordini", "portes": 3, "places": 4, "reservoir": 35},

                {"modele": "Renault Sport RS 01", "variante": "RS 01 Standard", "portes": 2, "places": 2,
                 "reservoir": 65},

                # Modèles Renault Sport actuels et récents
                {"modele": "Clio RS", "variante": None, "portes": 5, "places": 5, "reservoir": 50},  # compacte sportive
                {"modele": "Megane RS", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
                # berline compacte sportive
                {"modele": "Arkana RS", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
                # SUV coupé sportif
                {"modele": "Captur RS Line", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                # SUV compact, finition sportive

                # Modèles historiques Renault Sport
                {"modele": "Twingo RS", "variante": None, "portes": 3, "places": 4, "reservoir": 35},
                # citadine sportive
                {"modele": "Sport Spider", "variante": None, "portes": 2, "places": 2, "reservoir": 50},  # roadster
                {"modele": "Clio RS ", "variante": None, "portes": 3, "places": 5, "reservoir": 50},
                # toutes générations Clio RS
                {"modele": "Megane RS ", "variante": None, "portes": 5, "places": 5,
                 "reservoir": 55},  # toutes générations Megane RS
                {"modele": "Megane RS Trophy", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
                # versions Trophy

            ],

            "Audi": [
                {"modele": "A1", "variante": None, "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "A3", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "A3 Sportback", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "A4", "variante": None, "portes": 4, "places": 5, "reservoir": 54},
                {"modele": "A4 Avant", "variante": None, "portes": 5, "places": 5, "reservoir": 54},
                {"modele": "A5", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "A5 Sportback", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "A5 Coupé", "variante": None, "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "A6", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "A6 Avant", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "A7 Sportback", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "A8", "variante": None, "portes": 4, "places": 5, "reservoir": 75},
                {"modele": "Q2", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Q3", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Q5", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Q5 Sportback", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Q7", "variante": None, "portes": 5, "places": 7, "reservoir": 85},
                {"modele": "Q8", "variante": None, "portes": 5, "places": 5, "reservoir": 85},
                {"modele": "e-tron", "variante": None, "portes": 5, "places": 5, "reservoir": 0},  # électrique
                {"modele": "e-tron GT", "variante": None, "portes": 4, "places": 5, "reservoir": 0},  # électrique
                {"modele": "R8", "variante": None, "portes": 2, "places": 2, "reservoir": 82},  # sportive
                {"modele": "TT", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "TT Roadster", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
            ],
            "Audi RS": [
                {"modele": "RS3", "variante": None, "portes": 5, "places": 5, "reservoir": 50},  # version sportive A3
                {"modele": "RS4 Avant", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "RS5 Coupé", "variante": None, "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "RS6 Avant", "variante": None, "portes": 5, "places": 5, "reservoir": 75},
                {"modele": "RS7 Sportback", "variante": None, "portes": 5, "places": 5, "reservoir": 75},
                {"modele": "SQ5", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "SQ7", "variante": None, "portes": 5, "places": 7, "reservoir": 85},

            ],

            "Alpine": [

                {"modele": "A110 (1961-1977)", "variante": "Berlinette", "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "A310", "variante": "Base", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "A310", "variante": "V6", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "A610", "variante": "V6 Turbo", "portes": 2, "places": 2, "reservoir": 70},

                {"modele": "A110", "variante": "Pure", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "A110", "variante": "Legende", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "A110", "variante": "S", "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "A110", "variante": "GT", "portes": 2, "places": 2, "reservoir": 45}
            ],


            # Espagne
            "SEAT": [
                # Modèles historiques / anciens
                {"modele": "SEAT 600", "variante": None, "portes": 2, "places": 4, "annees": "1957–1973"},
                {"modele": "SEAT 850", "variante": None, "portes": 2, "places": 4, "annees": "1966–1974"},
                {"modele": "SEAT 124", "variante": None, "portes": 4, "places": 5, "annees": "1968–1980"},
                {"modele": "SEAT 127", "variante": None, "portes": 2, "places": 4, "annees": "1972–1982"},

                # Compactes / populaires
                {"modele": "SEAT Ibiza", "variante": None, "portes": 3, "places": 5, "annees": "1984–présent"},
                {"modele": "SEAT León", "variante": None, "portes": 5, "places": 5, "annees": "1999–présent"},
                {"modele": "SEAT Toledo", "variante": None, "portes": 4, "places": 5, "annees": "1991–2019"},

                # SUV / crossovers
                {"modele": "SEAT Arona", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                {"modele": "SEAT Ateca", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},
                {"modele": "SEAT Tarraco", "variante": None, "portes": 5, "places": 7, "annees": "2018–présent"},

                # Sportives / sport edition
                {"modele": "SEAT Ibiza Cupra", "variante": "Cupra", "portes": 3, "places": 5, "annees": "1996–2012"},
                {"modele": "SEAT León Cupra", "variante": "Cupra", "portes": 5, "places": 5, "annees": "1996–présent"},

                # Électriques / hybrides
                {"modele": "SEAT Mii Electric", "variante": "Électrique", "portes": 5, "places": 4,
                 "annees": "2019–présent"},

                {"modele": "Ibiza", "variante": "FR", "portes": 5, "places": 5, "reservoir": 45},
                {"modele": "Ibiza", "variante": "Cupra", "portes": 3, "places": 4, "reservoir": 45},

                {"modele": "Leon", "variante": "FR", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Leon", "variante": "Cupra", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Leon ST", "variante": "Break", "portes": 5, "places": 5, "reservoir": 55},

                {"modele": "Arona", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Ateca", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Tarraco", "variante": None, "portes": 5, "places": 7, "reservoir": 60},

                {"modele": "Toledo", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                {"modele": "Altea", "variante": "MPV", "portes": 5, "places": 5, "reservoir": 55},
                {"modele": "Cordoba", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},

                {"modele": "Mii", "variante": "Citadine", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "Mii Electric", "variante": "Electrique", "portes": 3, "places": 4, "reservoir": 0}



            ],
            "Honda": [

                {"modele": "Civic", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                {"modele": "Civic", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Civic Type R", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Accord", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "Jazz", "variante": None, "portes": 5, "places": 5, "reservoir": 40},
                {"modele": "City", "variante": None, "portes": 4, "places": 5, "reservoir": 40},
                {"modele": "CR-V", "variante": None, "portes": 5, "places": 5, "reservoir": 58},
                {"modele": "HR-V", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Passport", "variante": None, "portes": 5, "places": 5, "reservoir": 65},
                {"modele": "Pilot", "variante": None, "portes": 5, "places": 7, "reservoir": 75},

                {"modele": "Odyssey", "variante": None, "portes": 5, "places": 7, "reservoir": 75},

                {"modele": "NSX", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 70},

                {"modele": "Honda e", "variante": "Electrique", "portes": 5, "places": 4, "reservoir": 0},
                {"modele": "CR-V Hybrid", "variante": "Hybride", "portes": 5, "places": 5, "reservoir": 58},
                {"modele": "Accord Hybrid", "variante": "Hybride", "portes": 4, "places": 5, "reservoir": 60}
            ],

            "Honda Type R": [
                {"modele": "Civic Type R", "variante": "EP3", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Civic Type R", "variante": "FN2", "portes": 3, "places": 4, "reservoir": 50},
                {"modele": "Civic Type R", "variante": "FK8", "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Integra Type R", "variante": "DC2", "portes": 3, "places": 4, "reservoir": 50}
            ],

            "Hispano-Suiza": [

                {"modele": "H6B", "variante": "Berlina", "portes": 4, "places": 5, "reservoir": 80},
                {"modele": "H6C", "variante": "Sport", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "K6", "variante": None, "portes": 4, "places": 5, "reservoir": 80},

                {"modele": "Carmen", "variante": "Coupe Electrique", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Carmen Boulogne", "variante": "Coupe Electrique", "portes": 2, "places": 2, "reservoir": 0}
            ],



            "Hyundai N": [
            {"modele": "i20 N", "variante": None, "portes": 5, "places": 5, "reservoir": 45},
            {"modele": "i30 N", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "Veloster N", "variante": None, "portes": 3, "places": 4, "reservoir": 50},
            {"modele": "Kona N", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "Elantra N", "variante": None, "portes": 4, "places": 5, "reservoir": 50}

            ],

                "Jaguar": [

                {"modele": "XE", "variante": None, "portes": 4, "places": 5, "reservoir": 63},
                {"modele": "XF", "variante": None, "portes": 4, "places": 5, "reservoir": 66},
                {"modele": "XJ", "variante": None, "portes": 4, "places": 5, "reservoir": 80},

                {"modele": "F-Type", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 61},
                {"modele": "F-Type", "variante": "Cabriolet", "portes": 2, "places": 2, "reservoir": 61},

                {"modele": "E-Pace", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "F-Pace", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "I-Pace", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},

                {"modele": "XK", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "XJ-S", "variante": None, "portes": 2, "places": 2, "reservoir": 80}

            ],

            "Jaguar R": [
            {"modele": "XE SV Project 8", "variante": "R", "portes": 4, "places": 5, "reservoir": 66},
            {"modele": "XFR", "variante": None, "portes": 4, "places": 5, "reservoir": 66},
            {"modele": "XKR", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
            {"modele": "F-Type R", "variante": None, "portes": 2, "places": 2, "reservoir": 61},
            {"modele": "F-Type SVR", "variante": None, "portes": 2, "places": 2, "reservoir": 61},
            {"modele": "XJ Supercharged", "variante": "R", "portes": 4, "places": 5, "reservoir": 80},
            {"modele": "F-Pace SVR", "variante": None, "portes": 5, "places": 5, "reservoir": 70}
            ],

            "Innocenti": [
            {"modele": "A40 Berlina", "variante": None, "portes": 4, "places": 5, "reservoir": 35},
            {"modele": "A40 Combinata", "variante": None, "portes": 3, "places": 5, "reservoir": 35},

            {"modele": "950 Spider", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
            {"modele": "IM3 / IM3S / I4 / I5", "variante": None, "portes": 4, "places": 5, "reservoir": 45},

            {"modele": "Innocenti 186 GT", "variante": None, "portes": 2, "places": 4, "reservoir": 50},

            {"modele": "Mini (ADO15)", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
            {"modele": "Mini Cooper Mk1", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
            {"modele": "Mini Cooper Mk2", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
            {"modele": "Mini 90L", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
            {"modele": "Mini 120L", "variante": None, "portes": 2, "places": 4, "reservoir": 40},

            {"modele": "Mini Bertone", "variante": None, "portes": 3, "places": 4, "reservoir": 40},
            {"modele": "Mini 3‑Cilindri", "variante": None, "portes": 3, "places": 4, "reservoir": 40},
            {"modele": "Mini De Tomaso", "variante": None, "portes": 2, "places": 4, "reservoir": 40},

            {"modele": "Regent", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
            {"modele": "IM3‑I4‑I5 (ADO16)", "variante": None, "portes": 4, "places": 5, "reservoir": 45},

            {"modele": "Koral", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
            {"modele": "Elba", "variante": None, "portes": 5, "places": 5, "reservoir": 45},
            {"modele": "Mille", "variante": None, "portes": 3, "places": 5, "reservoir": 45},
            ],

            "Jeep": [
            # Modèles historiques emblématiques
            {"modele": "Willys MB / GPW", "variante": None, "portes": 2, "places": 4, "reservoir": 22},
            {"modele": "Jeepster", "variante": None, "portes": 2, "places": 4, "reservoir": 40},
            {"modele": "CJ‑5", "variante": None, "portes": 2, "places": 4, "reservoir": 45},
            {"modele": "CJ‑7", "variante": None, "portes": 2, "places": 4, "reservoir": 45},
            {"modele": "Jeep Gladiator (1963‑72)", "variante": None, "portes": 2, "places": 5, "reservoir": 55},

            # SUV classiques et anciens
            {"modele": "Cherokee (XJ)", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
            {"modele": "Grand Cherokee (ZJ/WJ)", "variante": None, "portes": 4, "places": 5, "reservoir": 70},

            # Modèles modernes SUV et crossover
            {"modele": "Jeep Wrangler", "variante": "2‑portes", "portes": 2, "places": 4, "reservoir": 70},
            {"modele": "Jeep Wrangler", "variante": "4‑portes", "portes": 4, "places": 5, "reservoir": 70},
            {"modele": "Jeep Renegade", "variante": None, "portes": 5, "places": 5, "reservoir": 51},
            {"modele": "Jeep Compass", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            {"modele": "Jeep Cherokee", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            {"modele": "Jeep Grand Cherokee", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
            {"modele": "Jeep Avenger", "variante": None, "portes": 5, "places": 5, "reservoir": 45},

            # Gamme Wagoneer (full‑size / luxe)
            {"modele": "Wagoneer", "variante": None, "portes": 5, "places": 7, "reservoir": 85},
            {"modele": "Grand Wagoneer", "variante": None, "portes": 5, "places": 7, "reservoir": 90},
            {"modele": "Wagoneer S", "variante": None, "portes": 5, "places": 5, "reservoir": 75},

            # Pickup basé sur Wrangler
            {"modele": "Jeep Gladiator", "variante": None, "portes": 4, "places": 5, "reservoir": 76},

            # Véhicules électriques / futurs
            {"modele": "Jeep Recon", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            # EV, pas de réservoir traditionnel
            ],

            "Kia": [
            # Citadines et compactes
            {"modele": "Picanto / Morning", "variante": None, "portes": 4, "places": 5, "reservoir": 35},
            {"modele": "Rio / K3", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
            {"modele": "K4", "variante": None, "portes": 4, "places": 5, "reservoir": 45},

            # Compactes / berlines
            {"modele": "Ceed", "variante": "5 portes", "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "Ceed SW", "variante": "Break", "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "ProCeed", "variante": "Shooting Brake", "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "K5 / Optima", "variante": None, "portes": 4, "places": 5, "reservoir": 55},

            # Familles / familiales
            {"modele": "Carnival / Sedona", "variante": None, "portes": 5, "places": 7, "reservoir": 70},

            # SUV / crossovers thermiques
            {"modele": "Stonic", "variante": None, "portes": 5, "places": 5, "reservoir": 45},
            {"modele": "Seltos", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
            # *2026+ selon marché* :contentReference[oaicite:0]{index=0}
            {"modele": "Sportage", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            {"modele": "Sorento", "variante": None, "portes": 5, "places": 7, "reservoir": 70},
            {"modele": "Telluride", "variante": None, "portes": 5, "places": 7, "reservoir": 75},
            # Nouvelle génération en 2027 :contentReference[oaicite:1]{index=1}

            # Electriques et hybrides (réservoir 0 → EV)
            {"modele": "EV3", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            {"modele": "EV4", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            # hatch/compact EV :contentReference[oaicite:2]{index=2}
            {"modele": "EV5", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            {"modele": "EV6", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            # EV crossover 5 portes :contentReference[oaicite:3]{index=3}
            {"modele": "EV9", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            # EV large SUV :contentReference[oaicite:4]{index=4}

            # Autres modèles thermiques historiques ou moins courants
            {"modele": "Carens", "variante": None, "portes": 5, "places": 7, "reservoir": 60},
            {"modele": "Venga", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
            {"modele": "Optima", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
            ],

            "Kia GT": [
            # ... autres modèles précédemment listés ...

            # Modèles sportifs / GT
            {"modele": "Stinger", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            # berline sportive / GT
            {"modele": "Forte GT", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
            # compacte sportive
            {"modele": "K5 GT", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
            # berline moyenne sportive
            {"modele": "EV6 GT", "variante": None, "portes": 5, "places": 5, "reservoir": 0},
            # crossover électrique GT, réservoir = 0
            ],

            "Koenigsegg": [
            # Modèles historiques et premiers prototypes
            {"modele": "CC", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
            {"modele": "CC8S", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
            {"modele": "CCR", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
            {"modele": "CCX", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "CCXR", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "CCXR Trevita", "variante": None, "portes": 2, "places": 2, "reservoir": 75},

            # Modèles modernes
            {"modele": "Agera", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "Agera R", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "Agera RS", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "Regera", "variante": None, "portes": 2, "places": 2, "reservoir": 80},

            # Modèles récents / hypercars
            {"modele": "Jesko", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Jesko Absolut", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Gemera", "variante": None, "portes": 4, "places": 4, "reservoir": 80},  # 4 places hybride
            {"modele": "Fajer", "variante": None, "portes": 2, "places": 2, "reservoir": 75},  # Concept récent

            # Modèles spéciaux / éditions limitées
            {"modele": "One:1", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            {"modele": "CC850", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
            ],
            "Lamborghini": [
            # Modèles historiques classiques
            {"modele": "350 GT", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
            {"modele": "400 GT", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
            {"modele": "Miura", "variante": None, "portes": 2, "places": 2, "reservoir": 85},
            {"modele": "Espada", "variante": None, "portes": 4, "places": 4, "reservoir": 95},
            {"modele": "Islero", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
            {"modele": "Jarama", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
            {"modele": "Urraco", "variante": None, "portes": 2, "places": 2, "reservoir": 70},

            # Modèles des années 80-90
            {"modele": "Countach", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Jalpa", "variante": None, "portes": 2, "places": 2, "reservoir": 85},

            # Modèles modernes des années 2000+
            {"modele": "Murciélago", "variante": None, "portes": 2, "places": 2, "reservoir": 100},
            {"modele": "Gallardo", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Reventón", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Aventador", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            {"modele": "Huracán", "variante": None, "portes": 2, "places": 2, "reservoir": 83},

            # Éditions spéciales et récentes
            {"modele": "Sian", "variante": None, "portes": 2, "places": 2, "reservoir": 83},  # hybride
            {"modele": "Essenza SCV12", "variante": None, "portes": 2, "places": 1, "reservoir": 90},  # circuit
            {"modele": "Revuelto", "variante": None, "portes": 2, "places": 2, "reservoir": 83},  # hybride récent
            {"modele": "Countach LPI 800‑4", "variante": None, "portes": 2, "places": 2, "reservoir": 83},
            # réédition moderne

            # SUV Lamborghini
            {"modele": "Urus", "variante": None, "portes": 5, "places": 5, "reservoir": 85},  # SUV luxe performant
            ],

            "Lancia": [
            # Modèles classiques / historiques
            {"modele": "Lambda", "variante": None, "portes": 4, "places": 4, "reservoir": 60},
            {"modele": "Augusta", "variante": None, "portes": 4, "places": 4, "reservoir": 60},
            {"modele": "Aprilia", "variante": None, "portes": 4, "places": 4, "reservoir": 60},
            {"modele": "Ardea", "variante": None, "portes": 4, "places": 4, "reservoir": 55},
            {"modele": "Aurelia", "variante": None, "portes": 4, "places": 4, "reservoir": 65},
            {"modele": "Flaminia", "variante": None, "portes": 4, "places": 4, "reservoir": 70},
            {"modele": "Fulvia", "variante": None, "portes": 2, "places": 4, "reservoir": 50},
            {"modele": "Beta", "variante": None, "portes": 2, "places": 4, "reservoir": 55},

            # Modèles des années 80-90
            {"modele": "Delta", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
            {"modele": "Prisma", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
            {"modele": "Thema", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
            {"modele": "Dedra", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
            {"modele": "Kappa", "variante": None, "portes": 4, "places": 5, "reservoir": 65},

            # Modèles récents / modernes
            {"modele": "Ypsilon", "variante": None, "portes": 5, "places": 5, "reservoir": 40},
            {"modele": "Delta HF Integrale", "variante": None, "portes": 3, "places": 4, "reservoir": 55},
            # rallye légendaire
            {"modele": "Stratos", "variante": None, "portes": 2, "places": 2, "reservoir": 60},  # rallye iconique
            {"modele": "Flavia", "variante": None, "portes": 4, "places": 4, "reservoir": 60},

            # Edition spéciales / variantes
            {"modele": "Delta S4", "variante": None, "portes": 3, "places": 4, "reservoir": 55},  # rallye
            {"modele": "Hyena", "variante": None, "portes": 2, "places": 2, "reservoir": 50},  # concept rare
            ],

            "Lotus Exige": [
            # Générations historiques / anciens
            {"modele": "Exige 1.8 192ch", "variante": None, "portes": 2, "places": 2, "annees": "2004–2008"},
            {"modele": "Exige S Pack 240", "variante": "240 S Pack", "portes": 2, "places": 2,
             "annees": "2008–2011"},
            {"modele": "Exige 3.5 V6 S", "variante": None, "portes": 2, "places": 2, "annees": "2011–2016"},

            # Variantes Series 3 / modernes
            {"modele": "Exige Sport 350", "variante": None, "portes": 2, "places": 2, "annees": "2016–2023"},
            {"modele": "Exige Sport 380", "variante": None, "portes": 2, "places": 2, "annees": "2016–2023"},
            {"modele": "Exige Sport 410", "variante": None, "portes": 2, "places": 2, "annees": "2018–2023"},
            {"modele": "Exige Cup 380", "variante": "Cup", "portes": 2, "places": 2, "annees": "2016–2023"},
            {"modele": "Exige Cup 430", "variante": "Cup", "portes": 2, "places": 2, "annees": "2017–2023"},
            {"modele": "Exige V6 350 SE", "variante": "Special Edition", "portes": 2, "places": 2,
             "annees": "2016"},
            ],

            "Maybach": [
            # Modèles historiques / anciens
            {"modele": "Maybach DS7 Zeppelin", "variante": "Limousine", "portes": 4, "places": 5,
             "annees": "1928–1938"},
            {"modele": "Maybach DS8 Zeppelin", "variante": "Limousine", "portes": 4, "places": 5,
             "annees": "1930–1938"},

            # Modèles modernes produits après la renaissance de la marque
            {"modele": "Maybach 57", "variante": None, "portes": 4, "places": 5, "annees": "2002–2012"},
            {"modele": "Maybach 57 S", "variante": "Spezial", "portes": 4, "places": 5, "annees": "2005–2012"},
            {"modele": "Maybach 57 Zeppelin", "variante": "Zeppelin Edition", "portes": 4, "places": 5,
             "annees": "2009–2012"},
            {"modele": "Maybach 62", "variante": None, "portes": 4, "places": 5, "annees": "2002–2012"},
            {"modele": "Maybach 62 S", "variante": "Sport", "portes": 4, "places": 5, "annees": "2005–2012"},
            {"modele": "Maybach 62 Zeppelin", "variante": "Zeppelin Edition", "portes": 4, "places": 5,
             "annees": "2009–2012"},

            # Modèles contemporains / Mercedes‑Maybach
            {"modele": "Mercedes‑Maybach S 580", "variante": None, "portes": 4, "places": 5,
             "annees": "2020–présent"},
            {"modele": "Mercedes‑Maybach S 580 e", "variante": "Hybride rechargeable", "portes": 4, "places": 5,
             "annees": "2023–présent"},
            {"modele": "Mercedes‑Maybach S 680", "variante": None, "portes": 4, "places": 5,
             "annees": "2020–présent"},
            {"modele": "Mercedes‑Maybach GLS 600", "variante": None, "portes": 5, "places": 7,
             "annees": "2020–présent"},
            {"modele": "Mercedes‑Maybach EQS SUV 680", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2026–présent"},
            {"modele": "Mercedes‑Maybach SL 680 Monogram Series", "variante": "Série spéciale", "portes": 2,
             "places": 2, "annees": "2025–présent"},
            {"modele": "Mercedes‑Maybach S 680 Edition 100", "variante": "Édition anniversaire", "portes": 4,
             "places": 5, "annees": "2021–2022"},
            {"modele": "Mercedes‑Maybach S 680 Edition Emerald Isle", "variante": "Édition limitée", "portes": 4,
             "places": 5, "annees": "2025"},
            ],

            "Mercedes-Benz": [
            # Modèles historiques / anciens
            {"modele": "300 SL Gullwing", "variante": None, "portes": 2, "places": 2, "annees": "1954–1963"},
            {"modele": "190 SL", "variante": None, "portes": 2, "places": 2, "annees": "1955–1963"},
            {"modele": "W108 / W109", "variante": None, "portes": 4, "places": 5, "annees": "1965–1972"},
            {"modele": "W111 / W112", "variante": None, "portes": 4, "places": 5, "annees": "1959–1971"},
            {"modele": "G-Class W460", "variante": None, "portes": 3, "places": 5, "annees": "1979–1990"},
            {"modele": "G-Class W463", "variante": None, "portes": 5, "places": 5, "annees": "1990–présent"},

            # Modèles récents / contemporains
            {"modele": "A-Class", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},
            {"modele": "B-Class", "variante": None, "portes": 5, "places": 5, "annees": "2011–présent"},
            {"modele": "C-Class", "variante": None, "portes": 4, "places": 5, "annees": "2014–présent"},
            {"modele": "E-Class", "variante": None, "portes": 4, "places": 5, "annees": "2016–présent"},
            {"modele": "S-Class", "variante": None, "portes": 4, "places": 5, "annees": "2013–présent"},
            {"modele": "CLA", "variante": None, "portes": 4, "places": 5, "annees": "2013–présent"},
            {"modele": "CLS", "variante": None, "portes": 4, "places": 5, "annees": "2011–présent"},
            {"modele": "GLA", "variante": None, "portes": 5, "places": 5, "annees": "2014–présent"},
            {"modele": "GLC", "variante": None, "portes": 5, "places": 5, "annees": "2015–présent"},
            {"modele": "GLE", "variante": None, "portes": 5, "places": 5, "annees": "2015–présent"},
            {"modele": "GLS", "variante": None, "portes": 5, "places": 7, "annees": "2016–présent"},
            {"modele": "EQC", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2019–présent"},
            {"modele": "EQS", "variante": "Berline électrique", "portes": 4, "places": 5, "annees": "2021–présent"},
            {"modele": "EQB", "variante": "SUV électrique", "portes": 5, "places": 5, "annees": "2021–présent"},
            {"modele": "EQE SUV", "variante": "SUV électrique", "portes": 5, "places": 5, "annees": "2022–présent"},
            {"modele": "EQA", "variante": "SUV électrique", "portes": 5, "places": 5, "annees": "2021–présent"},
            ],

            "Mitsubishi": [
            # Modèles historiques / anciens
            {"modele": "Mitsubishi 500", "variante": None, "portes": 2, "places": 4, "annees": "1960–1962"},
            {"modele": "Mitsubishi Colt 800", "variante": None, "portes": 2, "places": 4, "annees": "1965–1971"},
            {"modele": "Mitsubishi Galant", "variante": None, "portes": 4, "places": 5, "annees": "1969–2012"},
            {"modele": "Mitsubishi Lancer", "variante": None, "portes": 4, "places": 5, "annees": "1973–2017"},
            {"modele": "Mitsubishi Pajero", "variante": None, "portes": 5, "places": 7, "annees": "1982–2021"},
            {"modele": "Mitsubishi Eclipse", "variante": None, "portes": 2, "places": 4, "annees": "1989–2011"},
            {"modele": "Mitsubishi 3000GT", "variante": None, "portes": 2, "places": 2, "annees": "1990–2001"},
            {"modele": "Mitsubishi Starion", "variante": None, "portes": 2, "places": 2, "annees": "1982–1989"},

            # Modèles récents / modernes
            {"modele": "Mitsubishi Outlander", "variante": None, "portes": 5, "places": 7,
             "annees": "2001–présent"},
            {"modele": "Mitsubishi Outlander PHEV", "variante": "Hybride rechargeable", "portes": 5, "places": 5,
             "annees": "2013–présent"},
            {"modele": "Mitsubishi ASX", "variante": None, "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "Mitsubishi Eclipse Cross", "variante": None, "portes": 5, "places": 5,
             "annees": "2017–présent"},
            {"modele": "Mitsubishi Mirage", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},
            {"modele": "Mitsubishi i-MiEV", "variante": "Électrique", "portes": 3, "places": 4,
             "annees": "2009–2017"},
            {"modele": "Mitsubishi L200", "variante": None, "portes": 4, "places": 5, "annees": "1978–présent"},
            {"modele": "Mitsubishi Triton", "variante": None, "portes": 4, "places": 5, "annees": "1996–présent"}

            ],

            "Mitsubishi Evo": [
            {"modele": "Mitsubishi Lancer Evolution", "variante": None, "portes": 4, "places": 5, "annees": "1992–2016"}
            ],

            "Nissan": [
            # Modèles historiques / anciens
            {"modele": "Fairlady Z (S30)", "variante": None, "portes": 2, "places": 2, "annees": "1969–1978"},
            {"modele": "300ZX (Z31)", "variante": None, "portes": 2, "places": 2, "annees": "1984–1989"},
            {"modele": "350Z", "variante": None, "portes": 2, "places": 2, "annees": "2002–2009"},
            # sport coupé/roadster :contentReference[oaicite:0]{index=0}
            {"modele": "370Z", "variante": None, "portes": 2, "places": 2, "annees": "2008–2021"},
            # sport :contentReference[oaicite:1]{index=1}
            {"modele": "Bluebird", "variante": None, "portes": 4, "places": 5, "annees": "1955–2001"},
            # compacte historique :contentReference[oaicite:2]{index=2}

            # Berlines / compactes
            {"modele": "Micra", "variante": None, "portes": 5, "places": 5, "annees": "1982–présent"},
            {"modele": "Sentra", "variante": None, "portes": 4, "places": 5, "annees": "2000–présent"},
            {"modele": "Altima", "variante": None, "portes": 4, "places": 5, "annees": "1992–présent"},
            {"modele": "Maxima", "variante": None, "portes": 4, "places": 5, "annees": "1981–2023"},
            # produit jusqu’en 2023 :contentReference[oaicite:3]{index=3}

            # SUV / crossovers
            {"modele": "Juke", "variante": None, "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "Qashqai", "variante": None, "portes": 5, "places": 5, "annees": "2006–présent"},
            {"modele": "X‑Trail", "variante": None, "portes": 5, "places": 5, "annees": "2001–présent"},
            {"modele": "Murano", "variante": None, "portes": 5, "places": 5, "annees": "2002–présent"},
            {"modele": "Pathfinder", "variante": None, "portes": 5, "places": 7, "annees": "1986–présent"},
            {"modele": "Kicks", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},

            # Électriques / hybrides
            {"modele": "Leaf", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "Ariya", "variante": "SUV électrique", "portes": 5, "places": 5, "annees": "2022–présent"},

            # Pickup / utilitaires
            {"modele": "Navara", "variante": None, "portes": 4, "places": 5, "annees": "1997–présent"},
            {"modele": "NP300 Frontier", "variante": None, "portes": 4, "places": 5, "annees": "2005–présent"},

            # Monospaces / utilitaires légers
            {"modele": "e‑NV200", "variante": "Électrique utilitaire", "portes": 5, "places": 5,
             "annees": "2014–présent"},
            ],

            "Nissan Nismo": [
            # Sportives et Nismo
            {"modele": "370Z Nismo", "variante": None, "portes": 2, "places": 2, "annees": "2009–2021"},
            {"modele": "GT-R Nismo", "variante": None, "portes": 2, "places": 2, "annees": "2009–présent"},
            {"modele": "Juke Nismo", "variante": None, "portes": 5, "places": 5, "annees": "2013–2019"},
            {"modele": "Juke Nismo RS", "variante": "RS", "portes": 5, "places": 5, "annees": "2013–2019"},
            {"modele": "Note Nismo", "variante": None, "portes": 5, "places": 5, "annees": "2011–2019"},
            {"modele": "Note Nismo S", "variante": "S", "portes": 5, "places": 5, "annees": "2014–2019"},
            {"modele": "March/Micra Nismo", "variante": None, "portes": 5, "places": 5, "annees": "2013–2020"},
            {"modele": "Micra Nismo S", "variante": "S", "portes": 5, "places": 5, "annees": "2017–2020"},
            {"modele": "370Z Nismo Roadster", "variante": "Roadster", "portes": 2, "places": 2,
             "annees": "2010–2021"},
            {"modele": "GT-R Nismo Special Edition", "variante": "Special Edition", "portes": 2, "places": 2,
             "annees": "2015–présent"},
            ],

            "Pagani": [
            # Modèles historiques / premiers
            {"modele": "Pagani Zonda C12", "variante": None, "portes": 2, "places": 2, "annees": "1999–2002"},
            {"modele": "Pagani Zonda S", "variante": None, "portes": 2, "places": 2, "annees": "2002–2005"},
            {"modele": "Pagani Zonda F", "variante": None, "portes": 2, "places": 2, "annees": "2005–2011"},
            {"modele": "Pagani Zonda Roadster", "variante": None, "portes": 2, "places": 2, "annees": "2002–2011"},
            {"modele": "Pagani Zonda Cinque", "variante": None, "portes": 2, "places": 2, "annees": "2009–2010"},
            {"modele": "Pagani Zonda Tricolore", "variante": None, "portes": 2, "places": 2, "annees": "2010"},

            # Modèles récents / modernes
            {"modele": "Pagani Huayra", "variante": None, "portes": 2, "places": 2, "annees": "2012–2018"},
            {"modele": "Pagani Huayra BC", "variante": None, "portes": 2, "places": 2, "annees": "2016–présent"},
            {"modele": "Pagani Huayra Roadster", "variante": None, "portes": 2, "places": 2,
             "annees": "2012–présent"},
            {"modele": "Pagani Huayra Roadster BC", "variante": None, "portes": 2, "places": 2,
             "annees": "2019–présent"},
            {"modele": "Pagani Huayra R", "variante": None, "portes": 2, "places": 2, "annees": "2021–présent"},

            # Nouveau modèle hypercar
            {"modele": "Pagani Utopia", "variante": None, "portes": 2, "places": 2, "annees": "2023–présent"},
            ],

            "Peugeot": [
            # Modèles historiques / anciens
            {"modele": "Peugeot 201", "variante": None, "portes": 4, "places": 5, "annees": "1929–1937"},
            {"modele": "Peugeot 202", "variante": None, "portes": 4, "places": 5, "annees": "1938–1949"},
            {"modele": "Peugeot 203", "variante": None, "portes": 4, "places": 5, "annees": "1948–1960"},
            {"modele": "Peugeot 204", "variante": None, "portes": 4, "places": 5, "annees": "1965–1976"},
            {"modele": "Peugeot 205", "variante": None, "portes": 3, "places": 5, "annees": "1983–1998"},
            {"modele": "Peugeot 206", "variante": None, "portes": 3, "places": 5, "annees": "1998–2010"},
            {"modele": "Peugeot 207", "variante": None, "portes": 3, "places": 5, "annees": "2006–2014"},

            # Berlines et compactes récentes
            {"modele": "Peugeot 208", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},
            {"modele": "Peugeot 308", "variante": None, "portes": 5, "places": 5, "annees": "2007–présent"},
            {"modele": "Peugeot 408", "variante": None, "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "Peugeot 508", "variante": None, "portes": 4, "places": 5, "annees": "2010–présent"},

            # SUV / crossovers
            {"modele": "Peugeot 2008", "variante": None, "portes": 5, "places": 5, "annees": "2013–présent"},
            {"modele": "Peugeot 3008", "variante": None, "portes": 5, "places": 5, "annees": "2007–présent"},
            {"modele": "Peugeot 5008", "variante": None, "portes": 5, "places": 7, "annees": "2009–présent"},
            {"modele": "Peugeot 4007", "variante": None, "portes": 5, "places": 7, "annees": "2007–2012"},

            # Monospaces / utilitaires légers
            {"modele": "Peugeot Expert", "variante": None, "portes": 4, "places": 3, "annees": "1995–présent"},
            {"modele": "Peugeot Traveller", "variante": None, "portes": 5, "places": 8, "annees": "2016–présent"},

            # Électriques / hybrides
            {"modele": "Peugeot e-208", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2019–présent"},
            {"modele": "Peugeot e-2008", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2020–présent"},
            {"modele": "Peugeot e-Expert", "variante": "Électrique", "portes": 4, "places": 3,
             "annees": "2020–présent"},
            {"modele": "Peugeot e-Traveller", "variante": "Électrique", "portes": 5, "places": 8,
             "annees": "2020–présent"},
            ],

            "Radical": [
            # Modèles principaux / sportifs
            {"modele": "Radical SR1", "variante": None, "portes": 0, "places": 1, "annees": "2000–présent"},
            {"modele": "Radical SR3", "variante": None, "portes": 0, "places": 1, "annees": "2002–présent"},
            {"modele": "Radical SR8", "variante": None, "portes": 0, "places": 1, "annees": "2005–2015"},
            {"modele": "Radical SR10", "variante": None, "portes": 0, "places": 1, "annees": "2009–présent"},
            {"modele": "Radical RXC", "variante": None, "portes": 2, "places": 2, "annees": "2013–présent"},
            {"modele": "Radical RXC Turbo", "variante": "Turbo", "portes": 2, "places": 2,
             "annees": "2015–présent"},
            {"modele": "Radical SR3 RSX", "variante": "RSX", "portes": 0, "places": 1, "annees": "2012–présent"},

            # Modèles récents / hypercars de piste
            {"modele": "Radical SR1 Cup", "variante": "Cup", "portes": 0, "places": 1, "annees": "2000–présent"},
            {"modele": "Radical SR3 SL", "variante": "SL", "portes": 0, "places": 1, "annees": "2005–présent"},
            {"modele": "Radical RXC Spyder", "variante": "Spyder", "portes": 2, "places": 2,
             "annees": "2014–présent"},
            ],

            "Rimac": [
            # Modèles principaux / supercars électriques
            {"modele": "Rimac Concept One", "variante": None, "portes": 2, "places": 2, "annees": "2011–2013"},
            {"modele": "Rimac Concept S", "variante": None, "portes": 2, "places": 2, "annees": "2016–présent"},
            {"modele": "Rimac C_Two", "variante": None, "portes": 2, "places": 2, "annees": "2018–présent"},
            {"modele": "Rimac Nevera", "variante": None, "portes": 2, "places": 2, "annees": "2021–présent"},

            # Versions limitées / spéciales
            {"modele": "Rimac Concept One Alpha", "variante": "Alpha", "portes": 2, "places": 2,
             "annees": "2012–2013"},
            ],

            "SAIPA": [
            # Modèles historiques / anciens
            {"modele": "SAIPA 141", "variante": None, "portes": 4, "places": 5, "annees": "1994–2010"},
            {"modele": "SAIPA 132", "variante": None, "portes": 4, "places": 5, "annees": "2000–2010"},

            # Modèles populaires / récents
            {"modele": "SAIPA Pride", "variante": None, "portes": 4, "places": 5, "annees": "1992–présent"},
            {"modele": "SAIPA Saina", "variante": None, "portes": 4, "places": 5, "annees": "2016–présent"},
            {"modele": "SAIPA Quick", "variante": None, "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "SAIPA Aria", "variante": None, "portes": 4, "places": 5, "annees": "2020–présent"},

            # Véhicules utilitaires légers
            {"modele": "SAIPA 151", "variante": None, "portes": 2, "places": 3, "annees": "2000–présent"},
            ],



            "Skoda": [
            # Modèles historiques / anciens
            {"modele": "Škoda Popular", "variante": None, "portes": 4, "places": 5, "annees": "1934–1946"},
            {"modele": "Škoda Rapid", "variante": None, "portes": 4, "places": 5, "annees": "1935–1947"},
            {"modele": "Škoda Octavia", "variante": None, "portes": 4, "places": 5, "annees": "1959–1971"},
            {"modele": "Škoda Felicia", "variante": None, "portes": 2, "places": 4, "annees": "1959–1964"},

            # Modèles récents / berlines et compactes
            {"modele": "Škoda Fabia", "variante": None, "portes": 5, "places": 5, "annees": "1999–présent"},
            {"modele": "Škoda Octavia", "variante": None, "portes": 5, "places": 5, "annees": "1996–présent"},
            {"modele": "Škoda Superb", "variante": None, "portes": 4, "places": 5, "annees": "1934–présent"},

            # SUV / crossovers
            {"modele": "Škoda Kodiaq", "variante": None, "portes": 5, "places": 7, "annees": "2016–présent"},
            {"modele": "Škoda Karoq", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
            {"modele": "Škoda Kamiq", "variante": None, "portes": 5, "places": 5, "annees": "2019–présent"},
            {"modele": "Škoda Enyaq iV", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2020–présent"},

            # Sportives / Edition spéciale
            {"modele": "Škoda Octavia RS", "variante": "RS", "portes": 5, "places": 5, "annees": "2000–présent"},
            {"modele": "Škoda Fabia RS", "variante": "RS", "portes": 5, "places": 5, "annees": "2003–présent"},
            ],

            "Subaru": [
            # Modèles historiques / anciens
            {"modele": "Subaru 360", "variante": None, "portes": 2, "places": 4, "annees": "1958–1971"},
            {"modele": "Subaru Leone", "variante": None, "portes": 4, "places": 5, "annees": "1971–1994"},

            # Modèles populaires / berlines et compactes
            {"modele": "Subaru Impreza", "variante": None, "portes": 5, "places": 5, "annees": "1992–présent"},
            {"modele": "Subaru Legacy", "variante": None, "portes": 4, "places": 5, "annees": "1989–présent"},
            {"modele": "Subaru Outback", "variante": None, "portes": 5, "places": 5, "annees": "1994–présent"},

            # SUV / crossovers
            {"modele": "Subaru Forester", "variante": None, "portes": 5, "places": 5, "annees": "1997–présent"},
            {"modele": "Subaru XV", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},

            # Sportives / rallye
            {"modele": "Subaru WRX", "variante": None, "portes": 4, "places": 5, "annees": "1992–présent"},
            {"modele": "Subaru WRX STI", "variante": "STI", "portes": 4, "places": 5, "annees": "1994–présent"},

            # Compactes et électriques / hybrides
            {"modele": "Subaru Solterra", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2022–présent"},
            ],
            "Subaru STI": [
            # Modèles sportives / rallye
            {"modele": "Subaru Impreza WRX STI", "variante": "STI", "portes": 4, "places": 5,
             "annees": "1994–présent"},
            {"modele": "Subaru WRX STI", "variante": "STI", "portes": 4, "places": 5, "annees": "2014–présent"},

            # Éditions spéciales
            {"modele": "Subaru WRX STI S209", "variante": "S209", "portes": 4, "places": 5, "annees": "2019"},
            {"modele": "Subaru WRX STI Type RA", "variante": "Type RA", "portes": 4, "places": 5, "annees": "2021"},
            ],
            "Suzuki": [
            # Modèles historiques / anciens
            {"modele": "Suzuki LJ10", "variante": None, "portes": 2, "places": 4, "annees": "1970–1972"},
            {"modele": "Suzuki LJ50", "variante": None, "portes": 2, "places": 4, "annees": "1972–1981"},
            {"modele": "Suzuki Alto", "variante": None, "portes": 3, "places": 4, "annees": "1979–présent"},
            {"modele": "Suzuki Swift", "variante": None, "portes": 3, "places": 5, "annees": "1983–présent"},

            # SUV / 4x4
            {"modele": "Suzuki Vitara", "variante": None, "portes": 3, "places": 5, "annees": "1988–présent"},
            {"modele": "Suzuki Grand Vitara", "variante": None, "portes": 5, "places": 5, "annees": "1998–2019"},
            {"modele": "Suzuki Jimny", "variante": None, "portes": 3, "places": 4, "annees": "1968–présent"},

            # Compactes et berlines
            {"modele": "Suzuki Celerio", "variante": None, "portes": 5, "places": 5, "annees": "2008–présent"},
            {"modele": "Suzuki Baleno", "variante": None, "portes": 5, "places": 5, "annees": "1995–présent"},

            # Sportives / édition spéciale
            {"modele": "Suzuki Swift Sport", "variante": "Sport", "portes": 3, "places": 4,
             "annees": "2005–présent"},

            # Électriques / hybrides
            {"modele": "Suzuki Across", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2020–présent"},
            {"modele": "Suzuki Solio", "variante": "Hybride", "portes": 5, "places": 5, "annees": "1999–présent"},
            ],

            "TVR": [
            # Modèles historiques / anciens
            {"modele": "TVR Grantura", "variante": None, "portes": 2, "places": 2, "annees": "1958–1967"},
            {"modele": "TVR Vixen", "variante": None, "portes": 2, "places": 2, "annees": "1967–1973"},
            {"modele": "TVR Tuscan", "variante": None, "portes": 2, "places": 2, "annees": "1967–1971"},
            {"modele": "TVR Chimaera", "variante": None, "portes": 2, "places": 2, "annees": "1992–2003"},

            # Modèles récents / sportives
            {"modele": "TVR Griffith", "variante": None, "portes": 2, "places": 2, "annees": "1991–2002"},
            {"modele": "TVR Cerbera", "variante": None, "portes": 2, "places": 2, "annees": "1996–2006"},
            {"modele": "TVR Sagaris", "variante": None, "portes": 2, "places": 2, "annees": "2005–2006"},

            # Modèles très récents / revival
            {"modele": "TVR Griffith (2020)", "variante": None, "portes": 2, "places": 2, "annees": "2020–présent"},
            {"modele": "TVR Tuscan (2021)", "variante": None, "portes": 2, "places": 2, "annees": "2021–présent"},
            ],

            "Triumph": [
            # Modèles historiques / anciens
            {"modele": "Triumph TR2", "variante": None, "portes": 2, "places": 2, "annees": "1953–1955"},
            {"modele": "Triumph TR3", "variante": None, "portes": 2, "places": 2, "annees": "1955–1962"},
            {"modele": "Triumph TR4", "variante": None, "portes": 2, "places": 2, "annees": "1961–1965"},
            {"modele": "Triumph TR5", "variante": None, "portes": 2, "places": 2, "annees": "1967–1968"},
            {"modele": "Triumph TR6", "variante": None, "portes": 2, "places": 2, "annees": "1968–1976"},

            # Roadsters et coupés populaires
            {"modele": "Triumph Spitfire", "variante": None, "portes": 2, "places": 2, "annees": "1962–1980"},
            {"modele": "Triumph Herald", "variante": None, "portes": 2, "places": 4, "annees": "1959–1971"},
            {"modele": "Triumph Stag", "variante": None, "portes": 2, "places": 4, "annees": "1970–1978"},

            # Berlines et compactes
            {"modele": "Triumph Dolomite", "variante": None, "portes": 4, "places": 5, "annees": "1972–1980"},
            {"modele": "Triumph Toledo", "variante": None, "portes": 4, "places": 5, "annees": "1970–1976"},

            # Modèles récents / revival (si applicable)
            {"modele": "Triumph TR25", "variante": None, "portes": 2, "places": 2, "annees": "années 1980"},
            ],

            "Toyota": [
            # Modèles historiques / anciens
            {"modele": "Toyota Land Cruiser 20", "variante": None, "portes": 2, "places": 4, "annees": "1955–1960"},
            {"modele": "Toyota Land Cruiser 40", "variante": None, "portes": 2, "places": 4, "annees": "1960–1984"},
            {"modele": "Toyota Corona", "variante": None, "portes": 4, "places": 5, "annees": "1957–2001"},
            {"modele": "Toyota Celica", "variante": None, "portes": 2, "places": 4, "annees": "1970–2006"},

            # Compactes / berlines
            {"modele": "Toyota Corolla", "variante": None, "portes": 4, "places": 5, "annees": "1966–présent"},
            {"modele": "Toyota Yaris", "variante": None, "portes": 5, "places": 5, "annees": "1999–présent"},
            {"modele": "Toyota Prius", "variante": None, "portes": 5, "places": 5, "annees": "1997–présent"},

            # SUV / crossovers
            {"modele": "Toyota RAV4", "variante": None, "portes": 5, "places": 5, "annees": "1994–présent"},
            {"modele": "Toyota Highlander", "variante": None, "portes": 5, "places": 7, "annees": "2000–présent"},
            {"modele": "Toyota C-HR", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},

            # Pickups
            {"modele": "Toyota Hilux", "variante": None, "portes": 2, "places": 4, "annees": "1968–présent"},

            # Sportives / éditions spéciales
            {"modele": "Toyota Supra", "variante": None, "portes": 2, "places": 2,
             "annees": "1978–2002, 2019–présent"},
            {"modele": "Toyota GR Yaris", "variante": "GR", "portes": 3, "places": 4, "annees": "2020–présent"},

            # Électriques / hybrides
            {"modele": "Toyota bZ4X", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2022–présent"},
            ],

            "Tesla": [
            # Modèles historiques / premiers
            {"modele": "Tesla Roadster", "variante": None, "portes": 2, "places": 2, "annees": "2008–2012"},

            # Berlines
            {"modele": "Tesla Model S", "variante": None, "portes": 4, "places": 5, "annees": "2012–présent"},
            {"modele": "Tesla Model 3", "variante": None, "portes": 4, "places": 5, "annees": "2017–présent"},

            # SUV / crossovers
            {"modele": "Tesla Model X", "variante": None, "portes": 5, "places": 7, "annees": "2015–présent"},
            {"modele": "Tesla Model Y", "variante": None, "portes": 5, "places": 7, "annees": "2020–présent"},

            # Futures / concepts
            {"modele": "Tesla Cybertruck", "variante": None, "portes": 4, "places": 6, "annees": "2023–présent"},
            {"modele": "Tesla Semi", "variante": None, "portes": 2, "places": 3, "annees": "2023–présent"},
            ],

            "Tesla Performance": [
            # Versions haute performance
            {"modele": "Tesla Model S Plaid", "variante": "Performance", "portes": 4, "places": 5,
             "annees": "2021–présent"},
            {"modele": "Tesla Model 3 Performance", "variante": "Performance", "portes": 4, "places": 5,
             "annees": "2018–présent"},
            {"modele": "Tesla Model X Plaid", "variante": "Performance", "portes": 5, "places": 7,
             "annees": "2021–présent"},
            {"modele": "Tesla Model Y Performance", "variante": "Performance", "portes": 5, "places": 7,
             "annees": "2020–présent"},
            ],
            "Toyota GR": [
            # Sportives / haute performance
            {"modele": "Toyota GR Supra", "variante": "GR", "portes": 2, "places": 2, "annees": "2019–présent"},
            {"modele": "Toyota GR Yaris", "variante": "GR", "portes": 3, "places": 4, "annees": "2020–présent"},
            {"modele": "Toyota GR86", "variante": "GR", "portes": 2, "places": 4, "annees": "2021–présent"},
            {"modele": "Toyota GR Corolla", "variante": "GR", "portes": 5, "places": 5, "annees": "2022–présent"},
            ],

            "Venturi": [
            # Modèles historiques / anciens
            {"modele": "Venturi 260", "variante": None, "portes": 2, "places": 2, "annees": "1984–1994"},
            {"modele": "Venturi 400 GT", "variante": None, "portes": 2, "places": 2, "annees": "1992–1995"},
            {"modele": "Venturi Atlantique", "variante": None, "portes": 2, "places": 2, "annees": "1991–2000"},

            # Modèles récents / électriques
            {"modele": "Venturi Fétish", "variante": None, "portes": 2, "places": 2, "annees": "2004–2013"},
            {"modele": "Venturi Buckeye Bullet", "variante": None, "portes": 2, "places": 2,
             "annees": "2010–présent"},
            {"modele": "Venturi VBB-3", "variante": None, "portes": 2, "places": 1, "annees": "2016–présent"},
            ],
            "VinFast": [
            # Modèles récents / voitures particulières
            {"modele": "VinFast Lux A2.0", "variante": None, "portes": 4, "places": 5, "annees": "2018–2022"},
            {"modele": "VinFast Lux SA2.0", "variante": None, "portes": 5, "places": 7, "annees": "2018–2022"},
            {"modele": "VinFast Fadil", "variante": None, "portes": 5, "places": 5, "annees": "2019–2022"},

            # Modèles électriques récents
            {"modele": "VinFast VF e34", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2021–présent"},
            {"modele": "VinFast VF 5", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2022–présent"},
            {"modele": "VinFast VF 6", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2022–présent"},
            {"modele": "VinFast VF 8", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2022–présent"},
            {"modele": "VinFast VF 9", "variante": "Électrique", "portes": 5, "places": 7,
             "annees": "2022–présent"},
            ],

            "Volvo": [
            # Modèles historiques / anciens
            {"modele": "Volvo PV444", "variante": None, "portes": 2, "places": 4, "annees": "1947–1958"},
            {"modele": "Volvo PV544", "variante": None, "portes": 2, "places": 5, "annees": "1958–1965"},
            {"modele": "Volvo Amazon", "variante": None, "portes": 4, "places": 5, "annees": "1956–1970"},

            # Berlines / compactes
            {"modele": "Volvo 140", "variante": None, "portes": 4, "places": 5, "annees": "1966–1974"},
            {"modele": "Volvo 240", "variante": None, "portes": 4, "places": 5, "annees": "1974–1993"},
            {"modele": "Volvo 340", "variante": None, "portes": 3, "places": 5, "annees": "1976–1991"},
            {"modele": "Volvo 360", "variante": None, "portes": 4, "places": 5, "annees": "1982–1991"},

            # Modèles récents / berlines et SUV
            {"modele": "Volvo S60", "variante": None, "portes": 4, "places": 5, "annees": "2000–présent"},
            {"modele": "Volvo S90", "variante": None, "portes": 4, "places": 5, "annees": "2016–présent"},
            {"modele": "Volvo V40", "variante": None, "portes": 5, "places": 5, "annees": "1995–2019"},
            {"modele": "Volvo V60", "variante": None, "portes": 5, "places": 5, "annees": "2010–présent"},
            {"modele": "Volvo V90", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},

            # SUV / crossovers
            {"modele": "Volvo XC40", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
            {"modele": "Volvo XC60", "variante": None, "portes": 5, "places": 5, "annees": "2008–présent"},
            {"modele": "Volvo XC90", "variante": None, "portes": 5, "places": 7, "annees": "2002–présent"},

            # Électriques / hybrides
            {"modele": "Volvo XC40 Recharge", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2020–présent"},
            {"modele": "Volvo C40 Recharge", "variante": "Électrique", "portes": 5, "places": 5,
             "annees": "2021–présent"},
            ],
            "Volkswagen": [
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
            ],

            "Volkswagen R": [
            # Sportives / performance
            {"modele": "Volkswagen Golf R", "variante": "R", "portes": 5, "places": 5, "annees": "2002–présent"},
            {"modele": "Volkswagen Tiguan R", "variante": "R", "portes": 5, "places": 5, "annees": "2019–présent"},
            {"modele": "Volkswagen Arteon R", "variante": "R", "portes": 5, "places": 5, "annees": "2020–présent"},
            {"modele": "Volkswagen Passat R-Line", "variante": "R-Line", "portes": 4, "places": 5,
             "annees": "2010–présent"},

            # Éditions limitées / spéciales
            {"modele": "Volkswagen Golf R32", "variante": "R32", "portes": 5, "places": 5, "annees": "2002–2005"},
            {"modele": "Volkswagen Golf R400", "variante": "R400", "portes": 3, "places": 4, "annees": "2014–2015"},
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
