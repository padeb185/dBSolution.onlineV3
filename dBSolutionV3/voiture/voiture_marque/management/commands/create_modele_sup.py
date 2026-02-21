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

            "Venturi": [
                {"modele": "Venturi 400 GT", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Venturi 260", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Venturi Atlantique 300", "variante": None, "portes": 2, "places": 2, "reservoir": 80},
                {"modele": "Venturi Atlantique 300 Biturbo", "variante": None, "portes": 2, "places": 2,
                 "reservoir": 80},
                {"modele": "Venturi Fétish", "variante": "Électrique", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Venturi Volage", "variante": "Électrique", "portes": 2, "places": 2, "reservoir": 0},
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

            "Nissan Nismo": [
                {"modele": "370Z Nismo", "variante": None, "portes": 2, "places": 2, "reservoir": 72},
                {"modele": "GT-R Nismo", "variante": None, "portes": 2, "places": 4, "reservoir": 74},
                {"modele": "Juke Nismo", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "Juke Nismo RS", "variante": None, "portes": 5, "places": 5, "reservoir": 50},
                {"modele": "March Nismo", "variante": None, "portes": 3, "places": 4, "reservoir": 41},
                {"modele": "Leaf Nismo RC", "variante": "Electrique", "portes": 2, "places": 2, "reservoir": 0},
                {"modele": "Skyline GT-R Nismo", "variante": None, "portes": 2, "places": 4, "reservoir": 75},
                {"modele": "Note Nismo", "variante": None, "portes": 5, "places": 5, "reservoir": 46}
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
            "Dodge SRT": [
                {"modele": "Challenger SRT Hellcat", "variante": None, "portes": 2, "places": 4, "reservoir": 70},
                {"modele": "Challenger SRT Hellcat Redeye", "variante": None, "portes": 2, "places": 4,
                 "reservoir": 70},
                {"modele": "Challenger SRT Demon", "variante": None, "portes": 2, "places": 2, "reservoir": 70},
                {"modele": "Charger SRT Hellcat", "variante": None, "portes": 4, "places": 5, "reservoir": 70},
                {"modele": "Durango SRT", "variante": None, "portes": 5, "places": 7, "reservoir": 85}
            ]
















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
