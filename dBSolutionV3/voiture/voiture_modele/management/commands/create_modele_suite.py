from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque
from voiture.voiture_modele.models import VoitureModele


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


        marques_modeles = {
                # Italie
                "Range Rover": [
                    {"modele": "Range Rover", "variante": "Base / Vogue", "portes": 5, "places": 5, "reservoir": 82},
                    {"modele": "Range Rover", "variante": "Autobiography", "portes": 5, "places": 5, "reservoir": 82},
                    {"modele": "Range Rover", "variante": "SV Autobiography", "portes": 5, "places": 5, "reservoir": 82},
                    {"modele": "Range Rover", "variante": "SV Autobiography Dynamic", "portes": 5, "places": 5,
                     "reservoir": 82},
                    {"modele": "Range Rover", "variante": "Long Wheelbase (LWB)", "portes": 5, "places": 5,
                     "reservoir": 90},

                    {"modele": "Range Rover Sport", "variante": "S", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "SE", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "Dynamic SE", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "Dynamic HSE", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "Autobiography", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "SVR", "portes": 5, "places": 5, "reservoir": 85},
                    {"modele": "Range Rover Sport", "variante": "SV Carbon", "portes": 5, "places": 5, "reservoir": 85},

                    {"modele": "Range Rover Velar", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 80},
                    {"modele": "Range Rover Velar", "variante": "R‑Dynamic S", "portes": 5, "places": 5, "reservoir": 80},
                    {"modele": "Range Rover Velar", "variante": "R‑Dynamic SE", "portes": 5, "places": 5, "reservoir": 80},
                    {"modele": "Range Rover Velar", "variante": "R‑Dynamic HSE", "portes": 5, "places": 5, "reservoir": 80},

                    {"modele": "Range Rover Evoque", "variante": "S", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Range Rover Evoque", "variante": "Dynamic SE", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Range Rover Evoque", "variante": "Dynamic HSE", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Range Rover Evoque", "variante": "Autobiography", "portes": 5, "places": 5, "reservoir": 60},
                    # Modèles historiques / anciens
                    {"modele": "Range Rover Classic", "variante": None, "portes": 5, "places": 5, "annees": "1970–1996"},
                    {"modele": "Range Rover P38A", "variante": None, "portes": 5, "places": 5, "annees": "1994–2001"},
                    {"modele": "Range Rover L322", "variante": None, "portes": 5, "places": 5, "annees": "2001–2012"},
                    # 3e génération :
                    {"modele": "Range Rover SV Coupé", "variante": "édition limitée", "portes": 3, "places": 4,
                     "annees": "2018 (édition spéciale)"},
                    # (Petites variantes historiques, ex. éditions spéciales rares)
                    {"modele": "Range Rover SV Burford Edition", "variante": "édition ultra-rare", "portes": 5, "places": 5,
                     "annees": "édition limitée contemporaine"},

                    # Modèles récents / actuels
                    {"modele": "Range Rover L405", "variante": None, "portes": 5, "places": 5, "annees": "2012–2021"},
                    {"modele": "Range Rover L460", "variante": None, "portes": 5, "places": 5, "annees": "2022–présent"},
                    # 5e génération :contentReference[oaicite:1]{index=1}
                    {"modele": "Range Rover Velar", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    # SUV intermédiaire :contentReference[oaicite:2]{index=2}
                    {"modele": "Range Rover Sport", "variante": None, "portes": 5, "places": 5, "annees": "2005–présent"},
                    {"modele": "Range Rover SE", "variante": "Standard", "portes": 5, "places": 5,
                     "annees": "2025–présent"},  # versions modernes (exemple 2025) :contentReference[oaicite:3]{index=3}
                    {"modele": "Range Rover HSE", "variante": None, "portes": 5, "places": 5, "annees": "2025–présent"},
                    # version mieux équipée :contentReference[oaicite:4]{index=4}
                ],



                "Polestar": [
                    {"modele": "Polestar 1", "variante": "Standard", "portes": 2, "places": 4, "reservoir": 0},
                    {"modele": "Polestar 2", "variante": "Standard Range Single Motor", "portes": 5, "places": 5,
                     "reservoir": 0},
                    {"modele": "Polestar 2", "variante": "Long Range Single Motor", "portes": 5, "places": 5,
                     "reservoir": 0},
                    {"modele": "Polestar 2", "variante": "Long Range Dual Motor", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 2", "variante": "Long Range Dual Motor Performance", "portes": 5, "places": 5,
                     "reservoir": 0},
                    {"modele": "Polestar 3", "variante": "Base", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 3", "variante": "Dual Motor", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 3", "variante": "Performance", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 4", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 4", "variante": "Plus Pack", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 4", "variante": "Pilot Pack", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 5", "variante": "Dual Motor", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 5", "variante": "Performance", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Polestar 6", "variante": "Roadster Standard", "portes": 2, "places": 2, "reservoir": 0},
                    {"modele": "Polestar 7", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 0}
                ],

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
                    {"modele": "Peugeot 9X8", "variante": "PEUGEOT Hypercar 9X8", "portes": 2, "places": 2, "reservoir": 90},
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

                    {"modele": "550 Spyder", "variante": None, "portes": 2, "places": 2,
                     "reservoir": 60},

                    # 911 classiques
                    {"modele": "911", "variante": "Carrera S", "portes": 2, "places": 4,
                     "reservoir": 67},
                    {"modele": "911", "variante": "Turbo", "portes": 2, "places": 4,
                     "reservoir": 67},

                    # 911 GT spéciaux
                    {"modele": "911", "variante": "GT3", "portes": 2, "places": 2,
                     "reservoir": 64},
                    {"modele": "911", "variante": "GT3 RS", "portes": 2, "places": 2,
                     "reservoir": 64},
                    {"modele": "911", "variante": "GT2 RS", "portes": 2, "places": 2,
                     "reservoir": 64},

                    # SUV et berlines
                    {"modele": "Cayenne", "variante": "S", "portes": 5, "places": 5,
                    "reservoir": 75},
                    {"modele": "Macan", "variante": None, "portes": 5, "places": 5,
                     "reservoir": 60},
                    {"modele": "Panamera", "variante": "4S", "portes": 5, "places": 5,
                     "reservoir": 75},

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

                    {"modele": "Cayenne", "variante": None, "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "S", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "GTS", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "Turbo", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "Turbo GT", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "E-Hybrid", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "S E-Hybrid", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "Turbo E-Hybrid", "portes": 5, "places": 5, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "Coupe", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Cayenne", "variante": "Coupe Turbo", "portes": 5, "places": 4, "reservoir": 75},

                    {"modele": "Macan", "variante": None, "portes": 5, "nbre_places": 5, "reservoir": 60},
                    {"modele": "Macan", "variante": "T", "portes": 5, "nbre_places": 5, "reservoir": 60},
                    {"modele": "Macan", "variante": "S", "portes": 5, "nbre_places": 5, "reservoir": 60},
                    {"modele": "Macan", "variante": "GTS", "portes": 5, "nbre_places": 5, "reservoir": 60},

                    {"modele": "Panamera", "variante": None, "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "4", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "4S", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "GTS", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "Turbo", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "Turbo S", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "E-Hybrid", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "4 E-Hybrid", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "4S E-Hybrid", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "Turbo E-Hybrid", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "Sport Turismo", "portes": 5, "places": 4, "reservoir": 75},
                    {"modele": "Panamera", "variante": "Executive", "portes": 5, "places": 4, "reservoir": 75},

                    {"modele": "718", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "718", "variante": "GT4", "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "Cayman", "variante": "GTS", "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "718", "variante": "Spyder", "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "718", "variante": "Spyder RS Weissach", "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "Cayman", "variante": "GT4 RS", "portes": 2, "places": 2,"taille_reservoir": 50},

                    {"modele": "911", "variante": "992 GT3 RS Weissach SSR", "portes": 2, "places": 4, "reservoir": 64},
                    {"modele": "911", "variante": "991.2 GT3 RS", "portes": 2, "places": 2, "reservoir": 64},


                    {"modele": "356", "variante": "", "portes": 2, "places": 4, "reservoir": 50},
                    {"modele": "912", "variante": "", "portes": 2, "places": 2, "reservoir": 62},
                    {"modele": "914", "variante": "", "portes": 2, "places": 2, "reservoir": 50},
                    {"modele": "924", "variante": "", "portes": 3, "places": 4, "reservoir": 63},
                    {"modele": "928", "variante": "", "portes": 3, "places": 4, "reservoir": 86},
                    {"modele": "944", "variante": "", "portes": 3, "places": 4, "reservoir": 80},
                    {"modele": "959", "variante": "", "portes": 2, "places": 2, "reservoir": 85},
                    {"modele": "968", "variante": "", "portes": 3, "places": 4, "reservoir": 80},
                    {"modele": "Boxster", "variante": "", "portes": 2, "places": 2, "reservoir": 64},


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

                "Dacia": [
                    {"modele": "1310", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "1300", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "1100", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 40},


                    {"modele": "Logan", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Logan MCV", "variante": "Break", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Sandero", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Sandero Stepway", "variante": "Hatchback SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Duster", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Duster Oroch", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Spring", "variante": "Hatchback Electrique", "portes": 5, "places": 4, "reservoir": 0}
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

                    {"modele": "Challenger SRT Hellcat", "variante": "Coupe", "portes": 2,"places": 4, "reservoir": 70},
                    {"modele": "Challenger SRT Demon", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                    {"modele": "Charger SRT Hellcat", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Charger SRT Widebody", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Challenger SRT Hellcat Redeye", "variante": None, "portes": 2, "places": 4,
                     "reservoir": 70},
                    {"modele": "Durango SRT", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},
                    {"modele": "Ram 1500 TRX", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 95}
                ],

                "De Tomaso": [
                    {"modele": "Pantera", "variante": "Coupe", "portes": 2, "places": 2,"reservoir": 80},
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
                    {"modele": "Amalfi", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 82},
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
                    {"modele": "Bentley Continental GTC", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 90},


                    {"modele": "Bentley Flying Spur", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},
                    {"modele": "Bentley Mulsanne", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 95},
                    {"modele": "Bentley Continental GT V8", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                    {"modele": "Bentley Continental GT Speed", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                    {"modele": "Bentley Continental GTC V8", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 90},


                    {"modele": "Bentley Continental GT Speed", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
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
                    {"modele": "Audi S5 B8 Cabriolet", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 70},
                    {"modele": "Audi S6 C6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 80},
                    {"modele": "Audi S7 4G", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 80},
                    {"modele": "Audi S8 D4", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},

                    {"modele": "Audi S3 8Y", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},
                    {"modele": "Audi S4 B9", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Audi S4 Avant B9", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "Audi S5 F5", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                    {"modele": "Audi S5 Cabriolet F5", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 70},
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

                "Fisker": [

                    {"modele": "Karma", "variante": "Sedan Hybride", "portes": 4, "places": 4,"reservoir": 50},
                    {"modele": "Ocean", "variante": "SUV Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Fisker Project Ronin", "variante": "Coupé Electrique", "portes": 2, "places": 2, "reservoir": 0}
                ],

                "Ford": [

                    {"modele": "Escort", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Escort", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 50},
                    {"modele": "Fiesta", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 40},
                    {"modele": "Fiesta", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 40},
                    {"modele": "Focus", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Focus", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 55},
                    {"modele": "Mondeo", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},


                    {"modele": "Kuga", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Escape", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Edge", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "Explorer", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},
                    {"modele": "Expedition", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 90},
                    {"modele": "Ranger", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 80},
                    {"modele": "F-150", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 95},


                    {"modele": "Mustang Mach-E", "variante": "SUV Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "F-150 Lightning", "variante": "Pickup Electrique", "portes": 4, "places": 5, "reservoir": 0}
                ],

                "Ford GT": [
                    {"modele": "GT40", "variante": "Coupé course", "portes": 2, "places":2, "reservoir": 90},
                    {"modele": "GT40 Mk II", "variante": "Coupé course", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "GT40 Mk III", "variante": "Coupé route", "portes": 2, "places": 2, "reservoir": 100},


                    {"modele": "Ford GT (2005-2006)", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 90},
                    {"modele": "Ford GT (2016+)", "variante": "Supercar", "portes": 2, "places": 2, "reservoir": 90}
                ],

                "GAZ": [

                    {"modele": "M20 Pobeda", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Volga M21", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Volga M24", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Volga 3102", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Chaika GAZ-13", "variante": "Limousine", "portes": 4, "places": 7, "reservoir": 80},
                    {"modele": "Chaika GAZ-14", "variante": "Limousine", "portes": 4, "places": 7, "reservoir": 80},


                    {"modele": "GAZelle", "variante": "Fourgon", "portes": 4, "places": 3, "reservoir": 70},
                    {"modele": "GAZelle Next", "variante": "Fourgon", "portes": 4, "places": 3, "reservoir": 70},
                    {"modele": "Sobol", "variante": "Van", "portes": 5, "places": 7, "reservoir": 70},


                    {"modele": "GAZ-51", "variante": "Camion", "portes": 2, "places": 3, "reservoir": 90},
                    {"modele": "GAZ-66", "variante": "Camion 4x4", "portes": 2, "places": 2, "reservoir": 110},
                    {"modele": "Tigr", "variante": "Militaire / 4x4", "portes": 5, "places": 7, "reservoir": 120}
                ],

            "Mazda Speed": [


                    {"modele": "MX-5 Miata NA", "variante": "Roadster", "portes": 2, "places": 2,"reservoir": 45},
                    {"modele": "MX-5 Miata NB", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 45},
                    {"modele": "Mazda3", "variante": "MazdaSpeed", "portes": 4, "places": 5, "reservoir": 51},
                    {"modele": "Mazda6", "variante": "MazdaSpeed", "portes": 4, "places": 5, "reservoir": 62},
                    {"modele": "MX-5 Miata NC", "variante": "MazdaSpeed", "portes": 2, "places": 2, "reservoir": 50}
                ],

                "Aiways": [
                    {"modele": "U5", "variante": "Standard", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "U5", "variante": "Premium", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "U6", "variante": "Crossover SUV", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "U6", "variante": "Coupé SUV", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "U7 ion", "variante": "Concept SUV", "portes": 5, "places": 5, "reservoir": 0}
                ],

                "Aston Martin Vantage": [

                    {"modele": "Vantage V8", "variante": "Coupe", "portes": 2,"places": 2, "reservoir": 80},
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

                    {"modele": "Type 35", "variante": "Racing", "portes": 0, "places": 2,"reservoir": 60},
                    {"modele": "Type 41 Royale", "variante": "Luxury", "portes": 4, "places": 4, "reservoir": 120},
                    {"modele": "Type 57", "variante": "SC Atlantic", "portes": 2, "places": 2, "reservoir": 90},
                    {"modele": "Type 57", "variante": "Ventoux", "portes": 2, "places": 2, "reservoir": 90},


                    {"modele": "Veyron 16.4", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Veyron 16.4 Grand Sport", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Chiron", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Chiron Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Chiron Pur Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Chiron Super Sport 300+", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 100},
                    {"modele": "Bolide", "variante": "Hypercar", "portes": 2, "places": 1, "reservoir": 90},
                    {"modele": "Divo", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90},
                    {"modele": "La Voiture Noire", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90},
                    {"modele": "Centodieci", "variante": "Hypercar", "portes": 2, "places": 2, "reservoir": 90}
                ],

                "Borgward": [

                    {"modele": "Isabella", "variante": "Coupe", "portes": 2, "places": 4,"reservoir": 45},
                    {"modele": "Isabella", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "Hansa 1500", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Hansa 1500", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 50},


                    {"modele": "BX5", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "BX7", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "BX7 TS", "variante": "SUV Sport", "portes": 5, "places": 5, "reservoir": 70}
                ],

                "Buick": [
                    {"modele": "Skylark", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                    {"modele": "Skylark", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "LeSabre", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 75},
                    {"modele": "Riviera", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 80},
                    {"modele": "Electra", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 85},
                    {"modele": "Regal", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},


                    {"modele": "Enclave", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},
                    {"modele": "Encore", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Envision", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Regal", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "LaCrosse", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Wildcat", "variante": "Concept", "portes": 2, "places": 4, "reservoir": 60}
                ],

                "BYD": [

                    {"modele": "Tang", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 0},
                    {"modele": "Tang DM", "variante": "SUV Hybride", "portes": 5, "places": 7, "reservoir": 60},
                    {"modele": "Han EV", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Han DM", "variante": "Sedan Hybride", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Yuan", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Yuan Pro", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Dolphin", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Seal", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Seal DM", "variante": "Sedan Hybride", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Atto 3", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Qin EV", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Qin Plus DM", "variante": "Sedan Hybride", "portes": 4, "places": 5, "reservoir": 60}
                ],

                "Cadillac": [

                    {"modele": "DeVille", "variante": "Sedan", "portes": 4, "places": 5,"reservoir": 80},
                    {"modele": "Eldorado", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 75},
                    {"modele": "Fleetwood", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 90},
                    {"modele": "Seville", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Allanté", "variante": "Convertible", "portes": 2, "places": 2, "reservoir": 60},


                    {"modele": "CT4", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "CT5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 65},
                    {"modele": "CT6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "XT4", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65},
                    {"modele": "XT5", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "XT6", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 75},
                    {"modele": "Escalade", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 90},
                    {"modele": "Escalade ESV", "variante": "SUV Long", "portes": 5, "places": 7, "reservoir": 95}
                ],

                "Chevrolet": [

                    {"modele": "Bel Air", "variante": "Sedan", "portes": 4, "places": 5,"reservoir": 70},
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

                "Chery": [

                    {"modele": "QQ", "variante": "Hatchback", "portes": 3, "places": 4,"reservoir": 35},
                    {"modele": "QQ", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 35},
                    {"modele": "Tiggo 3", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 55},
                    {"modele": "Tiggo 3X", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Tiggo 5", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Tiggo 7", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Tiggo 8", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 65},
                    {"modele": "Arrizo 5", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Arrizo 6", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Arrizo GX", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Arrizo e", "variante": "Sedan Electrique", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Tiggo e", "variante": "SUV Electrique", "portes": 5, "places": 5, "reservoir": 0}
                ],

                "Chrysler": [

                    {"modele": "New Yorker", "variante": "Sedan", "portes": 4, "places": 5,"reservoir": 70},
                    {"modele": "Imperial", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 75},
                    {"modele": "Imperial", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 75},
                    {"modele": "300", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 75},
                    {"modele": "LeBaron", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                    {"modele": "LeBaron", "variante": "Convertible", "portes": 2, "places": 4, "reservoir": 70},


                    {"modele": "Pacifica", "variante": "Minivan", "portes": 5, "places": 7, "reservoir": 70},
                    {"modele": "Pacifica Hybrid", "variante": "Minivan Hybride", "portes": 5, "places": 7, "reservoir": 40},
                    {"modele": "Voyager", "variante": "Minivan", "portes": 5, "places": 7, "reservoir": 65},
                    {"modele": "300", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 75},
                    {"modele": "Aspen", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 75},
                    {"modele": "Town & Country", "variante": "Minivan", "portes": 5, "places": 7, "reservoir": 75}
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

                    {"modele": "BX 4TC", "variante": "Rallye", "portes": 5,"places": 4, "reservoir": 70},
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

                    {"modele": "Cupra Ibiza", "variante": "Sport","portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "Cupra Leon", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Cupra Leon ST", "variante": "Sport", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Cupra Leon Competición", "variante": "Racing", "portes": 5, "places": 4, "reservoir": 50},


                    {"modele": "Cupra Ateca", "variante": "SUV Sport", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Cupra Formentor", "variante": "SUV Coupé Sport", "portes": 5, "places": 5, "reservoir": 55},
                    {"modele": "Cupra Born", "variante": "Hatchback Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Cupra Tavascan", "variante": "SUV Electrique Concept", "portes": 5, "places": 5, "reservoir": 0}
                ],

                "Daewoo": [
                    {"modele": "Lanos", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Lanos", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 50},
                    {"modele": "Nubira", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Nubira", "variante": "Wagon", "portes": 5, "places": 5, "reservoir": 55},
                    {"modele": "Leganza", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Espero", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},


                    {"modele": "Tacuma", "variante": "MPV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Rezzo", "variante": "MPV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Korando", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 65}
                ],

                "Daihatsu": [
                    {"modele": "Charade", "variante": "Hatchback", "portes": 3, "places": 4,"reservoir": 35},
                    {"modele": "Charade", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 35},
                    {"modele": "Applause", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "Rocky", "variante": "SUV", "portes": 3, "places": 4, "reservoir": 50},
                    {"modele": "Rocky", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},


                    {"modele": "Cuore", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 30},
                    {"modele": "Cuore", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 30},
                    {"modele": "Move", "variante": "MPV", "portes": 5, "places": 5, "reservoir": 35},
                    {"modele": "Terios", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Sirion", "variante": "Hatchback", "portes": 5, "places": 5, "reservoir": 35},
                    {"modele": "Cast", "variante": "Hatchback", "portes": 5, "places": 4, "reservoir": 35}
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
                    {"modele": "DS7 Crossback E-Tense", "variante": "SUV Hybride Rechargeable", "portes": 5, "places": 5,"reservoir": 55}
               ],

                "Fiat": [


                    {"modele": "500", "variante": "Cabriolet Classique", "portes": 2, "places": 4,"reservoir": 20},
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
                    {"modele": "F1", "variante": "Base", "portes": 2,"places": 3, "reservoir": 90},
                    {"modele": "F1 LM", "variante": "Edition Limitée", "portes": 2, "places": 3, "reservoir": 90},
                    {"modele": "F1 GTR Road Version", "variante": "Edition Limitée", "portes": 2, "places": 3, "reservoir": 90},


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
                    {"modele": "McLaren Speedtail LM", "variante": "Edition Limitée", "portes": 2, "places": 2, "reservoir": 85}
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


            #"Porsche": [
                    #{"modele": "550 Spyder", "nom_variante": None, "nombre_portes": 2, "nbre_places": 2,
                    # "taille_reservoir": 60},


                    #{"modele": "911", "nom_variante": "Carrera S", "nombre_portes": 2, "nbre_places": 4,
                    # "taille_reservoir": 67},
                    #{"modele": "911", "nom_variante": "Turbo", "nombre_portes": 2, "nbre_places": 4,
                    # "taille_reservoir": 67},

                    # 911 GT spéciaux

                    #{"modele": "911", "nom_variante": "GT3", "nombre_portes": 2, "nbre_places": 2,
                     #"taille_reservoir": 64},
                    #{"modele": "911", "nom_variante": "GT3 RS", "nombre_portes": 2, "nbre_places": 2,
                     #"taille_reservoir": 64},
                    #{"modele": "911", "nom_variante": "GT2 RS", "nombre_portes": 2, "nbre_places": 2,
                     #"taille_reservoir": 64},

                    # SUV et berlines
                    #{"modele": "Cayenne", "nom_variante": "S", "nombre_portes": 5, "nbre_places": 5,
                     #"taille_reservoir": 75},
                   # {"modele": "Macan", "nom_variante": None, "nombre_portes": 5, "nbre_places": 5,
                    # "taille_reservoir": 60},
                   # {"modele": "Panamera", "nom_variante": "4S", "nombre_portes": 5, "nbre_places": 5,
                    # "taille_reservoir": 75},

                #],
                "GMC": [

                    {"modele": "Sierra 1500", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 98},
                    {"modele": "Sierra 2500HD", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 136},
                    {"modele": "Sierra 3500HD", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 136},


                       {"modele": "Yukon", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 98},
                    {"modele": "Yukon XL", "variante": "SUV Long", "portes": 5, "places": 8, "reservoir": 106},
                    {"modele": "Acadia", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 75},
                    {"modele": "Terrain", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 60},


                       {"modele": "Savana", "variante": "Van", "portes": 4, "places": 12, "reservoir": 117},
                    {"modele": "Canyon", "variante": "Pickup Moyen", "portes": 4, "places": 5, "reservoir": 80},


                       {"modele": "Hummer EV", "variante": "Pickup Electrique", "portes": 4, "places": 5, "reservoir": 0}
                    ],

                "Great Wall": [
                    {"modele": "Wingle 5", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Wingle 7", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Poer", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 78},


                    {"modele": "Haval H2", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 58},
                    {"modele": "Haval H6", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 58},
                    {"modele": "Haval H9", "variante": "SUV 4x4", "portes": 5, "places": 7, "reservoir": 80},
                    {"modele": "Tank 300", "variante": "SUV 4x4", "portes": 5, "places": 5, "reservoir": 80},


                    {"modele": "Ora Funky Cat", "variante": "Hatchback Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Tank 500 Hybrid", "variante": "SUV Hybride", "portes": 5, "places": 7, "reservoir": 70}
                ],

                "Gurgel": [

                    {"modele": "BR-800", "variante": "Hatchback", "portes": 3, "places": 4,"reservoir": 30},
                    {"modele": "Supermini", "variante": "Hatchback", "portes": 3, "places": 4, "reservoir": 32},


                    {"modele": "X-12", "variante": "4x4", "portes": 2, "places": 4, "reservoir": 45},
                    {"modele": "X-15", "variante": "4x4", "portes": 2, "places": 4, "reservoir": 45},
                    {"modele": "Carajas", "variante": "4x4", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Tocantins", "variante": "4x4", "portes": 2, "places": 4, "reservoir": 45}
                ],

                "Haval": [
                    {"modele": "H1", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "H2", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "H4", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "H5", "variante": "SUV 4x4", "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "H6", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 58},
                    {"modele": "H7", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 58},
                    {"modele": "H8", "variante": "SUV Luxe", "portes": 5, "places": 5, "reservoir": 72},
                    {"modele": "H9", "variante": "SUV 4x4", "portes": 5, "places": 7, "reservoir": 80},
                    {"modele": "Jolion", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 55}
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

                "Hindustan Motors": [

                    {"modele": "Ambassador", "variante": "Mark I", "portes": 4, "places": 5,"reservoir": 50},
                    {"modele": "Ambassador", "variante": "Mark II", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Ambassador", "variante": "Mark III", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Ambassador", "variante": "Mark IV", "portes": 4, "places": 5, "reservoir": 55},


                    {"modele": "Ambassador Classic", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Ambassador Grand", "variante": None, "portes": 4, "places": 5, "reservoir": 55}
                ],

                "Hispano-Suiza": [

                    {"modele": "H6B", "variante": "Berlina", "portes": 4, "places": 5,"reservoir": 80},
                    {"modele": "H6C", "variante": "Sport", "portes": 2, "places": 2, "reservoir": 80},
                    {"modele": "K6", "variante": None, "portes": 4, "places": 5, "reservoir": 80},


                    {"modele": "Carmen", "variante": "Coupe Electrique", "portes": 2, "places": 2, "reservoir": 0},
                    {"modele": "Carmen Boulogne", "variante": "Coupe Electrique", "portes": 2, "places": 2, "reservoir": 0}
                ],

                "Holden": [

                    {"modele": "Commodore", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Caprice", "variante": None, "portes": 4, "places": 5, "reservoir": 75},
                    {"modele": "Statesman", "variante": None, "portes": 4, "places": 5, "reservoir": 75},


                    {"modele": "Astra", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Zafira", "variante": None, "portes": 5, "places": 7, "reservoir": 60},
                    {"modele": "Trax", "variante": None, "portes": 5, "places": 5, "reservoir": 50},


                    {"modele": "Acadia", "variante": None, "portes": 5, "places": 7, "reservoir": 75},
                    {"modele": "Colorado", "variante": "Pickup", "portes": 4, "places": 5, "reservoir": 80},


                    {"modele": "HSV Clubsport", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "HSV GTS", "variante": None, "portes": 4, "places": 5, "reservoir": 70}
                ],

                "Hongqi": [
                    {"modele": "CA72", "variante": None, "portes": 4, "places": 5,"reservoir": 90},
                    {"modele": "CA770", "variante": None, "portes": 4, "places": 5, "reservoir": 90},
                    {"modele": "L5", "variante": None, "portes": 4, "places": 5, "reservoir": 95},
                    {"modele": "H5", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "H7", "variante": None, "portes": 4, "places": 5, "reservoir": 60},


                    {"modele": "HS5", "variante": None, "portes": 5, "places": 5, "reservoir": 65},
                    {"modele": "HS7", "variante": None, "portes": 5, "places": 7, "reservoir": 70},
                    {"modele": "E-HS9", "variante": "Electrique", "portes": 5, "places": 7, "reservoir": 0}
                ],

                "Hummer": [

                    {"modele": "H1", "variante": None, "portes": 4, "places": 4, "reservoir": 95},


                    {"modele": "H2", "variante": None, "portes": 4, "places": 5, "reservoir": 96},
                    {"modele": "H3", "variante": None, "portes": 4, "places": 5, "reservoir": 80},


                    {"modele": "Hummer EV Pickup", "variante": "Electrique", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Hummer EV SUV", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0}
                ],





                # Corée
                "Hyundai": [

                    {"modele": "i10", "variante": None, "portes": 5, "places": 5, "reservoir": 35},
                    {"modele": "i20", "variante": None, "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "i20", "variante": "N", "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "i30", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "i30", "variante": "N", "portes": 5, "places": 5, "reservoir": 50},


                    {"modele": "Elantra", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Sonata", "variante": None, "portes": 4, "places": 5, "reservoir": 60},


                    {"modele": "Kona", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Tucson", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Santa Fe", "variante": None, "portes": 5, "places": 7, "reservoir": 71},
                    {"modele": "Palisade", "variante": None, "portes": 5, "places": 7, "reservoir": 71},


                    {"modele": "Veloster N", "variante": "Sport", "portes": 3, "places": 4, "reservoir": 50},


                    {"modele": "Ioniq 5", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Ioniq 6", "variante": "Electrique", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Kona Electric", "variante": "Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Tucson Hybrid", "variante": "Hybride", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Santa Fe Hybrid", "variante": "Hybride", "portes": 5, "places": 7, "reservoir": 71}
                ],

                "Hyundai N": [
                    {"modele": "i20 N", "variante": None, "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "i30 N", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Veloster N", "variante": None, "portes": 3, "places": 4, "reservoir": 50},
                    {"modele": "Kona N", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Elantra N", "variante": None, "portes": 4, "places": 5, "reservoir": 50}
                ],

                "Infiniti": [

                    {"modele": "Q50", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Q60", "variante": None, "portes": 2, "places": 4, "reservoir": 65},
                    {"modele": "Q70", "variante": None, "portes": 4, "places": 5, "reservoir": 80},
                    {"modele": "Q70L", "variante": "Long Wheelbase", "portes": 4, "places": 5, "reservoir": 80},


                       {"modele": "QX30", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "QX50", "variante": None, "portes": 5, "places": 5, "reservoir": 65},
                    {"modele": "QX55", "variante": None, "portes": 5, "places": 5, "reservoir": 65},
                    {"modele": "QX60", "variante": None, "portes": 5, "places": 7, "reservoir": 75},
                    {"modele": "QX80", "variante": None, "portes": 5, "places": 7, "reservoir": 95},


                       {"modele": "Q50 Hybrid", "variante": "Hybride", "portes": 4, "places": 5, "reservoir": 70}
                ],

                "Jaguar": [

                    {"modele": "XE", "variante": None, "portes": 4, "places": 5,"reservoir": 63},
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
                    {"modele": "A40 Berlina",           "variante": None, "portes": 4, "places": 5, "reservoir": 35},
                    {"modele": "A40 Combinata",         "variante": None, "portes": 3, "places": 5, "reservoir": 35},

                    {"modele": "950 Spider",            "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                    {"modele": "IM3 / IM3S / I4 / I5",  "variante": None, "portes": 4, "places": 5, "reservoir": 45},

                    {"modele": "Innocenti 186 GT",      "variante": None, "portes": 2, "places": 4, "reservoir": 50},

                    {"modele": "Mini (ADO15)",          "variante": None, "portes": 2, "places": 4, "reservoir": 40},
                    {"modele": "Mini Cooper Mk1",       "variante": None, "portes": 2, "places": 4, "reservoir": 40},
                    {"modele": "Mini Cooper Mk2",       "variante": None, "portes": 2, "places": 4, "reservoir": 40},
                    {"modele": "Mini 90L",              "variante": None, "portes": 2, "places": 4, "reservoir": 40},
                    {"modele": "Mini 120L",             "variante": None, "portes": 2, "places": 4, "reservoir": 40},

                    {"modele": "Mini Bertone",          "variante": None, "portes": 3, "places": 4, "reservoir": 40},
                    {"modele": "Mini 3‑Cilindri",       "variante": None, "portes": 3, "places": 4, "reservoir": 40},
                    {"modele": "Mini De Tomaso",        "variante": None, "portes": 2, "places": 4, "reservoir": 40},

                    {"modele": "Regent",                "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "IM3‑I4‑I5 (ADO16)",     "variante": None, "portes": 4, "places": 5, "reservoir": 45},

                    {"modele": "Koral",                 "variante": None, "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "Elba",                  "variante": None, "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "Mille",                 "variante": None, "portes": 3, "places": 5, "reservoir": 45},
                ],

                "Iran Khodro": [
                    {"modele": "Paykan", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "Paykan Pickup", "variante": "Bardo", "portes": 2, "places": 2, "reservoir": 45},

                    {"modele": "Peugeot 405", "variante": "Berline", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "Peugeot Pars", "variante": None, "portes": 4, "places": 5, "reservoir": 60},

                    {"modele": "Samand", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Samand Soren", "variante": None, "portes": 4, "places": 5, "reservoir": 55},

                    {"modele": "Runna", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Runna+", "variante": None, "portes": 4, "places": 5, "reservoir": 50},

                    {"modele": "Dena", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Dena+", "variante": None, "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Dena+ Turbo", "variante": None, "portes": 4, "places": 5, "reservoir": 55},

                    {"modele": "Arisun", "variante": "Pickup", "portes": 2, "places": 2, "reservoir": 45},
                    {"modele": "Arisun 2", "variante": "Pickup", "portes": 2, "places": 2, "reservoir": 45},

                    {"modele": "Tara", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Reera", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                ],

                "Isuzu": [
                    # Modèles historiques ou classiques
                    {"modele": "Bellett", "variante": None, "portes": 4, "places": 5, "reservoir": 45},
                    {"modele": "Isuzu Florian", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "117 Coupé", "variante": None, "portes": 2, "places": 4, "reservoir": 45},
                    {"modele": "Gemini", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Piazza", "variante": None, "portes": 2, "places": 4, "reservoir": 50},
                    {"modele": "Amigo", "variante": None, "portes": 3, "places": 5, "reservoir": 45},
                    {"modele": "Trooper", "variante": None, "portes": 4, "places": 5, "reservoir": 65},
                    {"modele": "VehiCROSS", "variante": None, "portes": 3, "places": 4, "reservoir": 60},

                    # SUV et crossovers
                    {"modele": "Rodeo", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                    {"modele": "Axiom", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                    {"modele": "Ascender", "variante": None, "portes": 5, "places": 5, "reservoir": 70},

                    # Pick‑ups et utilitaires légers
                    {"modele": "D‑Max", "variante": "Single Cab", "portes": 2, "places": 2, "reservoir": 76},
                    {"modele": "D‑Max", "variante": "Double Cab", "portes": 4, "places": 5, "reservoir": 76},
                    {"modele": "MU‑X", "variante": None, "portes": 5, "places": 7, "reservoir": 76},

                    # Autres (véhicules utilitaires légers ou modèles rares)
                    {"modele": "Panther", "variante": None, "portes": 4, "places": 8, "reservoir": 70},
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


            "Ligier": [
                {"modele": "JS50", "variante": None, "portes": 2, "places": 2, "reservoir": 15},
                {"modele": "JS50L", "variante": None, "portes": 2, "places": 2, "reservoir": 15},
                {"modele": "Myli", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "Ixo", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "BE", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "Optimax", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "Pulse 4", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "X-too RS", "variante": None, "portes": 2, "places": 2, "reservoir": 10},
                {"modele": "JS1", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "JS2", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "JS3", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "JS P4", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "JS2 R", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "JS2 RS", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "JS51", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "JS55", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
            ],

            "Ginetta": [
                {"modele": "G4", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "G15", "variante": None, "portes": 2, "places": 2, "reservoir": 55},
                {"modele": "G32", "variante": None, "portes": 2, "places": 2, "reservoir": 55},
                {"modele": "G40", "variante": None, "portes": 2, "places": 2, "reservoir": 55},
                {"modele": "G50", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "G60", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "G55", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "G56", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "GT2", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Akula", "variante": None, "portes": 2, "places": 2, "reservoir": 80}
            ],
            "Brabham": [
                {"modele": "BT14", "variante": "Formula", "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "BT17", "variante": "Sports Prototype", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT18", "variante": "Formula 2/3", "portes": 0, "places": 1, "reservoir": 75},
                {"modele": "BT24", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT34", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT44", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT45", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT49", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT50", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT52", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT56", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT60", "variante": "Formula 1", "portes": 0, "places": 1, "reservoir": 90},
                {"modele": "BT62", "variante": "Track Hypercar", "portes": 2, "places": 2, "reservoir": 80},
            ],



            "Matra": [
                {"modele": "Matra Djet", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "Matra 530", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Matra Bagheera", "variante": None, "portes": 3, "places": 3, "reservoir": 60},
                {"modele": "Matra Murena", "variante": None, "portes": 3, "places": 3, "reservoir": 60},
                {"modele": "Matra Rancho", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
            ],

            "Bugatti (ancien)": [
                {"modele": "Type 35", "variante": "Grand Prix", "portes": 0, "places": 1, "reservoir": 40},
                {"modele": "Type 37", "variante": None, "portes": 0, "places": 1, "reservoir": 40},
                {"modele": "Type 41 Royale", "variante": None, "portes": 4, "places": 4, "reservoir": 120},
                {"modele": "Type 57", "variante": "SC Atlantic", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Type 101", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
            ],

            "Panhard Racing": [
                {"modele": "Panhard CD", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "Panhard 24 CT", "variante": None, "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Panhard LM64", "variante": "Prototype", "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "Panhard X86", "variante": "Prototype", "portes": 0, "places": 1, "reservoir": 80},

                {"modele": "X85", "variante": None, "portes": 0, "places": 1, "reservoir": 60},
                {"modele": "X88", "variante": None, "portes": 0, "places": 1, "reservoir": 60},
                {"modele": "Dyna X", "variante": None, "portes": 0, "places": 1, "reservoir": 60},
                {"modele": "24 CT", "variante": None, "portes": 0, "places": 1, "reservoir": 60},
                {"modele": "24 BT", "variante": None, "portes": 0, "places": 1, "reservoir": 60}
            ],

            "Talbot-Lago": [
                {"modele": "T26 Record", "variante": None, "portes": 4, "places": 4, "reservoir": 100},
                {"modele": "T150 C-SS", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "T23", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "T26 Grand Sport", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            ],
            "Opel OPC": [
                {"modele": "Astra G OPC", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Astra H OPC", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Astra J OPC", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Vectra OPC", "variante": None, "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Zafira A OPC", "variante": None, "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "Zafira B OPC", "variante": None, "portes": 5, "places": 7, "reservoir": 70},
                {"modele": "Meriva A OPC", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Corsa D OPC", "variante": None, "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Corsa E OPC", "variante": None, "portes": 3, "places": 5, "reservoir": 45},
                {"modele": "Insignia OPC", "variante": "Berline", "portes": 5, "places": 5, "reservoir": 70},
                {"modele": "Insignia OPC Sports Tourer", "variante": "Break", "portes": 5, "places": 5, "reservoir": 70}
            ],

            "Dallara": [
                # Monoplaces de course
                {"modele": "F3", "variante": "Formula 3", "portes": 0, "places": 1, "reservoir": 70},
                {"modele": "F2", "variante": "Formula 2", "portes": 0, "places": 1, "reservoir": 75},
                {"modele": "IndyCar", "variante": None, "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "GP2", "variante": None, "portes": 0, "places": 1, "reservoir": 75},
                {"modele": "Super Formula", "variante": None, "portes": 0, "places": 1, "reservoir": 75},

                # Voitures de sport / prototypes routiers
                {"modele": "Stradale", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "PZero", "variante": "GT", "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "DPV8", "variante": "Prototype", "portes": 0, "places": 1, "reservoir": 90},

                # Voitures pour courses spécifiques
                {"modele": "DW12", "variante": "IndyCar chassis", "portes": 0, "places": 1, "reservoir": 80},
                {"modele": "Tatuus F4 chassis", "variante": None, "portes": 0, "places": 1, "reservoir": 70}
            ],
            "Wiesmann": [
                {"modele": "MF3", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "MF4", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "MF4", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "MF5", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "MF5", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "MF6", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "GT MF4-CS", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "GT MF4-R", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "GT MF5", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 80},
            ],

            "Artega": [
                {"modele": "GT", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Scalo", "variante": "Electrique Concept", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Karo", "variante": "Roadster Prototype", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "SE", "variante": "Electrique", "portes": 2, "places": 2, "reservoir": 0}
            ],

            "Lancia HF": [
                {"modele": "Fulvia HF", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "Fulvia HF 1.6", "variante": None, "portes": 2, "places": 4, "reservoir": 50},
                {"modele": "Stratos HF", "variante": "Stradale", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Stratos HF Rally", "variante": "Rally", "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "037 Rally", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Delta HF 4WD", "variante": "Turbo", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Delta HF Integrale", "variante": "Evoluzione", "portes": 5, "places": 5, "reservoir": 60},
                {"modele": "Delta HF Integrale 16V", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
            ],

            "Pininfarina Battista": [
                {"modele": "Battista", "variante": "Roadster Concept", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Battista Anniversario", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Battista Anniversario Roadster", "variante": "Roadster", "portes": 2, "places": 2,
                 "reservoir": 0},
                {"modele": "Battista Anniversario N-Largo", "variante": "Edition limitée", "portes": 2, "places": 2,
                 "reservoir": 0}
            ],
            "Caterham": [
                {"modele": "Caterham Seven 160", "variante": None, "portes": 2, "places": 2, "reservoir": 35},
                {"modele": "Caterham Seven 270", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "Caterham Seven 310", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "Caterham Seven 360", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "Caterham Seven 420", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "Caterham Seven 485", "variante": None, "portes": 2, "places": 2, "reservoir": 40},
                {"modele": "Caterham Seven 620", "variante": None, "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Caterham Seven CSR", "variante": None, "portes": 2, "places": 2, "reservoir": 45},
                {"modele": "Caterham Seven R500", "variante": None, "portes": 2, "places": 2, "reservoir": 45}
            ],

            "Bentley Continental GT": [
                {"modele": "Continental GT", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Continental GT Speed", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Continental GT V8", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Continental GT Convertible", "variante": "Cabriolet", "portes": 2, "places": 4,
                 "reservoir": 90},
                {"modele": "Continental GT Speed Convertible", "variante": "Cabriolet", "portes": 2, "places": 4,
                 "reservoir": 90},
                {"modele": "Continental GT Mulliner", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 90},
                {"modele": "Continental GT Mulliner Convertible", "variante": "Cabriolet", "portes": 2, "places": 4,
                 "reservoir": 90}
            ],

            "Noble": [
                {"modele": "M12 GTO", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "M12 GTO-3R", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "M12 GTO-3R RS", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "M400", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Noble M600", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Noble M600 Speedster", "variante": None, "portes": 2, "places": 2, "reservoir": 80}
            ],

            "Morgan Aero": [
                {"modele": "Aero 8", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Aero SuperSports", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Aero Coupe", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Aero Roadster", "variante": None, "portes": 2, "places": 2, "reservoir": 60}
            ],

            "Gordon Murray Automotive": [
                {"modele": "T.50", "variante": "Coupe", "portes": 2, "places": 3, "reservoir": 60},
                {"modele": "T.50s Niki Lauda", "variante": "Edition limitée", "portes": 2, "places": 1,
                 "reservoir": 60},
                {"modele": "T.33", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "T.33C", "variante": "Cabriolet", "portes": 2, "places": 2, "reservoir": 65}
            ],



            "Toyota Supra": [
                {"modele": "Supra A40 (MK1)", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Supra A60 (MK2)", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Supra A70 (MK3)", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Supra A80 (MK4)", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "Supra A90 (MK5)", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Supra GR", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Supra GR Sport", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 70}
            ],

            "Honda S2000": [
                {"modele": "S2000 AP1", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "S2000 AP2", "variante": None, "portes": 2, "places": 2, "reservoir": 50},
                {"modele": "S2000 CR", "variante": "Club Racer", "portes": 2, "places": 2, "reservoir": 50}
            ],

            "Cadillac V-Series": [
                {"modele": "CTS-V", "variante": None, "portes": 4, "places": 5, "reservoir": 72},
                {"modele": "CTS-V Wagon", "variante": None, "portes": 5, "places": 5, "reservoir": 72},
                {"modele": "ATS-V", "variante": None, "portes": 4, "places": 5, "reservoir": 64},
                {"modele": "CT4-V", "variante": None, "portes": 4, "places": 5, "reservoir": 60},
                {"modele": "CT5-V", "variante": None, "portes": 4, "places": 5, "reservoir": 61},
                {"modele": "CT5-V Blackwing", "variante": "Edition performance", "portes": 4, "places": 5,
                 "reservoir": 61},
                {"modele": "Escalade-V", "variante": None, "portes": 5, "places": 7, "reservoir": 90}
            ],

            "Shelby": [
                {"modele": "Shelby GT350", "variante": None, "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Shelby GT500", "variante": None, "portes": 2, "places": 4, "reservoir": 61},
                {"modele": "Shelby Cobra 427", "variante": None, "portes": 2, "places": 2, "reservoir": 65},
                {"modele": "Shelby Super Snake", "variante": None, "portes": 2, "places": 4, "reservoir": 60},
                {"modele": "Shelby Daytona Coupe", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Shelby Series 1", "variante": None, "portes": 2, "places": 2, "reservoir": 60}
            ],

            "Hennessey Venom": [
                {"modele": "Venom GT", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Venom F5", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
                {"modele": "Venom F5 Roadster", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 90}
            ],

            "Chevrolet Corvette": [
                {"modele": "Corvette C1", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Corvette C2", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Corvette C3", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "Corvette C4", "variante": None, "portes": 2, "places": 2, "reservoir": 75},
                {"modele": "Corvette C5", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Corvette C6", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Corvette C7", "variante": None, "portes": 2, "places": 2, "reservoir": 82},
                {"modele": "Corvette C8", "variante": "Coupe", "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "Corvette C8 Convertible", "variante": "Cabriolet", "portes": 2, "places": 2,
                 "reservoir": 72}
            ],


            "Saleen": [
                {"modele": "S7", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "S7 Twin Turbo", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "S281", "variante": None, "portes": 2, "places": 4, "reservoir": 72},
                {"modele": "S302", "variante": None, "portes": 2, "places": 4, "reservoir": 72},
                {"modele": "S351", "variante": None, "portes": 2, "places": 4, "reservoir": 72},
                {"modele": "S7 LM", "variante": None, "portes": 2, "places": 2, "reservoir": 80}
            ],

            "SSC Tuatara": [
                {"modele": "Tuatara Coupe", "variante": None, "portes": 2, "places": 2, "reservoir": 100},
                {"modele": "Tuatara Roadster", "variante": "Roadster", "portes": 2, "places": 2, "reservoir": 100}
            ],

            "Chevrolet Camaro ZL1": [
                {"modele": "Camaro ZL1 2012-2015", "variante": None, "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Camaro ZL1 2017-2023", "variante": None, "portes": 2, "places": 4, "reservoir": 72},
                {"modele": "Camaro ZL1 Convertible", "variante": "Cabriolet", "portes": 2, "places": 4, "reservoir": 72}
            ],

            "Lola": [
                {"modele": "T70", "variante": None, "portes": 0, "places": 1, "reservoir": 120},
                {"modele": "T212", "variante": None, "portes": 0, "places": 1, "reservoir": 100},
                {"modele": "B98/10", "variante": None, "portes": 0, "places": 1, "reservoir": 100},
                {"modele": "B05/40", "variante": None, "portes": 0, "places": 1, "reservoir": 100},
                {"modele": "B12/80", "variante": None, "portes": 0, "places": 1, "reservoir": 100},
                {"modele": "T3000", "variante": None, "portes": 0, "places": 1, "reservoir": 100}
            ],

            "Marcos": [
                {"modele": "GT", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Mantara", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "Talon", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "GTS", "variante": None, "portes": 2, "places": 2, "reservoir": 60},
                {"modele": "LM600", "variante": None, "portes": 2, "places": 2, "reservoir": 60}
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

                "Lada": [
                    # Modèles historiques / classiques
                    {"modele": "2101", "variante": None, "portes": 4, "places": 5, "reservoir": 42},
                    {"modele": "2102", "variante": None, "portes": 2, "places": 4, "reservoir": 42},
                    {"modele": "2103", "variante": None, "portes": 4, "places": 5, "reservoir": 42},
                    {"modele": "2104", "variante": "Break", "portes": 5, "places": 5, "reservoir": 42},
                    {"modele": "2105", "variante": None, "portes": 4, "places": 5, "reservoir": 42},
                    {"modele": "2106", "variante": None, "portes": 4, "places": 5, "reservoir": 42},
                    {"modele": "2107", "variante": None, "portes": 4, "places": 5, "reservoir": 42},

                    # Série Samara / Sputnik
                    {"modele": "Samara 3 portes", "variante": None, "portes": 3, "places": 5, "reservoir": 50},
                    {"modele": "Samara 5 portes", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Samara Coupe", "variante": None, "portes": 3, "places": 4, "reservoir": 50},

                    # Série 110
                    {"modele": "Lada 110", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Lada 111", "variante": "Break", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Lada 112", "variante": None, "portes": 5, "places": 5, "reservoir": 50},

                    # Modèles SUV / tout‑terrain
                    {"modele": "Niva (2121)", "variante": None, "portes": 3, "places": 5, "reservoir": 60},
                    {"modele": "Niva 5 portes", "variante": None, "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Urban Niva", "variante": None, "portes": 5, "places": 5, "reservoir": 60},

                    # Gamme moderne
                    {"modele": "Granta", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Granta Liftback", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Granta Cross", "variante": None, "portes": 4, "places": 5, "reservoir": 50},

                    {"modele": "Vesta", "variante": None, "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Vesta SW", "variante": "Break", "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "Vesta Cross", "variante": None, "portes": 5, "places": 5, "reservoir": 50},

                    {"modele": "X‑Ray", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                    {"modele": "X‑Ray Cross", "variante": None, "portes": 5, "places": 5, "reservoir": 50},

                    {"modele": "Largus", "variante": None, "portes": 5, "places": 5, "reservoir": 55},
                    # basé sur Dacia Logan
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

                "Land Rover": [
                    # Modèles historiques / anciens
                    {"modele": "Series I", "variante": None, "portes": 3, "places": 2, "annees": "1948–1958"},
                    {"modele": "Series II", "variante": None, "portes": 3, "places": 2, "annees": "1958–1967"},
                    {"modele": "Series IIA", "variante": None, "portes": 3, "places": 2, "annees": "1961–1971"},
                    {"modele": "Series III", "variante": None, "portes": 3, "places": 2, "annees": "1971–1985"},

                    {"modele": "Freelander", "variante": None, "portes": 5, "places": 5, "annees": "1997–2015"},
                    {"modele": "Discovery Series I", "variante": None, "portes": 5, "places": 5, "annees": "1989–1998"},
                    {"modele": "Discovery Series II", "variante": None, "portes": 5, "places": 5, "annees": "1998–2004"},


                    {"modele": "Discovery 5", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "Discovery Sport", "variante": None, "portes": 5, "places": 5, "annees": "2015–présent"},
                    {"modele": "Defender 90/110/130", "variante": None, "portes": 3 , "places": 5 ,"annees": "1983–présent"},
                ],

                "Lexus": [
                    # Modèles historiques / anciens
                    {"modele": "LS 400", "variante": None, "portes": 4, "places": 5, "annees": "1989–1994"},
                    {"modele": "LS 430", "variante": None, "portes": 4, "places": 5, "annees": "2000–2006"},
                    {"modele": "GS 300", "variante": None, "portes": 4, "places": 5, "annees": "1993–2005"},
                    {"modele": "IS 200", "variante": None, "portes": 4, "places": 5, "annees": "1998–2005"},
                    {"modele": "SC 400", "variante": "Coupé", "portes": 2, "places": 4, "annees": "1991–2000"},
                    {"modele": "RX 300", "variante": None, "portes": 5, "places": 5, "annees": "1998–2003"},

                    # Modèles intermédiaires
                    {"modele": "IS 250", "variante": None, "portes": 4, "places": 5, "annees": "2005–2013"},
                    {"modele": "GS 450h", "variante": "Hybride", "portes": 4, "places": 5, "annees": "2006–2011"},
                    {"modele": "RX 450h", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2009–2015"},
                    {"modele": "CT 200h", "variante": "Compact hybride", "portes": 5, "places": 5, "annees": "2011–2020"},

                    # Modèles récents / actuels
                    {"modele": "IS 300", "variante": None, "portes": 4, "places": 5, "annees": "2017–présent"},
                    {"modele": "ES 300h", "variante": "Hybride", "portes": 4, "places": 5, "annees": "2018–présent"},
                    {"modele": "LS 500", "variante": None, "portes": 4, "places": 5, "annees": "2017–présent"},
                    {"modele": "NX 350h", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2021–présent"},
                    {"modele": "RX 500h", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2022–présent"},
                    {"modele": "UX 250h", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2019–présent"},
                    {"modele": "RZ 450e", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2023–présent"},
                ],

                "Li Auto": [
                    # Modèles historiques / anciens
                    {"modele": "Li ONE", "variante": None, "portes": 5, "places": 5, "annees": "2019–2022"},

                    # Modèles récents / actuels
                    {"modele": "Li L6", "variante": None, "portes": 5, "places": 5, "annees": "2024–présent"},
                    {"modele": "Li L7", "variante": None, "portes": 5, "places": 5, "annees": "2023–présent"},
                    {"modele": "Li L8", "variante": None, "portes": 5, "places": 6, "annees": "2022–présent"},
                    {"modele": "Li L9", "variante": None, "portes": 5, "places": 6, "annees": "2022–présent"},
                    {"modele": "Li i8", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2025–présent"},
                    {"modele": "Li MEGA", "variante": "MPV électrique", "portes": 5, "places": 7, "annees": "2024–présent"},
                ],

                "Lincoln": [
                    # Modèles historiques / anciens
                    {"modele": "Model L Series", "variante": None, "portes": 4, "places": 5, "annees": "1920–1930"},
                    {"modele": "Model K Series", "variante": None, "portes": 4, "places": 5, "annees": "1931–1940"},
                    {"modele": "Zephyr", "variante": None, "portes": 4, "places": 5, "annees": "1936–1942"},
                    {"modele": "Continental", "variante": None, "portes": 4, "places": 5, "annees": "1941–1948"},
                    {"modele": "Cosmopolitan", "variante": None, "portes": 4, "places": 5, "annees": "1949–1954"},
                    {"modele": "Capri", "variante": None, "portes": 4, "places": 5, "annees": "1952–1959"},
                    {"modele": "Premiere", "variante": None, "portes": 4, "places": 5, "annees": "1956–1960"},
                    {"modele": "Versailles", "variante": None, "portes": 4, "places": 5, "annees": "1977–1980"},
                    {"modele": "Mark III", "variante": None, "portes": 2, "places": 4, "annees": "1969–1971"},
                    {"modele": "Mark V", "variante": None, "portes": 2, "places": 4, "annees": "1977–1979"},
                    {"modele": "Mark VII", "variante": None, "portes": 2, "places": 4, "annees": "1984–1992"},
                    {"modele": "Mark VIII", "variante": None, "portes": 2, "places": 4, "annees": "1993–1998"},

                    # Modèles récents / modernes
                    {"modele": "Town Car", "variante": None, "portes": 4, "places": 5, "annees": "1981–2011"},
                    {"modele": "LS", "variante": None, "portes": 4, "places": 5, "annees": "2000–2006"},
                    {"modele": "Aviator", "variante": None, "portes": 5, "places": 6, "annees": "2003–présent"},
                    {"modele": "Blackwood", "variante": None, "portes": 4, "places": 5, "annees": "2002"},
                    {"modele": "MKC", "variante": None, "portes": 5, "places": 5, "annees": "2015–2019"},
                    {"modele": "Nautilus", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "Corsair", "variante": None, "portes": 5, "places": 5, "annees": "2019–présent"},
                    {"modele": "Zephyr (nouvelle génération)", "variante": None, "portes": 4, "places": 5,
                     "annees": "2006–présent"},
                    {"modele": "Navigator", "variante": None, "portes": 5, "places": 7, "annees": "1998–présent"},
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

                "Lucid": [
                    # Modèles historiques / anciens
                    {"modele": "Lucid Air Pure", "variante": "Berline électrique", "portes": 4, "places": 5,
                     "annees": "2022–présent"},
                    {"modele": "Lucid Air Touring", "variante": "Berline électrique", "portes": 4, "places": 5,
                     "annees": "2022–présent"},
                    {"modele": "Lucid Air Grand Touring", "variante": "Berline électrique", "portes": 4, "places": 5,
                     "annees": "2022–présent"},
                    {"modele": "Lucid Air Sapphire", "variante": "Berline électrique", "portes": 4, "places": 5,
                     "annees": "2023–présent"},

                    # Modèles récents / actuels
                    {"modele": "Lucid Gravity Touring", "variante": "SUV électrique", "portes": 5, "places": 5,
                     "annees": "2025–présent"},
                    {"modele": "Lucid Gravity Grand Touring", "variante": "SUV électrique", "portes": 5, "places": 7,
                     "annees": "2025–présent"},
                ],

                "Mahindra": [
                    # Modèles historiques / anciens
                    {"modele": "Bolero Classic", "variante": None, "portes": 5, "places": 7, "annees": "2000–2020"},
                    {"modele": "TUV300", "variante": None, "portes": 5, "places": 5, "annees": "2015–2020"},
                    {"modele": "XUV500", "variante": None, "portes": 5, "places": 7, "annees": "2011–2021"},
                    {"modele": "KUV100", "variante": None, "portes": 5, "places": 5, "annees": "2016–2022"},

                    # Modèles récents / actuels
                    {"modele": "Bolero Neo", "variante": None, "portes": 5, "places": 7, "annees": "2021–présent"},
                    {"modele": "XUV 3XO", "variante": None, "portes": 5, "places": 5, "annees": "2024–présent"},
                    {"modele": "XUV 7XO", "variante": None, "portes": 5, "places": 7, "annees": "2026–présent"},
                    {"modele": "Scorpio-N", "variante": None, "portes": 5, "places": 7, "annees": "2022–présent"},
                    {"modele": "Thar ROXX", "variante": None, "portes": 5, "places": 5, "annees": "2024–présent"},
                    {"modele": "BE6", "variante": None, "portes": 5, "places": 5, "annees": "2024–présent"},
                    {"modele": "BE6 Formula E", "variante": "Edition spéciale", "portes": 5, "places": 5,
                     "annees": "2025–présent"},
                    {"modele": "XEV 9S", "variante": None, "portes": 5, "places": 7, "annees": "2025–présent"},
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

                "Mercury": [
                    # Modèles historiques / anciens
                    {"modele": "Mercury Eight", "variante": None, "portes": 4, "places": 5, "annees": "1939–1951"},
                    {"modele": "Turnpike Cruiser", "variante": None, "portes": 4, "places": 5, "annees": "1957–1958"},
                    {"modele": "Montclair", "variante": None, "portes": 4, "places": 5, "annees": "1955–1960"},
                    {"modele": "Medalist", "variante": None, "portes": 4, "places": 5, "annees": "1956–1958"},
                    {"modele": "Monterey", "variante": None, "portes": 4, "places": 5, "annees": "1950–1974"},
                    {"modele": "S‑55", "variante": None, "portes": 2, "places": 5, "annees": "1962–1967"},
                    {"modele": "Monarch", "variante": None, "portes": 4, "places": 5, "annees": "1975–1980"},
                    {"modele": "Cougar", "variante": None, "portes": 2, "places": 4, "annees": "1967–2002"},
                    # 2‑portes généralement :contentReference[oaicite:1]{index=1}

                    # Modèles plus récents avant fin de production
                    {"modele": "Grand Marquis", "variante": None, "portes": 4, "places": 5, "annees": "1975–2011"},
                    {"modele": "Sable", "variante": None, "portes": 4, "places": 5, "annees": "1986–2009"},
                    {"modele": "Milan", "variante": None, "portes": 4, "places": 5, "annees": "2006–2011"},
                    {"modele": "Montego", "variante": None, "portes": 4, "places": 5, "annees": "2005–2007"},
                    {"modele": "Mariner", "variante": None, "portes": 5, "places": 5, "annees": "2005–2010"},
                    {"modele": "Mountaineer", "variante": None, "portes": 5, "places": 7, "annees": "1997–2010"},
                    {"modele": "Capri", "variante": None, "portes": 2, "places": 4, "annees": "1970–1994"},
                    {"modele": "Tracer", "variante": None, "portes": 4, "places": 5, "annees": "1987–1999"},
                    {"modele": "Villager", "variante": None, "portes": 5, "places": 7, "annees": "1993–2002"},
                ],

                "MG": [
                    # Modèles historiques / anciens (classiques britanniques)
                    {"modele": "MG Midget", "variante": None, "portes": 2, "places": 2, "annees": "1961–1979"},
                    {"modele": "MGA", "variante": None, "portes": 2, "places": 2, "annees": "1955–1962"},
                    {"modele": "MGB", "variante": None, "portes": 2, "places": 4, "annees": "1962–1980"},
                    {"modele": "MG TD", "variante": None, "portes": 2, "places": 2, "annees": "1950–1953"},
                    {"modele": "MG TF", "variante": None, "portes": 2, "places": 2, "annees": "2002–2005"},
                    {"modele": "MG Metro", "variante": None, "portes": 5, "places": 5, "annees": "1982–1990"},
                    {"modele": "MG ZR", "variante": None, "portes": 5, "places": 5, "annees": "2001–2005"},
                    {"modele": "MG XPower SV", "variante": None, "portes": 2, "places": 2, "annees": "2004–2005"},

                    # Modèles récents / actuels (sous propriété SAIC Motor)
                    {"modele": "MG3", "variante": None, "portes": 5, "places": 5, "annees": "2008–présent"},
                    {"modele": "MG4 EV", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2022–présent"},
                    {"modele": "MG5", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},
                    {"modele": "MG GT", "variante": None, "portes": 4, "places": 5, "annees": "2014–2019"},
                    {"modele": "MG6", "variante": None, "portes": 4, "places": 5, "annees": "2009–présent"},
                    {"modele": "MG7", "variante": None, "portes": 4, "places": 5, "annees": "2007–présent"},
                    {"modele": "MG ZS", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "MG ZS EV", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2018–présent"},
                    {"modele": "MG HS", "variante": None, "portes": 5, "places": 5, "annees": "2018–présent"},
                    {"modele": "MG HS PHEV", "variante": "Hybride", "portes": 5, "places": 5, "annees": "2019–présent"},
                    {"modele": "MGS5 EV", "variante": "Électrique SUV", "portes": 5, "places": 5, "annees": "2025–présent"},
                    {"modele": "MGS6 EV", "variante": "Électrique SUV", "portes": 5, "places": 5, "annees": "2025–présent"},
                    {"modele": "MG Cyberster", "variante": "Roadster électrique", "portes": 2, "places": 2,
                     "annees": "2023–présent"},
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
                    {"modele": "Mitsubishi Lancer Evolution", "variante": None, "portes": 4, "places": 5,"annees": "1992–2016"}
                ],

                "Morgan": [
                    # Modèles historiques / anciens
                    {"modele": "Morgan 4/4", "variante": None, "portes": 2, "places": 2, "annees": "1936–présent"},
                    {"modele": "Morgan Plus 4", "variante": None, "portes": 2, "places": 2, "annees": "1950–2020"},
                    {"modele": "Morgan Plus 4 Plus", "variante": "Coupé rare", "portes": 2, "places": 2,
                     "annees": "1964–1967"},  # très limitée :contentReference[oaicite:0]{index=0}
                    {"modele": "Morgan Plus 8", "variante": None, "portes": 2, "places": 2, "annees": "1968–2018"},
                    # classique V8 :contentReference[oaicite:1]{index=1}
                    {"modele": "Morgan Aero 8", "variante": None, "portes": 2, "places": 2, "annees": "2001–2018"},
                    # sport moderne :contentReference[oaicite:2]{index=2}

                    # Modèles récents / actuels
                    {"modele": "Morgan Plus Four", "variante": None, "portes": 2, "places": 2, "annees": "2020–présent"},
                    # actuel roadster :contentReference[oaicite:3]{index=3}
                    {"modele": "Morgan Plus Six", "variante": None, "portes": 2, "places": 2, "annees": "2019–2025"},
                    # remplace la Plus 8 :contentReference[oaicite:4]{index=4}
                    {"modele": "Morgan Super 3", "variante": "Tricycle", "portes": 0, "places": 1,
                     "annees": "2019–présent"},  # tricycle motorisé :contentReference[oaicite:5]{index=5}
                    {"modele": "Morgan Supersport", "variante": None, "portes": 2, "places": 2, "annees": "2025–présent"},
                    # nouveau roadster :contentReference[oaicite:6]{index=6}
                ],

                "Moskvitch": [
                    # Modèles historiques / anciens
                    {"modele": "Moskvitch 400/401", "variante": None, "portes": 4, "places": 5, "annees": "1946–1956"},
                    {"modele": "Moskvitch 402/403", "variante": None, "portes": 4, "places": 5, "annees": "1956–1965"},
                    {"modele": "Moskvitch 407", "variante": None, "portes": 4, "places": 5, "annees": "1958–1963"},
                    {"modele": "Moskvitch 408", "variante": None, "portes": 4, "places": 5, "annees": "1964–1976"},
                    {"modele": "Moskvitch 410", "variante": None, "portes": 4, "places": 5, "annees": "1957–1961"},
                    {"modele": "Moskvitch 411", "variante": "Break", "portes": 5, "places": 5, "annees": "1958–1961"},
                    {"modele": "Moskvitch 412", "variante": None, "portes": 4, "places": 5, "annees": "1967–1976"},
                    {"modele": "Moskvitch 426", "variante": "Break", "portes": 5, "places": 5, "annees": "1966–1976"},
                    {"modele": "Moskvitch 2140", "variante": None, "portes": 4, "places": 5, "annees": "1976–1988"},
                    {"modele": "Moskvitch 2141 Aleko", "variante": "Hatchback", "portes": 5, "places": 5,
                     "annees": "1986–2001"},
                    {"modele": "Moskvitch 2142", "variante": None, "portes": 4, "places": 5, "annees": "1998–2002"},

                    # Modèles récents / modernes (après renaissance de la marque)
                    {"modele": "Moskvitch 3", "variante": None, "portes": 5, "places": 5, "annees": "2022–présent"},
                    {"modele": "Moskvitch 3e", "variante": "Électrique", "portes": 5, "places": 5,
                     "annees": "2022–présent"},
                    {"modele": "Moskvitch 3 Comfort", "variante": "Confort", "portes": 5, "places": 5,
                     "annees": "2023–présent"},
                    {"modele": "Moskvitch 5", "variante": None, "portes": 5, "places": 5, "annees": "2024–présent"},
                    {"modele": "Moskvitch 6", "variante": None, "portes": 5, "places": 5, "annees": "2023–présent"},
                    {"modele": "Moskvitch 8", "variante": None, "portes": 5, "places": 7, "annees": "2024–présent"},
                ],

                "NIO": [
                    # Modèles électriques principaux
                    {"modele": "NIO ES8", "variante": None, "portes": 5, "places": 7, "annees": "2018–présent"},
                    {"modele": "NIO ES7", "variante": None, "portes": 5, "places": 5, "annees": "2022–présent"},
                    {"modele": "NIO EC7", "variante": "Coupé SUV", "portes": 5, "places": 5, "annees": "2023–présent"},
                    {"modele": "NIO ES6", "variante": None, "portes": 5, "places": 5, "annees": "2019–présent"},
                    {"modele": "NIO EC6", "variante": "Coupé SUV", "portes": 5, "places": 5, "annees": "2020–présent"},
                    {"modele": "NIO ET7", "variante": None, "portes": 4, "places": 5, "annees": "2022–présent"},
                    {"modele": "NIO ET5", "variante": None, "portes": 4, "places": 5, "annees": "2022–présent"},
                    {"modele": "NIO ET5 Touring", "variante": "Break", "portes": 5, "places": 5, "annees": "2023–présent"},

                    # Modèles plus récents / à venir
                    {"modele": "NIO ET9", "variante": "Flagship sedan", "portes": 4, "places": 5, "annees": "2025–présent"},
                    {"modele": "NIO ES9", "variante": None, "portes": 5, "places": 7, "annees": "2026–présent"},
                    # grand SUV flagship :contentReference[oaicite:0]{index=0}

                    # Modèles complémentaires de la gamme Firefly
                    {"modele": "NIO Firefly", "variante": None, "portes": 5, "places": 5, "annees": "2025–présent"},
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
                    {"modele": "Leaf Nismo RC", "variante": "Electrique", "portes": 2, "places": 2, "reservoir": 0},
                    {"modele": "Skyline GT-R Nismo", "variante": None, "portes": 2, "places": 4, "reservoir": 75},


                ],

                "Oldsmobile": [
                    # Modèles très anciens / historiques
                    {"modele": "Oldsmobile Curved Dash", "variante": None, "portes": 2, "places": 2, "annees": "1901–1907"},
                    {"modele": "Oldsmobile Series 20", "variante": None, "portes": 4, "places": 5, "annees": "1909"},
                    {"modele": "Oldsmobile Light Eight", "variante": None, "portes": 4, "places": 5, "annees": "1916–1923"},

                    # Modèles classiques/milieu de siècle
                    {"modele": "Oldsmobile 88", "variante": None, "portes": 4, "places": 5, "annees": "1949–1999"},
                    # gamme populaire full‑size :contentReference[oaicite:0]{index=0}
                    {"modele": "Oldsmobile 98", "variante": None, "portes": 4, "places": 5, "annees": "1940–1996"},
                    # flagship full‑size :contentReference[oaicite:1]{index=1}
                    {"modele": "Oldsmobile F‑85", "variante": None, "portes": 4, "places": 5, "annees": "1961–1967"},
                    {"modele": "Oldsmobile Starfire", "variante": None, "portes": 2, "places": 4, "annees": "1961–1966"},
                    {"modele": "Oldsmobile Vista Cruiser", "variante": None, "portes": 5, "places": 7,
                     "annees": "1964–1977"},
                    {"modele": "Oldsmobile Cutlass", "variante": None, "portes": 2, "places": 4, "annees": "1964–1977"},
                    {"modele": "Oldsmobile Cutlass Supreme", "variante": None, "portes": 4, "places": 5,
                     "annees": "1967–1997"},
                    {"modele": "Oldsmobile 442", "variante": None, "portes": 2, "places": 4, "annees": "1968–1987"},
                    {"modele": "Oldsmobile Toronado", "variante": None, "portes": 2, "places": 4, "annees": "1966–1992"},
                    {"modele": "Oldsmobile Custom Cruiser", "variante": None, "portes": 5, "places": 7,
                     "annees": "1971–1992"},
                    {"modele": "Oldsmobile Omega", "variante": None, "portes": 4, "places": 5, "annees": "1973–1984"},

                    # Modèles des années 1980‑1990
                    {"modele": "Oldsmobile Cutlass Ciera", "variante": None, "portes": 4, "places": 5,
                     "annees": "1982–1996"},
                    {"modele": "Oldsmobile Cutlass Calais", "variante": None, "portes": 2, "places": 4,
                     "annees": "1985–1991"},  # aussi berline selon version :contentReference[oaicite:2]{index=2}
                    {"modele": "Oldsmobile Firenza", "variante": None, "portes": 3, "places": 5, "annees": "1982–1988"},
                    {"modele": "Oldsmobile Touring Sedan", "variante": None, "portes": 4, "places": 5,
                     "annees": "1987–1993"},
                    {"modele": "Oldsmobile Bravada", "variante": None, "portes": 5, "places": 5, "annees": "1991–2004"},
                    {"modele": "Oldsmobile Silhouette", "variante": None, "portes": 5, "places": 7, "annees": "1990–2004"},
                    {"modele": "Oldsmobile Achieva", "variante": None, "portes": 4, "places": 5, "annees": "1992–1998"},
                    {"modele": "Oldsmobile Intrigue", "variante": None, "portes": 4, "places": 5, "annees": "1998–2002"},
                    {"modele": "Oldsmobile Aurora", "variante": None, "portes": 4, "places": 5, "annees": "1995–2003"},
                    {"modele": "Oldsmobile Alero", "variante": None, "portes": 4, "places": 5, "annees": "1999–2004"},
                ],
                "Opel": [
                    # Modèles historiques / anciens
                    {"modele": "Opel 1.2 Liter", "variante": None, "portes": 2, "places": 4, "annees": "1935–1937"},
                    {"modele": "Opel Kadett", "variante": None, "portes": 2, "places": 4, "annees": "1936–1940"},
                    {"modele": "Opel Olympia", "variante": None, "portes": 4, "places": 5, "annees": "1935–1953"},
                    {"modele": "Opel Rekord", "variante": None, "portes": 4, "places": 5, "annees": "1953–1986"},
                    {"modele": "Opel GT", "variante": None, "portes": 2, "places": 2, "annees": "1968–1973"},
                    {"modele": "Opel Manta", "variante": None, "portes": 2, "places": 4, "annees": "1970–1988"},

                    # Modèles des années 1980‑1990
                    {"modele": "Opel Kadett E", "variante": None, "portes": 3, "places": 5, "annees": "1984–1991"},
                    {"modele": "Opel Astra F", "variante": None, "portes": 3, "places": 5, "annees": "1991–1998"},
                    {"modele": "Opel Vectra A", "variante": None, "portes": 4, "places": 5, "annees": "1988–1995"},
                    {"modele": "Opel Omega A", "variante": None, "portes": 4, "places": 5, "annees": "1986–1993"},

                    # Modèles récents / modernes
                    {"modele": "Opel Astra", "variante": None, "portes": 5, "places": 5, "annees": "1998–présent"},
                    {"modele": "Opel Corsa", "variante": None, "portes": 5, "places": 5, "annees": "1982–présent"},
                    {"modele": "Opel Insignia", "variante": None, "portes": 4, "places": 5, "annees": "2008–présent"},
                    {"modele": "Opel Mokka", "variante": None, "portes": 5, "places": 5, "annees": "2012–présent"},
                    {"modele": "Opel Crossland", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "Opel Grandland", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "Opel Zafira", "variante": None, "portes": 5, "places": 7, "annees": "1999–2019"},

                    # Modèles électriques / hybrides
                    {"modele": "Opel Ampera", "variante": None, "portes": 4, "places": 5, "annees": "2011–2015"},
                    {"modele": "Opel Ampera-e", "variante": None, "portes": 5, "places": 5, "annees": "2017–2020"},
                    {"modele": "Opel Corsa-e", "variante": "Électrique", "portes": 5, "places": 5,
                     "annees": "2020–présent"},
                    {"modele": "Opel Mokka-e", "variante": "Électrique", "portes": 5, "places": 5,
                     "annees": "2020–présent"},
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

                "Pontiac": [
                    # Modèles classiques / anciens
                    {"modele": "Pontiac Torpedo", "variante": None, "portes": 4, "places": 5, "annees": "1940–1948"},
                    {"modele": "Pontiac Streamliner", "variante": None, "portes": 4, "places": 5, "annees": "1941–1952"},
                    {"modele": "Pontiac Chieftain", "variante": None, "portes": 4, "places": 5, "annees": "1949–1958"},
                    {"modele": "Pontiac Catalina", "variante": None, "portes": 2, "places": 5, "annees": "1950–1981"},
                    {"modele": "Pontiac Bonneville", "variante": None, "portes": 4, "places": 5, "annees": "1957–2005"},
                    {"modele": "Pontiac Star Chief", "variante": None, "portes": 4, "places": 5, "annees": "1954–1966"},

                    # Modèles muscle cars et sportives
                    {"modele": "Pontiac GTO", "variante": None, "portes": 2, "places": 4, "annees": "1964–1974"},
                    {"modele": "Pontiac Firebird", "variante": None, "portes": 2, "places": 4, "annees": "1967–2002"},
                    {"modele": "Pontiac Trans Am", "variante": None, "portes": 2, "places": 4, "annees": "1969–2002"},
                    {"modele": "Pontiac Fiero", "variante": None, "portes": 2, "places": 2, "annees": "1984–1988"},
                    {"modele": "Pontiac Grand Prix", "variante": None, "portes": 4, "places": 5, "annees": "1962–2008"},
                    {"modele": "Pontiac Sunfire", "variante": None, "portes": 2, "places": 4, "annees": "1995–2005"},

                    # Modèles compacts et crossover
                    {"modele": "Pontiac Vibe", "variante": None, "portes": 5, "places": 5, "annees": "2002–2009"},
                    {"modele": "Pontiac Aztek", "variante": None, "portes": 5, "places": 5, "annees": "2001–2005"},
                    {"modele": "Pontiac Torrent", "variante": None, "portes": 5, "places": 7, "annees": "2005–2009"},

                    # Petites voitures / compactes
                    {"modele": "Pontiac G3", "variante": None, "portes": 5, "places": 5, "annees": "2006–2009"},
                    {"modele": "Pontiac Wave", "variante": None, "portes": 5, "places": 5, "annees": "2004–2007"},
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

                "Ram": [
                    # Pickups classiques et récents
                    {"modele": "Ram 1500", "variante": None, "portes": 2, "places": 3, "annees": "1981–présent"},
                    {"modele": "Ram 1500 Quad Cab", "variante": None, "portes": 4, "places": 5, "annees": "2002–présent"},
                    {"modele": "Ram 1500 Crew Cab", "variante": None, "portes": 4, "places": 5, "annees": "1994–présent"},
                    {"modele": "Ram 2500", "variante": None, "portes": 2, "places": 3, "annees": "1994–présent"},
                    {"modele": "Ram 2500 Mega Cab", "variante": None, "portes": 4, "places": 5, "annees": "2006–présent"},
                    {"modele": "Ram 3500", "variante": None, "portes": 2, "places": 3, "annees": "1994–présent"},
                    {"modele": "Ram 3500 Mega Cab", "variante": None, "portes": 4, "places": 5, "annees": "2006–présent"},

                    # Versions électriques / modernes
                    {"modele": "Ram 1500 REV", "variante": "Électrique", "portes": 4, "places": 5,
                     "annees": "2024–présent"},

                    # Modèles classiques / historiques
                    {"modele": "Ramcharger", "variante": None, "portes": 2, "places": 5, "annees": "1974–1993"},
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

                "Rivian": [
                    # Pickups et SUV électriques
                    {"modele": "Rivian R1T", "variante": None, "portes": 4, "places": 5, "annees": "2021–présent"},
                    {"modele": "Rivian R1S", "variante": None, "portes": 5, "places": 7, "annees": "2021–présent"},

                    # Éditions limitées / spéciales
                    {"modele": "Rivian R1T Launch Edition", "variante": "Launch Edition", "portes": 4, "places": 5,
                     "annees": "2021–2022"},
                    {"modele": "Rivian R1S Launch Edition", "variante": "Launch Edition", "portes": 5, "places": 7,
                     "annees": "2021–2022"},
                ],

                "Rover": [
                    # Modèles historiques / classiques
                    {"modele": "Rover 10", "variante": None, "portes": 4, "places": 5, "annees": "1927–1947"},
                    {"modele": "Rover 14", "variante": None, "portes": 4, "places": 5, "annees": "1924–1948"},
                    {"modele": "Rover P4", "variante": None, "portes": 4, "places": 5, "annees": "1949–1964"},
                    {"modele": "Rover P5", "variante": None, "portes": 4, "places": 5, "annees": "1958–1973"},
                    {"modele": "Rover P6", "variante": None, "portes": 4, "places": 5, "annees": "1963–1977"},

                    # Modèles récents / Rover classique moderne
                    {"modele": "Rover 200", "variante": None, "portes": 3, "places": 5, "annees": "1984–1999"},
                    {"modele": "Rover 400", "variante": None, "portes": 4, "places": 5, "annees": "1990–1999"},
                    {"modele": "Rover 600", "variante": None, "portes": 4, "places": 5, "annees": "1993–1999"},
                    {"modele": "Rover 75", "variante": None, "portes": 4, "places": 5, "annees": "1998–2005"},

                    # SUV / 4x4
                    {"modele": "Rover Streetwise", "variante": None, "portes": 5, "places": 5, "annees": "2003–2005"},
                    {"modele": "Rover SD1", "variante": None, "portes": 5, "places": 5, "annees": "1976–1986"},
                ],
                "Saab": [
                    # Modèles historiques / anciens
                    {"modele": "Saab 92", "variante": None, "portes": 2, "places": 4, "annees": "1949–1956"},
                    {"modele": "Saab 93", "variante": None, "portes": 2, "places": 4, "annees": "1955–1960"},
                    {"modele": "Saab 95", "variante": None, "portes": 5, "places": 7, "annees": "1959–1978"},
                    {"modele": "Saab 96", "variante": None, "portes": 2, "places": 4, "annees": "1960–1980"},

                    # Modèles populaires / classiques
                    {"modele": "Saab 99", "variante": None, "portes": 2, "places": 5, "annees": "1968–1984"},
                    {"modele": "Saab 900", "variante": None, "portes": 3, "places": 5, "annees": "1978–1993"},
                    {"modele": "Saab 9000", "variante": None, "portes": 4, "places": 5, "annees": "1984–1998"},

                    # Modèles récents / modernes
                    {"modele": "Saab 9-3", "variante": None, "portes": 4, "places": 5, "annees": "1998–2014"},
                    {"modele": "Saab 9-3 Convertible", "variante": None, "portes": 2, "places": 4, "annees": "2003–2014"},
                    {"modele": "Saab 9-5", "variante": None, "portes": 4, "places": 5, "annees": "1997–2012"},


                    {"modele": "9-3", "variante": None, "portes": 5, "places": 5, "reservoir": 55},

                    {"modele": "Saab 9-3 EV", "variante": "Électrique", "portes": 4, "places": 5, "annees": "2010–2011"},
                ],
                "SAIC": [
                    # Marques sous SAIC : Roewe / MG
                    # Roewe - berlines et SUV
                    {"modele": "Roewe 350", "variante": None, "portes": 4, "places": 5, "annees": "2009–2014"},
                    {"modele": "Roewe 550", "variante": None, "portes": 4, "places": 5, "annees": "2008–2014"},
                    {"modele": "Roewe 750", "variante": None, "portes": 4, "places": 5, "annees": "2006–2016"},
                    {"modele": "Roewe RX5", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},
                    {"modele": "Roewe i6", "variante": None, "portes": 4, "places": 5, "annees": "2017–présent"},

                    # MG (rachetée par SAIC) - berlines, SUV et électriques
                    {"modele": "MG3", "variante": None, "portes": 5, "places": 5, "annees": "2003–présent"},
                    {"modele": "MG ZS", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "MG ZS EV", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2019–présent"},
                    {"modele": "MG5 EV", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2020–présent"},
                    {"modele": "MG6", "variante": None, "portes": 4, "places": 5, "annees": "2011–présent"},
                    {"modele": "MG7", "variante": None, "portes": 4, "places": 5, "annees": "2007–2014"},

                    # SUV / crossovers électriques
                    {"modele": "MG HS", "variante": None, "portes": 5, "places": 5, "annees": "2018–présent"},
                    {"modele": "MG Marvel R", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2020–présent"},
                    {"modele": "MG4 EV", "variante": "Électrique", "portes": 5, "places": 5, "annees": "2022–présent"},
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
                "Simca": [
                    # Modèles historiques / anciens
                    {"modele": "Simca 8", "variante": None, "portes": 4, "places": 5, "annees": "1937–1951"},
                    {"modele": "Simca 9 Aronde", "variante": None, "portes": 4, "places": 5, "annees": "1951–1964"},
                    {"modele": "Simca 1000", "variante": None, "portes": 4, "places": 5, "annees": "1961–1978"},
                    {"modele": "Simca 1100", "variante": None, "portes": 5, "places": 5, "annees": "1967–1982"},
                    {"modele": "Simca 1301", "variante": None, "portes": 4, "places": 5, "annees": "1966–1975"},
                    {"modele": "Simca 1307/1308", "variante": None, "portes": 4, "places": 5, "annees": "1975–1980"},

                    # Coupés / sportives
                    {"modele": "Simca 1200S", "variante": None, "portes": 2, "places": 4, "annees": "1961–1966"},
                    {"modele": "Simca 1000 Coupé", "variante": None, "portes": 2, "places": 4, "annees": "1962–1969"},

                    # Modèles utilitaires légers
                    {"modele": "Simca Cargo", "variante": None, "portes": 2, "places": 3, "annees": "1965–1980"},
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

                "Smart": [
                    # Modèles classiques / anciens
                    {"modele": "Smart City-Coupe", "variante": None, "portes": 2, "places": 2, "annees": "1998–2007"},
                    {"modele": "Smart City-Cabrio", "variante": None, "portes": 2, "places": 2, "annees": "2000–2007"},

                    # Modèles modernes / électriques
                    {"modele": "Smart Fortwo", "variante": None, "portes": 2, "places": 2, "annees": "1998–présent"},
                    {"modele": "Smart Fortwo Cabrio", "variante": None, "portes": 2, "places": 2, "annees": "2000–présent"},
                    {"modele": "Smart Forfour", "variante": None, "portes": 4, "places": 4, "annees": "2004–présent"},

                    # Électriques / Smart EQ
                    {"modele": "Smart EQ Fortwo", "variante": "Électrique", "portes": 2, "places": 2,
                     "annees": "2017–présent"},
                    {"modele": "Smart EQ Forfour", "variante": "Électrique", "portes": 4, "places": 4,
                     "annees": "2017–présent"},
                ],
                "SsangYong": [
                    # SUV et 4x4 historiques / anciens
                    {"modele": "SsangYong Korando", "variante": None, "portes": 3, "places": 5, "annees": "1983–présent"},
                    {"modele": "SsangYong Musso", "variante": None, "portes": 4, "places": 5, "annees": "1993–2005"},
                    {"modele": "SsangYong Rexton", "variante": None, "portes": 5, "places": 5, "annees": "2001–présent"},
                    {"modele": "SsangYong Actyon", "variante": None, "portes": 5, "places": 5, "annees": "2005–2011"},

                    # Modèles récents / SUV et crossover
                    {"modele": "SsangYong Tivoli", "variante": None, "portes": 5, "places": 5, "annees": "2015–présent"},
                    {"modele": "SsangYong XLV", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},
                    {"modele": "SsangYong Korando e-Motion", "variante": "Électrique", "portes": 5, "places": 5,
                     "annees": "2021–présent"},

                    # Pickups
                    {"modele": "SsangYong Musso Grand", "variante": None, "portes": 4, "places": 5,
                     "annees": "2018–présent"},
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

                "Talbot": [
                    # Modèles historiques / anciens
                    {"modele": "Talbot-Lago T26", "variante": None, "portes": 4, "places": 5, "annees": "1947–1959"},
                    {"modele": "Talbot-Lago T15", "variante": None, "portes": 4, "places": 5, "annees": "1935–1950"},
                    {"modele": "Talbot Express", "variante": None, "portes": 4, "places": 2, "annees": "1981–1995"},

                    # Modèles récents / compactes
                    {"modele": "Talbot Samba", "variante": None, "portes": 3, "places": 4, "annees": "1981–1986"},
                    {"modele": "Talbot Horizon", "variante": None, "portes": 5, "places": 5, "annees": "1978–1987"},
                    {"modele": "Talbot Solara", "variante": None, "portes": 4, "places": 5, "annees": "1980–1986"},

                    # Berlines / sportives
                    {"modele": "Talbot Tagora", "variante": None, "portes": 4, "places": 5, "annees": "1980–1983"},
                    {"modele": "Talbot Lago Sport", "variante": None, "portes": 2, "places": 2, "annees": "1948–1953"},
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

                "Tata": [
                    # Modèles historiques / anciens
                    {"modele": "Tata Sierra", "variante": None, "portes": 3, "places": 5, "annees": "1991–2003"},
                    {"modele": "Tata Estate", "variante": None, "portes": 5, "places": 5, "annees": "1992–2000"},
                    {"modele": "Tata Telcoline", "variante": None, "portes": 2, "places": 5, "annees": "1988–2006"},

                    # Compactes / citadines
                    {"modele": "Tata Indica", "variante": None, "portes": 5, "places": 5, "annees": "1998–2018"},
                    {"modele": "Tata Indigo", "variante": None, "portes": 4, "places": 5, "annees": "2002–2012"},

                    # SUV / crossovers
                    {"modele": "Tata Safari", "variante": None, "portes": 5, "places": 7, "annees": "1998–présent"},
                    {"modele": "Tata Harrier", "variante": None, "portes": 5, "places": 7, "annees": "2018–présent"},
                    {"modele": "Tata Nexon", "variante": None, "portes": 5, "places": 5, "annees": "2017–présent"},
                    {"modele": "Tata Nexon EV", "variante": "Électrique", "portes": 5, "places": 5,
                     "annees": "2020–présent"},

                    # Pickups / utilitaires
                    {"modele": "Tata Xenon", "variante": None, "portes": 2, "places": 5, "annees": "2006–2015"},
                ],

                "Tatra": [
                    # Modèles historiques / anciens
                    {"modele": "Tatra 11", "variante": None, "portes": 2, "places": 2, "annees": "1923–1927"},
                    {"modele": "Tatra 12", "variante": None, "portes": 2, "places": 2, "annees": "1926–1933"},
                    {"modele": "Tatra 77", "variante": None, "portes": 4, "places": 4, "annees": "1934–1938"},
                    {"modele": "Tatra 87", "variante": None, "portes": 4, "places": 4, "annees": "1936–1950"},
                    {"modele": "Tatra 97", "variante": None, "portes": 2, "places": 4, "annees": "1936–1939"},

                    # Modèles récents / camions et utilitaires
                    {"modele": "Tatra T815", "variante": None, "portes": 2, "places": 3, "annees": "1983–présent"},
                    {"modele": "Tatra Phoenix", "variante": None, "portes": 2, "places": 3, "annees": "2007–présent"},
                ],

                "UAZ": [
                    # Modèles historiques / anciens
                    {"modele": "UAZ 450", "variante": None, "portes": 2, "places": 4, "annees": "1958–1965"},
                    {"modele": "UAZ 469", "variante": None, "portes": 4, "places": 5, "annees": "1971–2003"},

                    # Modèles récents / SUV et utilitaires
                    {"modele": "UAZ Hunter", "variante": None, "portes": 3, "places": 5, "annees": "2003–présent"},
                    {"modele": "UAZ Patriot", "variante": None, "portes": 5, "places": 7, "annees": "2005–présent"},
                    {"modele": "UAZ Pickup", "variante": None, "portes": 2, "places": 3, "annees": "2008–présent"},
                    {"modele": "UAZ Profi", "variante": None, "portes": 2, "places": 3, "annees": "2015–présent"},
                ],

                "Venturi": [
                    # Modèles historiques / anciens
                    {"modele": "Venturi 260", "variante": None, "portes": 2, "places": 2, "annees": "1984–1994"},
                    {"modele": "Venturi 400 GT", "variante": None, "portes": 2, "places": 2, "annees": "1992–1995"},
                    {"modele": "Venturi Atlantique", "variante": None, "portes": 2, "places": 2, "annees": "1991–2000"},

                    # Modèles récents / électriques
                    {"modele": "Venturi Buckeye Bullet", "variante": None, "portes": 2, "places": 2,
                     "annees": "2010–présent"},
                    {"modele": "Venturi VBB-3", "variante": None, "portes": 2, "places": 1, "annees": "2016–présent"},
                    {"modele": "Venturi Atlantique 300 Biturbo", "variante": None, "portes": 2, "places": 2,
                     "reservoir": 80},
                    {"modele": "Venturi Fétish", "variante": "Électrique", "portes": 2, "places": 2, "reservoir": 0},
                    {"modele": "Venturi Volage", "variante": "Électrique", "portes": 2, "places": 2, "reservoir": 0},
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




                "Wartburg": [
                    # Modèles historiques / anciens
                    {"modele": "Wartburg 311", "variante": None, "portes": 4, "places": 5, "annees": "1956–1965"},
                    {"modele": "Wartburg 312", "variante": None, "portes": 4, "places": 5, "annees": "1965–1967"},
                    {"modele": "Wartburg 353", "variante": None, "portes": 4, "places": 5, "annees": "1966–1988"},
                    {"modele": "Wartburg 1.3", "variante": None, "portes": 4, "places": 5, "annees": "1988–1991"},

                    # Modèles particuliers / dérivés
                    {"modele": "Wartburg Tourist", "variante": None, "portes": 2, "places": 2, "annees": "1961–1988"},
                    {"modele": "Wartburg Kombi", "variante": None, "portes": 4, "places": 5, "annees": "1966–1988"},
                ],
                "Wuling": [
                    # Modèles populaires / citadines et mini-vans
                    {"modele": "Wuling Hongguang", "variante": None, "portes": 5, "places": 7, "annees": "2010–présent"},
                    {"modele": "Wuling Hongguang S", "variante": None, "portes": 5, "places": 7, "annees": "2013–présent"},
                    {"modele": "Wuling Hongguang Mini EV", "variante": "Électrique", "portes": 3, "places": 4,
                     "annees": "2020–présent"},
                    {"modele": "Wuling Baojun 510", "variante": None, "portes": 5, "places": 5, "annees": "2016–présent"},
                    {"modele": "Wuling Victory", "variante": None, "portes": 5, "places": 7, "annees": "2020–présent"},

                    # Pickups et utilitaires
                    {"modele": "Wuling Rongguang", "variante": None, "portes": 2, "places": 5, "annees": "2008–présent"},
                ],
                "XPeng": [
                    # Berlines électriques
                    {"modele": "XPeng P7", "variante": None, "portes": 4, "places": 5, "annees": "2020–présent"},
                    {"modele": "XPeng P5", "variante": None, "portes": 4, "places": 5, "annees": "2021–présent"},

                    # SUV électriques
                    {"modele": "XPeng G3", "variante": None, "portes": 5, "places": 5, "annees": "2018–2023"},
                    {"modele": "XPeng G6", "variante": None, "portes": 5, "places": 5, "annees": "2023–présent"},
                    {"modele": "XPeng G9", "variante": None, "portes": 5, "places": 5, "annees": "2023–présent"},
                ],
                "ZIL": [
                    # Modèles historiques / voitures de luxe et limousines
                    {"modele": "ZIL-111", "variante": None, "portes": 4, "places": 6, "annees": "1958–1967"},
                    {"modele": "ZIL-114", "variante": None, "portes": 4, "places": 6, "annees": "1967–1978"},
                    {"modele": "ZIL-115", "variante": None, "portes": 4, "places": 6, "annees": "1978–1989"},
                    {"modele": "ZIL-4104", "variante": None, "portes": 4, "places": 6, "annees": "1985–1994"},

                    # Camions et utilitaires
                    {"modele": "ZIL-130", "variante": None, "portes": 2, "places": 3, "annees": "1962–1994"},
                    {"modele": "ZIL-131", "variante": None, "portes": 2, "places": 3, "annees": "1966–1990"},
                    {"modele": "ZIL-133", "variante": None, "portes": 2, "places": 3, "annees": "1975–1991"},
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















                "Genesis": [

                    {"modele": "G70", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 60},
                    {"modele": "G80", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 73},
                    {"modele": "G90", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 83},


                    {"modele": "Genesis Coupe", "variante": "Coupe", "portes": 2, "places": 4, "reservoir": 65},


                    {"modele": "GV70", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 66},
                    {"modele": "GV80", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 80},

                    {"modele": "GV60", "variante": "SUV Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "G80 Electrified", "variante": "Sedan Electrique", "portes": 4, "places": 5, "reservoir": 0}
                ],
                "Genesis G70 Sport": [
                    {"modele": "G70", "variante": "Sport", "portes": 4, "places": 5, "reservoir": 60}
                ],


                # Chine
                "Geely": [

                    {"modele": "Emgrand EC7", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Emgrand GT", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 55},
                    {"modele": "Vision", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Binrui", "variante": "Sedan", "portes": 4, "places": 5, "reservoir": 50},
                    {"modele": "Panda", "variante": "Hatchback", "portes": 5, "places": 4, "reservoir": 35},


                    {"modele": "Boyue", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Atlas", "variante": "SUV", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "Xingyue", "variante": "SUV Coupé", "portes": 5, "places": 5, "reservoir": 60},
                    {"modele": "GX3", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "Coolray", "variante": "SUV Compact", "portes": 5, "places": 5, "reservoir": 45},
                    {"modele": "Okavango", "variante": "SUV 7 places", "portes": 5, "places": 7, "reservoir": 60},


                    {"modele": "Geometry A", "variante": "Sedan Electrique", "portes": 4, "places": 5, "reservoir": 0},
                    {"modele": "Geometry C", "variante": "SUV Electrique", "portes": 5, "places": 5, "reservoir": 0},
                    {"modele": "Panda Mini EV", "variante": "Citadine Electrique", "portes": 3, "places": 4, "reservoir": 0}
                ],
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
                    obj, created = VoitureModele.objects.update_or_create(
                        voiture_marque=marque_obj,
                        nom_modele=m["modele"],
                        nom_variante=m.get("variante"),
                        defaults={
                            "nombre_portes": m.get("portes", 5),
                            "nbre_places": m.get("places", 5),
                            "taille_reservoir": m.get("reservoir", 50),
                            "societe": tenant  # obligatoire pour ton modèle
                        }
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} modèles ajoutés ou mis à jour pour le tenant '{tenant.schema_name}'"
        ))