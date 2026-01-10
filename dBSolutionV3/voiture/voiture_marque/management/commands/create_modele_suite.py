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
                {"modele": "Range Rover Evoque", "variante": "Autobiography", "portes": 5, "places": 5, "reservoir": 60}
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
                {"modele": "Peugeot 9X8", "variante": "PEUGEOT Hypercar 9X8", "portes": 2, "places": 2, "reservoir": 0}
            ],

            "Porsche": [

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



        "Fiat": [
                {"modele": "500", "variante": "Pop", "portes": 3, "places": 4, "reservoir": 35},
                {"modele": "Panda", "variante": "City", "portes": 5, "places": 5, "reservoir": 40},
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


            "BMW M": [
                {"modele": "M3 E30", "variante": "Coupe", "portes": 2, "places": 4,"reservoir": 60},
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
                {"modele": "X7 M G07", "variante": "SUV", "portes": 5, "places": 7, "reservoir": 85}
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



        "Lancia": [
                {"modele": "Ypsilon", "variante": "Gold", "portes": 5, "places": 5, "reservoir": 40},
            ],
                       "Pagani": [
                {"modele": "Huayra", "variante": None, "portes": 2, "places": 2, "reservoir": 90},
            ],
            "De Tomaso": [
                {"modele": "Pantera", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
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
                {"modele": "Ghost", "variante": None, "portes": 4, "places": 5, "reservoir": 90},
                {"modele": "Cullinan", "variante": None, "portes": 5, "places": 5, "reservoir": 105},
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
