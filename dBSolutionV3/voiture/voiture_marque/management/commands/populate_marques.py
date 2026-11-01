from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from societe.models import Societe
from voiture.voiture_marque.models import VoitureMarque


class Command(BaseCommand):
    help = "Ajoute les marques automobiles mondiales depuis 1950 pour le tenant 'dbsolution'"

    def handle(self, *args, **options):
        try:
            tenant = Societe.objects.get(schema_name='dbsolution')
        except Societe.DoesNotExist:
            self.stdout.write(self.style.ERROR("Tenant 'dbsolution' introuvable !"))
            return

        marques = [
            # 🇫🇷 France
            "Peugeot", "Renault", "Citroën", "DS Automobiles", "Alpine",
            "Bugatti", "Simca", "Talbot", "Venturi", "Volkswagen R",
            # Pionniers (1890-1919)
            "Panhard", "De Dion-Bouton", "Bollée", "Mors", "Darracq", "Delahaye",
            "Delage", "Hotchkiss", "Clément-Bayard", "Lorraine-Dietrich", "Berliet",
            "Unic", "Chenard-Walcker", "Brasier", "Georges Richard", "Rochet-Schneider",
            "Turcat-Méry", "Sizaire-Naudin", "Le Zèbre", "La Licorne", "Gobron-Brillié",
            "Decauville", "Delaunay-Belleville", "Charron", "Cottin & Desgouttes",
            "Vinot-Deguingand",
            # Entre-deux-guerres
            "Voisin", "Salmson", "Amilcar", "Ballot", "Bignan", "Donnet", "Tracta",
            "Mathis", "Rosengart", "Talbot-Lago", "Matford",
            # Après-guerre (1945-1979)
            "Facel Vega", "DB", "CG", "Monica", "Matra", "Ligier", "Vespa", "Willème",
            "Saviem", "Bernard", "Sovam", "Heuliez",
            # Années 1980 à aujourd'hui
            "Aixam", "Microcar", "Chatenet", "Bellier", "Mega", "Hommell", "PGO",
            "De la Chapelle", "Dangel", "Gruau", "Renault Trucks", "Bluecar",
            "Mia Electric", "Hopium",

            # 🇩🇪 Allemagne
            "Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Porsche",
            "Opel", "Maybach", "Smart", "Borgward", "Wartburg",
            # Pionniers (1886-1919)
            "Benz", "Daimler", "Horch", "Wanderer", "Adler", "Stoewer", "Brennabor",
            "Dürkopp", "Protos", "NAG", "Dixi", "Hansa", "Komnick", "Presto",
            # Entre-deux-guerres
            "Auto Union", "DKW", "NSU", "Hanomag", "Tempo", "Goliath", "Lloyd",
            # Après-guerre (1945-1990)
            "Glas", "Gutbrod", "Messerschmitt", "Heinkel", "Zündapp", "Veritas",
            "Amphicar", "Trabant", "IFA", "EMW", "Barkas", "Melkus", "Multicar",
            # Préparateurs et sportives
            "Alpina", "AMG", "Brabus", "Ruf", "Gemballa", "9ff", "Isdera", "Lotec",
            "Wiesmann", "Gumpert", "Apollo", "Artega", "Mercedes-Maybach",
            # Électriques et nouvelles marques
            "Sono Motors", "e.GO Mobile", "StreetScooter",
            # Utilitaires, camions et autocars
            "MAN", "Büssing", "Magirus-Deutz", "Krupp", "Henschel", "Faun", "Setra",
            "Kässbohrer", "Neoplan", "Unimog", "Vidal & Sohn",

            # 🇮🇹 Italie
            "Fiat", "Alfa Romeo", "Lancia", "Ferrari", "Lamborghini",
            "Maserati", "Pagani", "Abarth", "De Tomaso", "Innocenti",

            # 🇬🇧 Royaume-Uni
            "Jaguar", "Land Rover", "Range Rover", "Mini", "Rolls-Royce",
            "Bentley", "Aston Martin", "Lotus", "MG", "Rover",
            "Morgan", "TVR", "Triumph",

            # 🇪🇸 Espagne
            "SEAT", "Cupra", "Hispano-Suiza",

            # 🇸🇪 Suède
            "Volvo", "Saab", "Koenigsegg", "Polestar",

            # 🇯🇵 Japon
            "Toyota", "Lexus", "Nissan", "Infiniti", "Honda", "Acura",
            "Mazda", "Subaru", "Mitsubishi", "Suzuki", "Isuzu", "Daihatsu",

            # 🇰🇷 Corée du Sud
            "Hyundai", "Kia", "Genesis", "Daewoo", "SsangYong",

            # 🇺🇸 États-Unis
            "Ford", "Chevrolet", "Cadillac", "Buick", "GMC", "Chrysler",
            "Dodge", "Jeep", "Tesla", "Lincoln", "Pontiac",
            "Oldsmobile", "Mercury", "Hummer", "Ram",
            # Pionniers (1890-1919)
            "Duryea", "Winton", "Haynes-Apperson", "Apperson", "Locomobile", "Stanley",
            "White", "Packard", "Pierce-Arrow", "Peerless", "Thomas", "Knox", "Pope",
            "Columbia", "Stevens-Duryea", "Franklin", "Studebaker", "Rambler", "Maxwell",
            "Hupmobile", "Marmon", "Mercer", "Stutz", "Simplex", "Chalmers", "Hudson",
            "Overland", "Cole", "Moon", "Paige", "Reo", "Saxon", "Scripps-Booth",
            "Velie", "Jeffery", "Kissel", "Lozier", "Matheson", "Chandler", "Jordan",
            "Dort", "Auburn", "Duesenberg", "Oakland", "Brush", "Cartercar", "Holsman",
            "Detroit Electric", "Baker Electric", "Riker", "Doble", "Owen Magnetic",
            "Premier", "National", "Regal", "Elmore", "Case", "Essex",
            # Entre-deux-guerres (1920-1945)
            "DeSoto", "Plymouth", "LaSalle", "Cord", "Graham-Paige", "Graham",
            "Durant", "Star", "Flint", "Rickenbacker", "Wills Sainte Claire", "Gardner",
            "Willys", "Whippet", "Erskine", "Rockne", "Viking", "Marquette",
            "Terraplane", "Lafayette", "Nash", "American Bantam", "Crosley",
            "Stout Scarab", "Checker",
            # Après-guerre (1945-1979)
            "Kaiser", "Frazer", "Henry J", "Tucker", "Muntz", "Cunningham", "Kurtis",
            "Nash-Healey", "Edsel", "Imperial", "Continental", "Allstate", "Metropolitan",
            "AMC", "International Harvester", "Scout", "Avanti", "Excalibur", "Shelby",
            "Clénet", "Zimmer",
            # Années 1980 à aujourd'hui
            "DeLorean", "Eagle", "Geo", "Saturn", "Vector", "Mosler", "Panoz",
            "Callaway", "Saleen", "Hennessey", "SSC", "Rossion", "Anteros", "Equus",
            "Falcon", "Rezvani", "Czinger", "Drako", "Lyons",
            # Électriques et nouvelles marques
            "Rivian", "Lucid", "Fisker", "Karma", "Canoo", "Lordstown", "Aptera",
            "Faraday Future", "Bollinger", "Scout Motors", "Workhorse", "Nikola",
            "Zap", "GEM", "Elio",
            # Utilitaires, camions et militaires
            "Mack", "Peterbilt", "Kenworth", "Freightliner", "International", "Navistar",
            "Western Star", "Autocar", "Diamond T", "Sterling", "Oshkosh", "AM General",
            "Federal", "FWD",

            # 🇨🇳 Chine
            "Geely", "BYD", "Chery", "Great Wall", "Haval", "NIO",
            "XPeng", "Li Auto", "Wuling", "SAIC", "Hongqi",

            # 🇷🇺 URSS / Russie
            "Lada", "GAZ", "UAZ", "Moskvitch", "ZIL",

            # 🇮🇳 Inde
            "Tata", "Mahindra", "Hindustan Motors",

            # 🇨🇿 Tchéquie
            "Skoda", "Tatra",

            # 🇧🇪 Belgique
            # Pionniers (1895-1919)
            "Minerva", "FN", "Métallurgique", "Excelsior", "Germain", "Nagant",
            "Pipe", "Vivinus", "Miesse", "Fondu", "Dasse", "Delin", "Jenatzy",
            "Pieper", "Springuel", "Auto-Mixte", "Linon", "Hermes", "Belgica",
            # Entre-deux-guerres
            "Imperia", "Vanden Plas", "D'Ieteren",
            # Artisans et sportives (depuis 1960)
            "Méan", "Apal", "Edran", "ADK", "Gillet",
            # Autocars, camions et motos
            "Van Hool", "Jonckheere", "LAG", "Brossel", "Saroléa", "Gillet Herstal",

            # 🇷🇴 Roumanie
            "Dacia",

            "Radical",
            # 🇮🇷 Iran
            "Iran Khodro", "SAIPA",

            # 🇧🇷 Brésil
            "Gurgel",

            # 🇦🇺 Australie
            "Holden",

            # 🌍 Marques mondiales / électriques
            "Polestar",
            "VinFast", "Aiways"
        ]

        created_count = 0

        with tenant_context(tenant):
            for marque in marques:
                # ✅ associer nom et societe dans le get_or_create
                _, created = VoitureMarque.objects.get_or_create(
                    nom_marque=marque,
                    societe=tenant  # obligatoire si societe_id est NOT NULL
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created_count} marques ajoutées avec succès pour le tenant '{tenant.schema_name}'"
        ))

