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
                {
                    "modele": "Range Rover",
                    "variantes": [
                        "Base / Vogue",
                        "Autobiography",
                        "SV Autobiography",
                        "SV Autobiography Dynamic",
                        "Long Wheelbase (LWB)"
                    ]
                },
                {
                    "modele": "Range Rover Sport",
                    "variantes": [
                        "S",
                        "SE",
                        "Dynamic SE",
                        "Dynamic HSE",
                        "Autobiography",
                        "SVR",
                        "SV Carbon"
                    ]
                },
                {
                    "modele": "Range Rover Velar",
                    "variantes": [
                        "Standard",
                        "R‑Dynamic S",
                        "R‑Dynamic SE",
                        "R‑Dynamic HSE"
                    ]
                },
                {
                    "modele": "Range Rover Evoque",
                    "variantes": [
                        "S",
                        "Dynamic SE",
                        "Dynamic HSE",
                        "Autobiography"
                    ]
                }
            ],


            "Polestar": [
                {
                    "modele": "Polestar 1",
                    "variantes": [
                        "Standard"
                    ]
                },
                {
                    "modele": "Polestar 2",
                    "variantes": [
                        "Standard Range Single Motor",
                        "Long Range Single Motor",
                        "Long Range Dual Motor",
                        "Long Range Dual Motor Performance"
                    ]
                },
                {
                    "modele": "Polestar 3",
                    "variantes": [
                        "Base",
                        "Dual Motor",
                        "Performance"
                    ]
                },
                {
                    "modele": "Polestar 4",
                    "variantes": [
                        "Standard",
                        "Plus Pack",
                        "Pilot Pack"
                    ]
                },
                {
                    "modele": "Polestar 5",
                    "variantes": [
                        "Dual Motor",
                        "Performance"
                    ]
                },
                {
                    "modele": "Polestar 6",
                    "variantes": [
                        "Roadster Standard"
                    ]
                },
                {
                    "modele": "Polestar 7",
                    "variantes": [
                        "Standard"
                    ]
                }
            ],
            "Peugeot Sport": [
                {
                    "modele": "Peugeot 205",
                    "variantes": [
                        "GTI 1.6",
                        "GTI 1.9"
                    ]
                },
                {
                    "modele": "Peugeot 206",
                    "variantes": [
                        "GTI",
                        "RC",
                        "S16",
                        "206 Rallye"
                    ]
                },
                {
                    "modele": "Peugeot 207",
                    "variantes": [
                        "GTi",
                        "RC",
                        "207 S2000"
                    ]
                },
                {
                    "modele": "Peugeot 208",
                    "variantes": [
                        "GTi 30th Anniversary",
                        "GTi by Peugeot Sport",
                        "e‑208 GTi" # future / relance sport électrique
                    ]
                },
                {
                    "modele": "Peugeot 308",
                    "variantes": [
                        "GTi by Peugeot Sport"
                    ]
                },
                {
                    "modele": "Peugeot 508",
                    "variantes": [
                        "508 PEUGEOT SPORT ENGINEERED",
                        "508 SW PEUGEOT SPORT ENGINEERED"
                    ]
                },
                {
                    "modele": "Peugeot 9X8",
                    "variantes": [
                        "PEUGEOT Hypercar 9X8" # prototype endurance WEC
                    ]
                }
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
            "Bentley": [
                {"modele": "Continental GT", "variante": None, "portes": 2, "places": 4, "reservoir": 90},
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

            {"modele": "Clio II RS",
             "variantes": [
                 "Phase 1",
                 "Phase 2",
                 "RS 172",
                 "RS 182",
                 "V6 Phase 1",
                 "V6 Phase 2"
             ]
             },
            {"modele": "Clio III RS",
             "variantes": [
                 "Phase 1",
                 "Phase 2",
                 "Cup",
                 "Trophy",
                 "Gordini"
             ]
             },
            {"modele": "Clio IV RS",
             "variantes": [
                 "Phase 1",
                 "Phase 2",
                 "Trophy",
                 "Trophy R"
             ]
             },
            {"modele": "Megane II RS",
             "variantes": [
                 "Phase 1",
                 "Phase 2",
                 "R26 F1 Team",
                 "R26.R"
             ]
             },
            {"modele": "Megane III RS",
             "variantes": [
                 "Base",
                 "Trophy",
                 "Trophy‑R"
             ]
             },
            {"modele": "Megane IV RS",
             "variantes": [
                 "Base",
                 "Trophy",
                 "Trophy‑R",
                 "Ultime"
             ]
             },
            {"modele": "Twingo II RS",
             "variantes": [
                 "Phase 1",
                 "Phase 2",
                 "Gordini"
             ]
             },
            {"modele": "Renault Sport RS 01",
             "variantes": [
                 "RS 01 Standard"
             ]
             },


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

            "Alpine": [
                {"modele": "Alpine A110 RS", "variante": None, "portes": 2, "places": 2, "reservoir": 50},  # Alpine RS
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
            "Porsche": [
                {"modele": "550 Spyder", "nom_variante": None, "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 60},

                # 911 classiques
                {"modele": "911", "nom_variante": "Carrera S", "nombre_portes": 2, "nbre_places": 4,
                 "taille_reservoir": 67},
                {"modele": "911", "nom_variante": "Turbo", "nombre_portes": 2, "nbre_places": 4,
                 "taille_reservoir": 67},

                # 911 GT spéciaux
                {"modele": "911", "nom_variante": "GT3", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},
                {"modele": "911", "nom_variante": "GT3 RS", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},
                {"modele": "911", "nom_variante": "GT2 RS", "nombre_portes": 2, "nbre_places": 2,
                 "taille_reservoir": 64},

                # SUV et berlines
                {"modele": "Cayenne", "nom_variante": "S", "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 75},
                {"modele": "Macan", "nom_variante": None, "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 60},
                {"modele": "Panamera", "nom_variante": "4S", "nombre_portes": 5, "nbre_places": 5,
                 "taille_reservoir": 75},

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
