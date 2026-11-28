# -*- coding: utf-8 -*-
"""
Référentiel UNIQUE des modèles de voitures (généré, trié par marque puis modèle, sans doublons).

Fusion de : create_modele, create_modele_all, create_modele_suite, create_modele_sup,
create_modele_abarth (+ copies par tenant) et des modèles des marques ajoutées le 01/11/2026.

Clés possibles par modèle (seule « modele » est obligatoire) :
  modele, generation (ex. "R50"), phase (ex. "1", "2", "Facelift"), variante (ex. "One 3 portes"),
  portes (0/2/3/4/5), places, reservoir (litres, 0 = électrique/inconnu), batterie (kWh),
  annee_debut, mois_debut, annee_fin, mois_fin (vides = inconnu / encore produit),
  moteurs : liste de (motoriste, code_moteur) existant dans voiture_moteur (1..N moteurs par modèle),
  remarques.

Exemple :
  "Mini": [
      {"modele": "One", "generation": "R50", "phase": "1", "variante": "3 portes", "portes": 3,
       "places": 4, "reservoir": 50, "annee_debut": 2001, "mois_debut": 7, "annee_fin": 2004,
       "moteurs": [("Mini", "Tritec-1.6")]},
  ]
"""

MODELES = {
    '9ff': [
    ],
    'Abarth': [
    ],
    'Acura': [
    ],
    'ADK': [
    ],
    'Adler': [
    ],
    'Aiways': [
    ],
    'Aixam': [
    ],
    'Alfa Romeo': [
    ],
    'Allstate': [
    ],
    'Alpina': [
    ],
    'Alpine': [
    ],
    'AM General': [
    ],
    'AMC': [
    ],
    'American Bantam': [
    ],
    'AMG': [
        {"modele": 'C 36 AMG', "generation": 'W202', "variante": 'Berline', "portes": 4, "places": 5, "reservoir": 62, "annee_debut": 1993, "annee_fin": 1997},
        {"modele": 'CLK GTR', "variante": 'Supercar', "portes": 2, "places": 2, "annee_debut": 1998, "annee_fin": 1999},
        {"modele": 'E 60 AMG', "generation": 'W124', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1993, "annee_fin": 1995},
        {"modele": 'GT', "generation": 'C190', "variante": 'Coupé / Roadster', "portes": 2, "places": 2, "reservoir": 65, "annee_debut": 2014, "annee_fin": 2021},
        {"modele": 'GT Black Series', "generation": 'C190', "variante": 'Coupé', "portes": 2, "places": 2, "reservoir": 75, "annee_debut": 2020, "annee_fin": 2021},
        {"modele": 'Hammer', "generation": 'W124', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1986, "annee_fin": 1990},
        {"modele": 'ONE', "variante": 'Hypercar hybride', "portes": 2, "places": 2, "annee_debut": 2022, "annee_fin": 2024},
        {"modele": 'SLS AMG', "generation": 'C197', "variante": 'Coupé', "portes": 2, "places": 2, "reservoir": 85, "annee_debut": 2010, "annee_fin": 2014},
    ],
    'Amilcar': [
    ],
    'Amphicar': [
    ],
    'Anteros': [
    ],
    'Apal': [
    ],
    'Apollo': [
    ],
    'Apperson': [
    ],
    'Aptera': [
    ],
    'Artega': [
    ],
    'Aston Martin': [
    ],
    'Aston Martin Vantage': [
        {"modele": 'V8 Vantage S', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'V8 Vantage S', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage AMR', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage AMR', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage GT8', "variante": 'Edition Limitée', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage V8', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage V8', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Vantage V12', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 95},
        {"modele": 'Vantage V12', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 95},
    ],
    'Auburn': [
    ],
    'Audi': [
    ],
    'Audi RS': [
    ],
    'Audi S': [
    ],
    'Auto-Mixte': [
    ],
    'Auto Union': [
    ],
    'Autocar': [
    ],
    'Avanti': [
    ],
    'Baker Electric': [
    ],
    'Ballot': [
    ],
    'Barkas': [
    ],
    'Belgica': [
    ],
    'Bellier': [
    ],
    'Bentley': [
    ],
    'Benz': [
    ],
    'Berliet': [
    ],
    'Bernard': [
    ],
    'Bignan': [
    ],
    'Bluecar': [
    ],
    'BMW': [

    ],
    'BMW M': [
    ],
    'Bollée': [
    ],
    'Bollinger': [
    ],
    'Borgward': [
    ],
    'Brabham': [
    ],
    'Brabus': [
    ],
    'Brasier': [
    ],
    'Brennabor': [
    ],
    'Brossel': [
    ],
    'Brush': [
    ],
    'Bugatti': [
    ],
    'Buick': [
    ],
    'Büssing': [
    ],
    'BYD': [
    ],
    'Cadillac': [
    ],
    'Cadillac V-Series': [
    ],
    'Callaway': [
    ],
    'Canoo': [
    ],
    'Cartercar': [
    ],
    'Case': [
    ],
    'Caterham': [
    ],
    'CG': [
    ],
    'Chalmers': [
    ],
    'Chandler': [
    ],
    'Charron': [
    ],
    'Chatenet': [
    ],
    'Checker': [
    ],
    'Chenard-Walcker': [
    ],
    'Chery': [
    ],
    'Chevrolet': [
    ],
    'Chevrolet Camaro ZL1': [
    ],
    'Chevrolet Corvette': [
    ],
    'Chrysler': [
    ],
    'Citroën': [
    ],
    'Citroën Sport': [
    ],
    'Clément-Bayard': [
    ],
    'Clénet': [
    ],
    'Cole': [
    ],
    'Columbia': [
    ],
    'Continental': [
    ],
    'Cord': [
    ],
    'Cottin & Desgouttes': [
    ],
    'Crosley': [
    ],
    'Cunningham': [
    ],
    'Cupra': [
    ],
    'Czinger': [
    ],
    "D'Ieteren": [
    ],
    'Dacia': [
    ],
    'Daewoo': [
    ],
    'Daihatsu': [
    ],
    'Daimler': [
    ],
    'Dallara': [
    ],
    'Dangel': [
    ],
    'Darracq': [
    ],
    'Dasse': [
    ],
    'DB': [
    ],
    'De Dion-Bouton': [
    ],
    'De la Chapelle': [
    ],
    'De Tomaso': [
    ],
    'Decauville': [
    ],
    'Delage': [
    ],
    'Delahaye': [
    ],
    'Delaunay-Belleville': [
    ],
    'Delin': [
    ],
    'DeLorean': [
    ],
    'DeSoto': [
    ],
    'Detroit Electric': [
    ],
    'Diamond T': [
    ],
    'Dixi': [
    ],
    'DKW': [
    ],
    'Doble': [
        {"modele": 'Model D', "variante": 'Vapeur', "portes": 4, "places": 5, "annee_debut": 1922, "annee_fin": 1923, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model E', "variante": 'Vapeur', "portes": 4, "places": 5, "annee_debut": 1923, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Dodge': [
    ],
    'Dodge SRT': [
    ],
    'Donnet': [
    ],
    'Dort': [
    ],
    'Drako': [
    ],
    'DS Automobiles': [
    ],
    'Duesenberg': [
    ],
    'Durant': [
    ],
    'Dürkopp': [
    ],
    'Duryea': [
    ],
    'e.GO Mobile': [
        {"modele": 'e.GO Life', "variante": 'Citadine électrique', "portes": 3, "places": 4, "reservoir": 0, "annee_debut": 2019, "annee_fin": 2022},
        {"modele": 'e.GO Mover', "variante": 'Minibus électrique', "portes": 4, "places": 15, "reservoir": 0, "annee_debut": 2019},
    ],
    'Eagle': [
    ],
    'Edran': [
    ],
    'Edsel': [
    ],
    'Elio': [
    ],
    'Elmore': [
    ],
    'EMW': [
    ],
    'Equus': [
    ],
    'Erskine': [
    ],
    'Essex': [
    ],
    'Excalibur': [
    ],
    'Excelsior': [
    ],
    'Facel Vega': [
    ],
    'Falcon': [
    ],
    'Faraday Future': [
    ],
    'Faun': [
    ],
    'Federal': [
    ],
    'Ferrari': [
    ],
    'Fiat': [
    ],
    'Fisker': [
        {"modele": 'Fisker Project Ronin', "variante": 'Coupé Electrique', "portes": 2, "places": 2, "reservoir": 0},
        {"modele": 'Karma', "variante": 'Sedan Hybride', "portes": 4, "places": 4, "reservoir": 50},
        {"modele": 'Karma', "variante": 'Berline hybride rechargeable', "portes": 4, "places": 4, "reservoir": 35, "annee_debut": 2011, "annee_fin": 2012},
        {"modele": 'Ocean', "variante": 'SUV électrique', "portes": 5, "places": 5, "reservoir": 0, "annee_debut": 2023, "annee_fin": 2024},
    ],
    'Flint': [
        {"modele": 'Model 40', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1923, "annee_fin": 1924, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 55', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1924, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 80', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'FN': [
    ],
    'Fondu': [
    ],
    'Ford': [
    ],
    'Franklin': [
    ],
    'Frazer': [
    ],
    'Freightliner': [
    ],
    'FWD': [
    ],
    'Gardner': [
    ],
    'GAZ': [
    ],
    'Geely': [
    ],
    'GEM': [
    ],
    'Gemballa': [
    ],
    'Genesis': [
    ],
    'Genesis G70 Sport': [
    ],
    'Geo': [
    ],
    'Georges Richard': [
    ],
    'Germain': [
    ],
    'Gillet': [
    ],
    'Gillet Herstal': [
    ],
    'Ginetta': [
    ],
    'Glas': [
    ],
    'GMC': [
    ],
    'Gobron-Brillié': [
    ],
    'Goliath': [
    ],
    'Gordon Murray Automotive': [
    ],
    'Graham': [
    ],
    'Graham-Paige': [
    ],
    'Great Wall': [
    ],
    'Gruau': [
    ],
    'Gumpert': [
    ],
    'Gurgel': [
    ],
    'Gutbrod': [
    ],
    'Hanomag': [
    ],
    'Hansa': [
    ],
    'Haval': [
    ],
    'Haynes-Apperson': [
    ],
    'Heinkel': [
    ],
    'Hennessey': [
    ],
    'Henry J': [
    ],
    'Henschel': [
    ],
    'Hermes': [
    ],
    'Heuliez': [
    ],
    'Hindustan Motors': [
    ],
    'Hispano-Suiza': [
    ],
    'Holden': [
    ],
    'Holsman': [
    ],
    'Hommell': [
    ],
    'Honda': [
    ],
    'Honda S2000': [
    ],
    'Honda Type R': [
    ],
    'Hongqi': [
    ],
    'Hopium': [
    ],
    'Horch': [
    ],
    'Hotchkiss': [
    ],
    'Hudson': [
    ],
    'Hummer': [
    ],
    'Hupmobile': [
    ],
    'Hyundai': [
    ],
    'Hyundai N': [
    ],
    'IFA': [
    ],
    'Imperia': [
    ],
    'Imperial': [
    ],
    'Infiniti': [
    ],
    'Innocenti': [
    ],
    'International': [
    ],
    'International Harvester': [
    ],
    'Iran Khodro': [
    ],
    'Isdera': [
    ],
    'Isuzu': [
    ],
    'Jaguar': [
    ],
    'Jaguar R': [
    ],
    'Jeep': [
    ],
    'Jeffery': [
    ],
    'Jenatzy': [
    ],
    'Jonckheere': [
    ],
    'Jordan': [
    ],
    'Kaiser': [
    ],
    'Karma': [
    ],
    'Kässbohrer': [
    ],
    'Kenworth': [
    ],
    'Kia': [
    ],
    'Kia GT': [
    ],
    'Kissel': [
    ],
    'Knox': [
    ],
    'Koenigsegg': [
    ],
    'Komnick': [
    ],
    'Krupp': [
    ],
    'Kurtis': [
    ],
    'La Licorne': [
    ],
    'Lada': [
    ],
    'Lafayette': [
    ],
    'LAG': [
    ],
    'Lamborghini': [
    ],
    'Lancia': [
    ],
    'Lancia HF': [
    ],
    'Land Rover': [
    ],
    'LaSalle': [
    ],
    'Le Zèbre': [
    ],
    'Lexus': [
    ],
    'Li Auto': [
    ],
    'Ligier': [
    ],
    'Lincoln': [
    ],
    'Linon': [
    ],
    'Lloyd': [
    ],
    'Locomobile': [
    ],
    'Lola': [
    ],
    'Lordstown': [
    ],
    'Lorraine-Dietrich': [
    ],
    'Lotec': [
    ],
    'Lotus': [
    ],
    'Lotus Exige': [
    ],
    'Lozier': [
        {"modele": 'Model 77', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1913, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model H', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1907, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Lucid': [
    ],
    'Lyons': [
        {"modele": 'LM2 Streamliner', "variante": 'Hypercar (prototype)', "portes": 2, "places": 2, "annee_debut": 2015},
    ],
    'Mack': [
    ],
    'Magirus-Deutz': [
    ],
    'Mahindra': [
    ],
    'MAN': [
        {"modele": 'F8', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1971, "annee_fin": 1986},
        {"modele": 'F90', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1986, "annee_fin": 1994},
        {"modele": 'F2000', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1994, "annee_fin": 2000},
        {"modele": "Lion's City", "variante": 'Autobus', "portes": 2, "places": 100, "annee_debut": 1996},
        {"modele": "Lion's Coach", "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1996},
        {"modele": 'TGA', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 2000, "annee_fin": 2007},
        {"modele": 'TGE', "variante": 'Utilitaire', "portes": 4, "places": 3, "reservoir": 75, "annee_debut": 2017},
        {"modele": 'TGL', "variante": 'Camion', "portes": 2, "places": 3, "annee_debut": 2005},
        {"modele": 'TGM', "variante": 'Camion', "portes": 2, "places": 3, "annee_debut": 2005},
        {"modele": 'TGS', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 2007},
        {"modele": 'TGX', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2007},
    ],
    'Marcos': [
    ],
    'Marmon': [
    ],
    'Marquette': [
    ],
    'Maserati': [
    ],
    'Matford': [
    ],
    'Matheson': [
    ],
    'Mathis': [
    ],
    'Matra': [
    ],
    'Maxwell': [
    ],
    'Maybach': [
    ],
    'Mazda': [
    ],
    'Mazda Speed': [
    ],
    'McLaren': [
    ],
    'Méan': [
        {"modele": 'Sonora', "variante": 'Barquette', "portes": 0, "places": 2, "annee_debut": 1966, "annee_fin": 1972, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Mega': [
    ],
    'Melkus': [
    ],
    'Mercedes-AMG': [
        {"modele": 'AMG ONE', "variante": 'Hypercar', "portes": 2, "places": 2, "reservoir": 65},
        {"modele": 'C36', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 70},
        {"modele": 'C55', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 70},
        {"modele": 'C63', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 66},
        {"modele": 'C63 S', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 66},
        {"modele": 'CLK63', "variante": 'AMG', "portes": 2, "places": 4, "reservoir": 80},
        {"modele": 'E36', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 80},
        {"modele": 'E55', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 80},
        {"modele": 'E63', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 80},
        {"modele": 'E63 S', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 80},
        {"modele": 'GLC 63', "variante": 'AMG', "portes": 5, "places": 5, "reservoir": 66},
        {"modele": 'GLE 63', "variante": 'AMG', "portes": 5, "places": 5, "reservoir": 93},
        {"modele": 'GT', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'GT Black Series', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'GT C', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'GT R', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'S63', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 80},
        {"modele": 'S70', "variante": 'AMG', "portes": 4, "places": 5, "reservoir": 90},
        {"modele": 'SL55', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 90},
        {"modele": 'SL60', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'SL63', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'SLK55', "variante": 'AMG', "portes": 2, "places": 2, "reservoir": 60},
    ],
    'Mercedes-Benz': [
    ],
    'Mercer': [
    ],
    'Mercury': [
    ],
    'Messerschmitt': [
    ],
    'Métallurgique': [
        {"modele": '12 HP', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1903, "annee_fin": 1906, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": '15/20 HP', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1920, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": '26/60 HP', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1907, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Metropolitan': [
    ],
    'MG': [
    ],
    'Mia Electric': [
    ],
    'Microcar': [
    ],
    'Miesse': [
    ],
    'Minerva': [
    ],
    'Mini': [
        {"modele": 'Clubman', "portes": 5, "places": 4, "reservoir": 48},
        {"modele": 'Clubman', "variante": 'John Cooper Works', "portes": 5, "places": 4, "reservoir": 48},
        {"modele": 'Clubman', "variante": 'One', "portes": 5, "places": 4, "reservoir": 48},
        {"modele": 'Clubman', "variante": 'S', "portes": 5, "places": 4, "reservoir": 48},
        {"modele": 'Convertible', "portes": 2, "places": 4, "reservoir": 40},
        {"modele": 'Convertible', "variante": 'John Cooper Works', "portes": 2, "places": 4, "reservoir": 40},
        {"modele": 'Convertible', "variante": 'One', "portes": 2, "places": 4, "reservoir": 40},
        {"modele": 'Convertible', "variante": 'S', "portes": 2, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": '3 portes', "portes": 3, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": '5 portes', "portes": 5, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'John Cooper Works 3 portes', "portes": 3, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'John Cooper Works 5 portes', "portes": 5, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'One 3 portes', "portes": 3, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'One 5 portes', "portes": 5, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'S 3 portes', "portes": 3, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'S 5 portes', "portes": 5, "places": 4, "reservoir": 40},
        {"modele": 'Cooper', "variante": 'SE', "portes": 3, "places": 4, "reservoir": 40, "moteurs": [('Mini', 'Mini-EV')]},
        {"modele": 'Countryman', "portes": 5, "places": 5, "reservoir": 51},
        {"modele": 'Countryman', "variante": 'John Cooper Works', "portes": 5, "places": 5, "reservoir": 51},
        {"modele": 'Countryman', "variante": 'One', "portes": 5, "places": 5, "reservoir": 51},
        {"modele": 'Countryman', "variante": 'S', "portes": 5, "places": 5, "reservoir": 51},
        {"modele": 'Paceman', "portes": 3, "places": 4, "reservoir": 50},
        {"modele": 'Paceman', "variante": 'John Cooper Works', "portes": 3, "places": 4, "reservoir": 50},
        {"modele": 'Paceman', "variante": 'One', "portes": 3, "places": 4, "reservoir": 50},
        {"modele": 'Paceman', "variante": 'S', "portes": 3, "places": 4, "reservoir": 50},
    ],
    'Mitsubishi': [
    ],
    'Mitsubishi Evo': [
    ],
    'Monica': [
        {"modele": '560', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1973, "annee_fin": 1975},
    ],
    'Moon': [
        {"modele": 'Aerotype Eight', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1928, "annee_fin": 1930, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 30', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1906, "annee_fin": 1910, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Victory', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1918, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Morgan': [
    ],
    'Morgan Aero': [
    ],
    'Mors': [
        {"modele": '14/19 HP', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1908, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Dauphin', "variante": 'Course', "portes": 0, "places": 2, "annee_debut": 1902, "annee_fin": 1902, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Sans-soupapes', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1912, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type C', "variante": 'Tonneau', "portes": 0, "places": 4, "annee_debut": 1899, "annee_fin": 1901, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Moskvitch': [
        {"modele": 'Moskvitch 3', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'Moskvitch 3 Comfort', "variante": 'Confort', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'Moskvitch 3e', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'Moskvitch 5', "portes": 5, "places": 5, "annee_debut": 2024},
        {"modele": 'Moskvitch 6', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'Moskvitch 8', "portes": 5, "places": 7, "annee_debut": 2024},
        {"modele": 'Moskvitch 400/401', "portes": 4, "places": 5, "annee_debut": 1946, "annee_fin": 1956},
        {"modele": 'Moskvitch 402/403', "portes": 4, "places": 5, "annee_debut": 1956, "annee_fin": 1965},
        {"modele": 'Moskvitch 407', "portes": 4, "places": 5, "annee_debut": 1958, "annee_fin": 1963},
        {"modele": 'Moskvitch 408', "portes": 4, "places": 5, "annee_debut": 1964, "annee_fin": 1976},
        {"modele": 'Moskvitch 410', "portes": 4, "places": 5, "annee_debut": 1957, "annee_fin": 1961},
        {"modele": 'Moskvitch 411', "variante": 'Break', "portes": 5, "places": 5, "annee_debut": 1958, "annee_fin": 1961},
        {"modele": 'Moskvitch 412', "portes": 4, "places": 5, "annee_debut": 1967, "annee_fin": 1976},
        {"modele": 'Moskvitch 426', "variante": 'Break', "portes": 5, "places": 5, "annee_debut": 1966, "annee_fin": 1976},
        {"modele": 'Moskvitch 2140', "portes": 4, "places": 5, "annee_debut": 1976, "annee_fin": 1988},
        {"modele": 'Moskvitch 2141 Aleko', "variante": 'Hatchback', "portes": 5, "places": 5, "annee_debut": 1986, "annee_fin": 2001},
        {"modele": 'Moskvitch 2142', "portes": 4, "places": 5, "annee_debut": 1998, "annee_fin": 2002},
    ],
    'Mosler': [
        {"modele": 'MT900', "variante": 'Supercar', "portes": 2, "places": 2, "annee_debut": 2001, "annee_fin": 2011},
        {"modele": 'Raptor', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1993, "annee_fin": 1995},
    ],
    'Multicar': [
        {"modele": 'Fumo', "variante": 'Utilitaire', "portes": 2, "places": 3, "annee_debut": 2005},
        {"modele": 'M22', "variante": 'Utilitaire', "portes": 2, "places": 2, "annee_debut": 1964, "annee_fin": 1978},
        {"modele": 'M25', "variante": 'Utilitaire', "portes": 2, "places": 2, "annee_debut": 1978, "annee_fin": 1992},
        {"modele": 'M26', "variante": 'Utilitaire', "portes": 2, "places": 2, "annee_debut": 1992, "annee_fin": 2010},
        {"modele": 'Tremo', "variante": 'Utilitaire', "portes": 2, "places": 2, "annee_debut": 2010},
    ],
    'Muntz': [
        {"modele": 'Jet', "variante": 'Cabriolet', "portes": 2, "places": 4, "annee_debut": 1950, "annee_fin": 1954},
    ],
    'NAG': [
        {"modele": '212', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1927, "annee_fin": 1929, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C4', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1920, "annee_fin": 1924, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'D4', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1925, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Nagant': [
        {"modele": 'Gobron-Nagant', "variante": 'Voiturette', "portes": 0, "places": 2, "annee_debut": 1900, "annee_fin": 1903, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Nagant 10/12 HP', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1920, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type C', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1910, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Nash': [
        {"modele": '600', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1941, "annee_fin": 1949},
        {"modele": 'Advanced Six', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1930},
        {"modele": 'Airflyte', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1949, "annee_fin": 1951},
        {"modele": 'Ambassador', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1932, "annee_fin": 1957},
        {"modele": 'Model 681', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1918, "annee_fin": 1921},
        {"modele": 'Rambler', "variante": 'Berline / Break', "portes": 2, "places": 5, "annee_debut": 1950, "annee_fin": 1955},
        {"modele": 'Statesman', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1950, "annee_fin": 1956},
    ],
    'Nash-Healey': [
        {"modele": 'Le Mans Coupé', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1953, "annee_fin": 1954},
        {"modele": 'Roadster', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1951, "annee_fin": 1954},
    ],
    'National': [
        {"modele": 'Highway Six', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1918, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 40', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1911, "annee_fin": 1913, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Sextet', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1920, "annee_fin": 1924, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Navistar': [
        {"modele": 'MaxxForce', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 2007, "annee_fin": 2016},
        {"modele": 'MXT', "variante": 'Pick-up géant', "portes": 4, "places": 5, "annee_debut": 2006, "annee_fin": 2008},
    ],
    'Neoplan': [
        {"modele": 'Cityliner', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1971},
        {"modele": 'Jetliner', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1973},
        {"modele": 'Skyliner', "variante": 'Autocar à impériale', "portes": 2, "places": 80, "annee_debut": 1967},
        {"modele": 'Spaceliner', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1979, "annee_fin": 2009},
        {"modele": 'Tourliner', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 2004},
    ],
    'Nikola': [
        {"modele": 'Tre BEV', "variante": 'Tracteur routier électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2022, "annee_fin": 2025},
        {"modele": 'Tre FCEV', "variante": 'Tracteur routier hydrogène', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2023, "annee_fin": 2025},
    ],
    'NIO': [
        {"modele": 'NIO EC6', "variante": 'Coupé SUV', "portes": 5, "places": 5, "annee_debut": 2020},
        {"modele": 'NIO EC7', "variante": 'Coupé SUV', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'NIO ES6', "portes": 5, "places": 5, "annee_debut": 2019},
        {"modele": 'NIO ES7', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'NIO ES8', "portes": 5, "places": 7, "annee_debut": 2018},
        {"modele": 'NIO ES9', "portes": 5, "places": 7, "annee_debut": 2026},
        {"modele": 'NIO ET5', "portes": 4, "places": 5, "annee_debut": 2022},
        {"modele": 'NIO ET5 Touring', "variante": 'Break', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'NIO ET7', "portes": 4, "places": 5, "annee_debut": 2022},
        {"modele": 'NIO ET9', "variante": 'Flagship sedan', "portes": 4, "places": 5, "annee_debut": 2025},
        {"modele": 'NIO Firefly', "portes": 5, "places": 5, "annee_debut": 2025},
    ],
    'Nissan': [
    ],
    'Nissan Nismo': [
    ],
    'Noble': [
    ],
    'NSU': [
    ],
    'Oakland': [
        {"modele": 'Eight', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1930, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 34', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1916, "annee_fin": 1917, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model K', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1909, "annee_fin": 1910, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Six', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1924, "annee_fin": 1929, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Oldsmobile': [
    ],
    'Opel': [
    ],
    'Opel OPC': [
    ],
    'Oshkosh': [
        {"modele": 'HEMTT', "variante": 'Camion militaire', "portes": 2, "places": 2, "annee_debut": 1982},
        {"modele": 'L-ATV', "variante": 'Tout-terrain militaire (JLTV)', "portes": 4, "places": 4, "annee_debut": 2015},
        {"modele": 'M-ATV', "variante": 'Blindé tout-terrain', "portes": 4, "places": 5, "annee_debut": 2009},
        {"modele": 'NGDV', "variante": 'Utilitaire postal', "portes": 2, "places": 1, "annee_debut": 2023},
        {"modele": 'Striker', "variante": 'Véhicule pompier aéroport', "portes": 2, "places": 3, "annee_debut": 2002},
    ],
    'Overland': [
        {"modele": 'Model 4', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1919, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 69', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1910, "annee_fin": 1913, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 83', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1916, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 90', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1917, "annee_fin": 1920, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 91', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1923, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Owen Magnetic': [
        {"modele": 'Model 60', "variante": 'Berline', "portes": 4, "places": 7, "annee_debut": 1917, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model O', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1916, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Packard': [
    ],
    'Pagani': [
    ],
    'Paige': [
        {"modele": 'Daytona', "variante": 'Roadster', "portes": 2, "places": 3, "annee_debut": 1921, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 25', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1910, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Six-66', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1922, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Panhard': [
        {"modele": '6 CS', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1927, "annee_fin": 1934, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": '24 BT', "variante": 'Coupé 4 places', "portes": 2, "places": 4, "reservoir": 42, "annee_debut": 1964, "annee_fin": 1967, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": '24 CT', "variante": 'Coupé', "portes": 2, "places": 4, "reservoir": 42, "annee_debut": 1963, "annee_fin": 1967, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'CD', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1963, "annee_fin": 1965, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Dyna Junior', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1952, "annee_fin": 1956, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Dyna X', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1947, "annee_fin": 1953, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Dyna Z', "variante": 'Berline', "portes": 4, "places": 6, "reservoir": 40, "annee_debut": 1953, "annee_fin": 1959, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Dynamic', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1936, "annee_fin": 1940, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'PL 17', "variante": 'Berline', "portes": 4, "places": 6, "reservoir": 42, "annee_debut": 1959, "annee_fin": 1965, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type A', "variante": 'Voiturette', "portes": 0, "places": 2, "annee_debut": 1891, "annee_fin": 1895, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'X17', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1911, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'X19', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1912, "annee_fin": 1920, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Panhard Racing': [
        {"modele": '24 BT', "portes": 0, "places": 1, "reservoir": 60},
        {"modele": '24 CT', "portes": 0, "places": 1, "reservoir": 60},
        {"modele": 'Dyna X', "portes": 0, "places": 1, "reservoir": 60},
        {"modele": 'Panhard 24 CT', "portes": 2, "places": 4, "reservoir": 60},
        {"modele": 'Panhard CD', "portes": 2, "places": 2, "reservoir": 50},
        {"modele": 'Panhard LM64', "variante": 'Prototype', "portes": 0, "places": 1, "reservoir": 80},
        {"modele": 'Panhard X86', "variante": 'Prototype', "portes": 0, "places": 1, "reservoir": 80},
        {"modele": 'X85', "portes": 0, "places": 1, "reservoir": 60},
        {"modele": 'X88', "portes": 0, "places": 1, "reservoir": 60},
    ],
    'Panoz': [
        {"modele": 'Abruzzi', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 2011, "annee_fin": 2012},
        {"modele": 'Esperante', "variante": 'Coupé / Cabriolet', "portes": 2, "places": 2, "annee_debut": 2000, "annee_fin": 2007},
        {"modele": 'Roadster', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1989, "annee_fin": 1999},
    ],
    'Peerless': [
        {"modele": 'Green Dragon', "variante": 'Course', "portes": 0, "places": 1, "annee_debut": 1904, "annee_fin": 1904, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Master Eight', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 38-Six', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1911, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Peterbilt': [
        {"modele": '351', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1954, "annee_fin": 1976},
        {"modele": '359', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 1967, "annee_fin": 1987},
        {"modele": '379', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 1987, "annee_fin": 2007},
        {"modele": '389', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2007},
        {"modele": '520', "variante": 'Benne à ordures', "portes": 2, "places": 3, "annee_debut": 2014},
        {"modele": '567', "variante": 'Chantier', "portes": 2, "places": 2, "annee_debut": 2013},
        {"modele": '579', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2012},
    ],
    'Peugeot': [
        {"modele": '208', "variante": 'Active', "portes": 5, "places": 5, "reservoir": 45},
        {"modele": '508', "variante": 'Allure', "portes": 5, "places": 5, "reservoir": 55},
    ],
    'Peugeot Sport': [
    ],
    'PGO': [
        {"modele": 'Cévennes', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1998},
        {"modele": 'Hemera', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 2007},
        {"modele": 'Speedster II', "variante": 'Roadster', "portes": 0, "places": 2, "annee_debut": 2000},
    ],
    'Pieper': [
        {"modele": 'Auto-Mixte', "variante": 'Torpedo hybride', "portes": 4, "places": 4, "annee_debut": 1906, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Voiturette', "variante": 'Voiturette', "portes": 0, "places": 2, "annee_debut": 1899, "annee_fin": 1903, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Pierce-Arrow': [
        {"modele": 'Great Arrow', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1904, "annee_fin": 1909},
        {"modele": 'Model 66', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1910, "annee_fin": 1918},
        {"modele": 'Series 80', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1928},
        {"modele": 'Silver Arrow', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1933, "annee_fin": 1933},
        {"modele": 'Twelve', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1932, "annee_fin": 1938},
    ],
    'Pininfarina Battista': [
        {"modele": 'Battista', "variante": 'Roadster Concept', "portes": 2, "places": 2, "reservoir": 0},
        {"modele": 'Battista Anniversario', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 0},
        {"modele": 'Battista Anniversario N-Largo', "variante": 'Edition limitée', "portes": 2, "places": 2, "reservoir": 0},
        {"modele": 'Battista Anniversario Roadster', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 0},
    ],
    'Pipe': [
        {"modele": 'Type 15', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1920, "annee_fin": 1932, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type 15/20 HP', "variante": 'Tonneau', "portes": 0, "places": 4, "annee_debut": 1904, "annee_fin": 1907, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type 60 HP', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1907, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Plymouth': [
    ],
    'Polestar': [
    ],
    'Pontiac': [
    ],
    'Pope': [
        {"modele": 'Pope-Hartford Model 27', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1903, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Pope-Toledo', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1903, "annee_fin": 1909, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Pope-Waverley', "variante": 'Électrique', "portes": 0, "places": 2, "reservoir": 0, "annee_debut": 1903, "annee_fin": 1908, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Porsche': [
    ],
    'Premier': [
        {"modele": 'Model 6-60', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1910, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 6-D', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1919, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Presto': [
        {"modele": 'Typ D', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1921, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Typ F', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Protos': [
        {"modele": 'Typ C', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1920, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Typ E1', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1908, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Radical': [
    ],
    'Ram': [
    ],
    'Rambler': [
        {"modele": 'Ambassador', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1958, "annee_fin": 1965},
        {"modele": 'American', "variante": 'Berline / Break', "portes": 4, "places": 6, "annee_debut": 1958, "annee_fin": 1969},
        {"modele": 'Classic', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1961, "annee_fin": 1966},
        {"modele": 'Cross Country', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1910, "annee_fin": 1913},
        {"modele": 'Marlin', "variante": 'Fastback', "portes": 2, "places": 6, "annee_debut": 1965, "annee_fin": 1965},
        {"modele": 'Model 63', "variante": 'Runabout', "portes": 0, "places": 2, "annee_debut": 1902, "annee_fin": 1903},
        {"modele": 'Rambler', "variante": 'Berline / Break', "portes": 2, "places": 6, "annee_debut": 1950, "annee_fin": 1955},
        {"modele": 'Six / Rebel', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1957, "annee_fin": 1960},
    ],
    'Range Rover': [
    ],
    'Regal': [
        {"modele": 'Model T', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1912, "annee_fin": 1918, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Underslung', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1910, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Renault': [
        {"modele": 'Clio', "variante": 'Zen', "portes": 5, "places": 5, "reservoir": 40},
        {"modele": 'Megane', "variante": 'RS', "portes": 5, "places": 5, "reservoir": 55},
        {"modele": 'Talisman', "variante": 'Intens', "portes": 5, "places": 5, "reservoir": 60},
    ],
    'Renault RS': [
    ],
    'Renault Trucks': [
        {"modele": 'C', "variante": 'Chantier', "portes": 2, "places": 2, "annee_debut": 2013},
        {"modele": 'D', "variante": 'Distribution', "portes": 2, "places": 2, "annee_debut": 2013},
        {"modele": 'E-Tech D', "variante": 'Camion électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2020},
        {"modele": 'K', "variante": 'Chantier lourd', "portes": 2, "places": 2, "annee_debut": 2013},
        {"modele": 'Kerax', "variante": 'Chantier', "portes": 2, "places": 2, "annee_debut": 1997, "annee_fin": 2013},
        {"modele": 'Magnum', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 1990, "annee_fin": 2013},
        {"modele": 'Master', "variante": 'Utilitaire', "portes": 4, "places": 3, "annee_debut": 2013},
        {"modele": 'Midlum', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 2000, "annee_fin": 2014},
        {"modele": 'Premium', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1996, "annee_fin": 2013},
        {"modele": 'T', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2013},
    ],
    'Reo': [
        {"modele": 'Fifth', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1912, "annee_fin": 1915},
        {"modele": 'Flying Cloud', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1927, "annee_fin": 1936},
        {"modele": 'Royale', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1931, "annee_fin": 1934},
        {"modele": 'Runabout', "variante": 'Runabout', "portes": 0, "places": 2, "annee_debut": 1905, "annee_fin": 1907},
        {"modele": 'Speed Wagon', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1915, "annee_fin": 1953},
    ],
    'Rezvani': [
        {"modele": 'Beast', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 2014},
        {"modele": 'Tank', "variante": 'SUV', "portes": 5, "places": 5, "annee_debut": 2017},
    ],
    'Rickenbacker': [
        {"modele": 'Vertical Eight', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Vertical Six', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1922, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Riker': [
        {"modele": 'Electric Torpedo', "variante": 'Record électrique', "portes": 0, "places": 2, "reservoir": 0, "annee_debut": 1901, "annee_fin": 1901, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Electric Victoria', "variante": 'Électrique', "portes": 0, "places": 2, "reservoir": 0, "annee_debut": 1897, "annee_fin": 1900, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Rimac': [
    ],
    'Rivian': [
        {"modele": 'EDV', "variante": 'Utilitaire électrique', "portes": 2, "places": 1, "reservoir": 0, "annee_debut": 2021},
        {"modele": 'R1S', "variante": 'SUV électrique', "portes": 5, "places": 7, "reservoir": 0, "annee_debut": 2022},
        {"modele": 'R1T', "variante": 'Pick-up électrique', "portes": 4, "places": 5, "reservoir": 0, "annee_debut": 2021},
        {"modele": 'R2', "variante": 'SUV électrique', "portes": 5, "places": 5, "reservoir": 0, "annee_debut": 2026},
        {"modele": 'Rivian R1S', "portes": 5, "places": 7, "annee_debut": 2021},
        {"modele": 'Rivian R1S Launch Edition', "variante": 'Launch Edition', "portes": 5, "places": 7, "annee_debut": 2021, "annee_fin": 2022},
        {"modele": 'Rivian R1T', "portes": 4, "places": 5, "annee_debut": 2021},
        {"modele": 'Rivian R1T Launch Edition', "variante": 'Launch Edition', "portes": 4, "places": 5, "annee_debut": 2021, "annee_fin": 2022},
    ],
    'Rochet-Schneider': [
        {"modele": '15 HP', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1910, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type 14000', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1930, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Rockne': [
        {"modele": 'Model 65', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1932, "annee_fin": 1933, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 75', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1932, "annee_fin": 1933, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Rolls-Royce': [
    ],
    'Rosengart': [
        {"modele": 'Ariette', "variante": 'Berline', "portes": 2, "places": 4, "annee_debut": 1951, "annee_fin": 1952, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'LR2', "variante": 'Berline', "portes": 2, "places": 4, "annee_debut": 1928, "annee_fin": 1934, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'LR4', "variante": 'Berline / Cabriolet', "portes": 2, "places": 4, "annee_debut": 1932, "annee_fin": 1939, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Sagaie', "variante": 'Cabriolet', "portes": 2, "places": 2, "annee_debut": 1953, "annee_fin": 1955, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Supercinq', "variante": 'Coupé / Cabriolet', "portes": 2, "places": 4, "annee_debut": 1938, "annee_fin": 1952, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Supertraction', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1938, "annee_fin": 1939, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Rossion': [
        {"modele": 'Q1', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 2008, "annee_fin": 2012},
    ],
    'Rover': [
    ],
    'Ruf': [
    ],
    'Saab': [
    ],
    'SAIC': [
        {"modele": 'MG3', "portes": 5, "places": 5, "annee_debut": 2003},
        {"modele": 'MG4 EV', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'MG5 EV', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2020},
        {"modele": 'MG6', "portes": 4, "places": 5, "annee_debut": 2011},
        {"modele": 'MG7', "portes": 4, "places": 5, "annee_debut": 2007, "annee_fin": 2014},
        {"modele": 'MG HS', "portes": 5, "places": 5, "annee_debut": 2018},
        {"modele": 'MG Marvel R', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2020},
        {"modele": 'MG ZS', "portes": 5, "places": 5, "annee_debut": 2017},
        {"modele": 'MG ZS EV', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2019},
        {"modele": 'Roewe 350', "portes": 4, "places": 5, "annee_debut": 2009, "annee_fin": 2014},
        {"modele": 'Roewe 550', "portes": 4, "places": 5, "annee_debut": 2008, "annee_fin": 2014},
        {"modele": 'Roewe 750', "portes": 4, "places": 5, "annee_debut": 2006, "annee_fin": 2016},
        {"modele": 'Roewe i6', "portes": 4, "places": 5, "annee_debut": 2017},
        {"modele": 'Roewe RX5', "portes": 5, "places": 5, "annee_debut": 2016},
    ],
    'SAIPA': [
        {"modele": 'SAIPA 132', "portes": 4, "places": 5, "annee_debut": 2000, "annee_fin": 2010},
        {"modele": 'SAIPA 141', "portes": 4, "places": 5, "annee_debut": 1994, "annee_fin": 2010},
        {"modele": 'SAIPA 151', "portes": 2, "places": 3, "annee_debut": 2000},
        {"modele": 'SAIPA Aria', "portes": 4, "places": 5, "annee_debut": 2020},
        {"modele": 'SAIPA Pride', "portes": 4, "places": 5, "annee_debut": 1992},
        {"modele": 'SAIPA Quick', "portes": 5, "places": 5, "annee_debut": 2010},
        {"modele": 'SAIPA Saina', "portes": 4, "places": 5, "annee_debut": 2016},
    ],
    'Saleen': [
    ],
    'Salmson': [
        {"modele": '2300 S', "variante": 'Coupé', "portes": 2, "places": 4, "annee_debut": 1953, "annee_fin": 1957, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'AL', "variante": 'Cyclecar', "portes": 0, "places": 2, "annee_debut": 1921, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'G72', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1950, "annee_fin": 1952, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'GP', "variante": 'Course', "portes": 0, "places": 2, "annee_debut": 1925, "annee_fin": 1929, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'S4', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1929, "annee_fin": 1934, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'S4-61', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1938, "annee_fin": 1952, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Saroléa': [
        {"modele": '23 M', "variante": 'Moto', "portes": 0, "places": 2, "annee_debut": 1923, "annee_fin": 1930},
        {"modele": 'SP7', "variante": 'Moto électrique', "portes": 0, "places": 1, "reservoir": 0, "annee_debut": 2017},
        {"modele": 'Typhon', "variante": 'Moto', "portes": 0, "places": 2, "annee_debut": 1956, "annee_fin": 1960},
    ],
    'Saturn': [
        {"modele": 'Astra', "variante": 'Compacte', "portes": 5, "places": 5, "annee_debut": 2008, "annee_fin": 2009},
        {"modele": 'Aura', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 2007, "annee_fin": 2010},
        {"modele": 'Ion', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 2003, "annee_fin": 2007},
        {"modele": 'L-Series', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 2000, "annee_fin": 2005},
        {"modele": 'Outlook', "variante": 'SUV', "portes": 5, "places": 8, "annee_debut": 2007, "annee_fin": 2010},
        {"modele": 'Relay', "variante": 'Monospace', "portes": 5, "places": 7, "annee_debut": 2005, "annee_fin": 2007},
        {"modele": 'S-Series', "variante": 'Berline / Coupé', "portes": 4, "places": 5, "annee_debut": 1990, "annee_fin": 2002},
        {"modele": 'Sky', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 2007, "annee_fin": 2010},
        {"modele": 'Vue', "variante": 'SUV', "portes": 5, "places": 5, "annee_debut": 2002, "annee_fin": 2010},
    ],
    'Saviem': [
        {"modele": 'JM', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1964, "annee_fin": 1980},
        {"modele": 'SC10', "variante": 'Autobus', "portes": 2, "places": 100, "annee_debut": 1965, "annee_fin": 1989},
        {"modele": 'SG2', "variante": 'Utilitaire', "portes": 2, "places": 3, "annee_debut": 1965, "annee_fin": 1982},
        {"modele": 'SG4', "variante": 'Utilitaire', "portes": 2, "places": 3, "annee_debut": 1965, "annee_fin": 1982},
        {"modele": 'SM', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1965, "annee_fin": 1980},
    ],
    'Saxon': [
        {"modele": 'Model A', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1914, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Six', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Scout': [
        {"modele": '80', "variante": 'Tout-terrain', "portes": 2, "places": 4, "annee_debut": 1961, "annee_fin": 1965},
        {"modele": '800', "variante": 'Tout-terrain', "portes": 2, "places": 4, "annee_debut": 1965, "annee_fin": 1971},
        {"modele": 'II', "variante": 'Tout-terrain', "portes": 2, "places": 5, "annee_debut": 1971, "annee_fin": 1980},
        {"modele": 'Terra', "variante": 'Pick-up', "portes": 2, "places": 3, "annee_debut": 1976, "annee_fin": 1980},
        {"modele": 'Traveler', "variante": 'SUV', "portes": 2, "places": 5, "annee_debut": 1976, "annee_fin": 1980},
    ],
    'Scout Motors': [
        {"modele": 'Terra', "variante": 'Pick-up électrique (sortie annoncée 2027)', "portes": 4, "places": 5, "reservoir": 0},
        {"modele": 'Traveler', "variante": 'SUV électrique (sortie annoncée 2027)', "portes": 5, "places": 5, "reservoir": 0},
    ],
    'Scripps-Booth': [
        {"modele": 'Model C', "variante": 'Roadster', "portes": 2, "places": 3, "annee_debut": 1915, "annee_fin": 1917, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model G', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1917, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Rocket', "variante": 'Cyclecar', "portes": 0, "places": 2, "annee_debut": 1913, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'SEAT': [
    ],
    'Setra': [
        {"modele": 'S 6', "variante": 'Autocar', "portes": 2, "places": 30, "annee_debut": 1955, "annee_fin": 1966},
        {"modele": 'S 215 HD', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1976, "annee_fin": 1991},
        {"modele": 'S 315 HD', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1991, "annee_fin": 2003},
        {"modele": 'S 415 HD', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 2001, "annee_fin": 2013},
        {"modele": 'S 515 HD', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 2012},
    ],
    'Shelby': [
    ],
    'Simca': [
    ],
    'Simplex': [
        {"modele": '50 HP', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1907, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Crane-Simplex Model 5', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1915, "annee_fin": 1917, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Sizaire-Naudin': [
        {"modele": 'Type C', "variante": 'Torpedo', "portes": 2, "places": 2, "annee_debut": 1910, "annee_fin": 1913, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type F1', "variante": 'Voiturette', "portes": 0, "places": 2, "annee_debut": 1906, "annee_fin": 1910, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Skoda': [
    ],
    'Smart': [
    ],
    'Sono Motors': [
        {"modele": 'Sion', "variante": 'Citadine électrique solaire (prototype)', "portes": 5, "places": 5, "reservoir": 0, "annee_debut": 2019, "annee_fin": 2023},
    ],
    'Sovam': [
        {"modele": 'Sovam 850', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1965, "annee_fin": 1966},
        {"modele": 'Sovam 1100', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1966, "annee_fin": 1968},
        {"modele": 'Sovam 1300 GS', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1967, "annee_fin": 1969},
    ],
    'Springuel': [
        {"modele": 'Type 10/12 HP', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1907, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'SsangYong': [
    ],
    'SSC': [
        {"modele": 'Tuatara', "variante": 'Hypercar', "portes": 2, "places": 2, "annee_debut": 2020},
        {"modele": 'Ultimate Aero', "variante": 'Hypercar', "portes": 2, "places": 2, "annee_debut": 2006, "annee_fin": 2013},
    ],
    'SSC Tuatara': [
        {"modele": 'Tuatara Coupe', "portes": 2, "places": 2, "reservoir": 100},
        {"modele": 'Tuatara Roadster', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 100},
    ],
    'Stanley': [
        {"modele": 'Model 735', "variante": 'Vapeur', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1917},
        {"modele": 'Model 740', "variante": 'Vapeur', "portes": 4, "places": 5, "annee_debut": 1918, "annee_fin": 1924},
        {"modele": 'Model EX', "variante": 'Vapeur Runabout', "portes": 0, "places": 2, "annee_debut": 1906, "annee_fin": 1908},
        {"modele": 'Rocket', "variante": 'Record vapeur', "portes": 0, "places": 1, "annee_debut": 1906, "annee_fin": 1906},
    ],
    'Star': [
        {"modele": 'Model C', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1924, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model F', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1922, "annee_fin": 1924, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model M', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Sterling': [
        {"modele": 'A-Line', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 1998, "annee_fin": 2009},
        {"modele": 'Acterra', "variante": 'Camion', "portes": 2, "places": 3, "annee_debut": 1998, "annee_fin": 2009},
        {"modele": 'Bullet', "variante": 'Camion léger', "portes": 2, "places": 3, "annee_debut": 2008, "annee_fin": 2009},
        {"modele": 'L-Line', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1998, "annee_fin": 2009},
    ],
    'Stevens-Duryea': [
        {"modele": 'Big Six', "variante": 'Torpedo', "portes": 4, "places": 7, "annee_debut": 1907, "annee_fin": 1915, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model E', "variante": 'Berline', "portes": 4, "places": 7, "annee_debut": 1919, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model L', "variante": 'Runabout', "portes": 0, "places": 2, "annee_debut": 1902, "annee_fin": 1905, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Stoewer': [
        {"modele": 'Arkona', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1937, "annee_fin": 1939, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'D3', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1919, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Gigant', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1928, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Greif', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1936, "annee_fin": 1939, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Marschall', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1928, "annee_fin": 1934, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Typ P5', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1908, "annee_fin": 1910, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Stout Scarab': [
        {"modele": 'Scarab', "variante": 'Monospace (1 porte latérale)', "portes": 2, "places": 6, "annee_debut": 1935, "annee_fin": 1939},
    ],
    'StreetScooter': [
        {"modele": 'Work', "variante": 'Utilitaire électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2014, "annee_fin": 2022},
        {"modele": 'Work L', "variante": 'Utilitaire électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2016, "annee_fin": 2022},
        {"modele": 'Work XL', "variante": 'Utilitaire électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2018, "annee_fin": 2022},
    ],
    'Studebaker': [
    ],
    'Stutz': [
        {"modele": 'Bearcat', "variante": 'Roadster', "portes": 0, "places": 2, "annee_debut": 1912, "annee_fin": 1925},
        {"modele": 'Blackhawk', "variante": 'Coupé', "portes": 2, "places": 4, "annee_debut": 1971, "annee_fin": 1987},
        {"modele": 'DV-32', "variante": 'Berline / Roadster', "portes": 4, "places": 5, "annee_debut": 1931, "annee_fin": 1935},
        {"modele": 'Vertical Eight AA', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1927},
    ],
    'Subaru': [
    ],
    'Subaru STI': [
    ],
    'Suzuki': [
    ],
    'Talbot': [
    ],
    'Talbot-Lago': [
        {"modele": 'T23', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'T26 Grand Sport', "portes": 2, "places": 2, "reservoir": 90},
        {"modele": 'T26 Record', "portes": 4, "places": 4, "reservoir": 100},
        {"modele": 'T150 C-SS', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 90},
    ],
    'Tata': [
        {"modele": 'Tata Estate', "portes": 5, "places": 5, "annee_debut": 1992, "annee_fin": 2000},
        {"modele": 'Tata Harrier', "portes": 5, "places": 7, "annee_debut": 2018},
        {"modele": 'Tata Indica', "portes": 5, "places": 5, "annee_debut": 1998, "annee_fin": 2018},
        {"modele": 'Tata Indigo', "portes": 4, "places": 5, "annee_debut": 2002, "annee_fin": 2012},
        {"modele": 'Tata Nexon', "portes": 5, "places": 5, "annee_debut": 2017},
        {"modele": 'Tata Nexon EV', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2020},
        {"modele": 'Tata Safari', "portes": 5, "places": 7, "annee_debut": 1998},
        {"modele": 'Tata Sierra', "portes": 3, "places": 5, "annee_debut": 1991, "annee_fin": 2003},
        {"modele": 'Tata Telcoline', "portes": 2, "places": 5, "annee_debut": 1988, "annee_fin": 2006},
        {"modele": 'Tata Xenon', "portes": 2, "places": 5, "annee_debut": 2006, "annee_fin": 2015},
    ],
    'Tatra': [
        {"modele": 'Tatra 11', "portes": 2, "places": 2, "annee_debut": 1923, "annee_fin": 1927},
        {"modele": 'Tatra 12', "portes": 2, "places": 2, "annee_debut": 1926, "annee_fin": 1933},
        {"modele": 'Tatra 77', "portes": 4, "places": 4, "annee_debut": 1934, "annee_fin": 1938},
        {"modele": 'Tatra 87', "portes": 4, "places": 4, "annee_debut": 1936, "annee_fin": 1950},
        {"modele": 'Tatra 97', "portes": 2, "places": 4, "annee_debut": 1936, "annee_fin": 1939},
        {"modele": 'Tatra Phoenix', "portes": 2, "places": 3, "annee_debut": 2007},
        {"modele": 'Tatra T815', "portes": 2, "places": 3, "annee_debut": 1983},
    ],
    'Tempo': [
        {"modele": 'G1200', "variante": 'Tout-terrain', "portes": 0, "places": 4, "annee_debut": 1936, "annee_fin": 1944},
        {"modele": 'Hanseat', "variante": 'Triporteur', "portes": 2, "places": 2, "annee_debut": 1949, "annee_fin": 1956},
        {"modele": 'Matador', "variante": 'Utilitaire', "portes": 3, "places": 3, "annee_debut": 1949, "annee_fin": 1967},
        {"modele": 'Wiking', "variante": 'Utilitaire', "portes": 2, "places": 3, "annee_debut": 1955, "annee_fin": 1963},
    ],
    'Terraplane': [
        {"modele": 'Deluxe Six', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1934, "annee_fin": 1937},
        {"modele": 'K', "variante": 'Berline / Coupé', "portes": 2, "places": 5, "annee_debut": 1932, "annee_fin": 1933},
        {"modele": 'Super', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1936, "annee_fin": 1938},
    ],
    'Tesla': [
    ],
    'Thomas': [
        {"modele": 'Flyer', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1903, "annee_fin": 1919, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 35', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1907, "annee_fin": 1909, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Toyota': [
    ],
    'Toyota GR': [
    ],
    'Trabant': [
    ],
    'Tracta': [
        {"modele": 'Type A', "variante": 'Sport', "portes": 2, "places": 2, "annee_debut": 1927, "annee_fin": 1930, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type E', "variante": 'Coupé', "portes": 2, "places": 2, "annee_debut": 1930, "annee_fin": 1932, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Triumph': [
    ],
    'Tucker': [
        {"modele": '48 Torpedo', "variante": 'Berline', "portes": 4, "places": 6, "reservoir": 76, "annee_debut": 1947, "annee_fin": 1948},
    ],
    'Turcat-Méry': [
        {"modele": 'Type MJ', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1910, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'UG', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1924, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'TVR': [
    ],
    'UAZ': [
        {"modele": 'UAZ 450', "portes": 2, "places": 4, "annee_debut": 1958, "annee_fin": 1965},
        {"modele": 'UAZ 469', "portes": 4, "places": 5, "annee_debut": 1971, "annee_fin": 2003},
        {"modele": 'UAZ Hunter', "portes": 3, "places": 5, "annee_debut": 2003},
        {"modele": 'UAZ Patriot', "portes": 5, "places": 7, "annee_debut": 2005},
        {"modele": 'UAZ Pickup', "portes": 2, "places": 3, "annee_debut": 2008},
        {"modele": 'UAZ Profi', "portes": 2, "places": 3, "annee_debut": 2015},
    ],
    'Unic': [
        {"modele": 'L9', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1922, "annee_fin": 1927, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Taxi Type A', "variante": 'Taxi', "portes": 4, "places": 4, "annee_debut": 1908, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'U4', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1931, "annee_fin": 1936, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'ZU', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1950, "annee_fin": 1966, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Unimog': [
        {"modele": '70200', "variante": 'Tout-terrain', "portes": 2, "places": 2, "annee_debut": 1948, "annee_fin": 1951},
        {"modele": 'U 401', "variante": 'Tout-terrain', "portes": 2, "places": 2, "annee_debut": 1953, "annee_fin": 1956},
        {"modele": 'U 406', "variante": 'Tout-terrain', "portes": 2, "places": 2, "annee_debut": 1963, "annee_fin": 1989},
        {"modele": 'U 423', "variante": 'Porte-outils', "portes": 2, "places": 3, "annee_debut": 2013},
        {"modele": 'U 1300 L', "variante": 'Tout-terrain militaire', "portes": 2, "places": 2, "annee_debut": 1975, "annee_fin": 1993},
        {"modele": 'U 5023', "variante": 'Tout-terrain', "portes": 2, "places": 3, "annee_debut": 2013},
    ],
    'Van Hool': [
        {"modele": 'A330', "variante": 'Autobus', "portes": 2, "places": 100, "annee_debut": 1987},
        {"modele": 'Alizée', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 1981},
        {"modele": 'Astron', "variante": 'Autocar à impériale', "portes": 2, "places": 80, "annee_debut": 1986},
        {"modele": 'CX', "variante": 'Autocar', "portes": 2, "places": 55, "annee_debut": 2014},
        {"modele": 'Exqui.City', "variante": 'Tram-bus', "portes": 2, "places": 150, "annee_debut": 2011},
        {"modele": 'TX', "variante": 'Autocar', "portes": 2, "places": 50, "annee_debut": 2008},
    ],
    'Vanden Plas': [
        {"modele": '1500', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1974, "annee_fin": 1980},
        {"modele": 'Princess 4 Litre', "variante": 'Limousine', "portes": 4, "places": 7, "annee_debut": 1957, "annee_fin": 1968},
        {"modele": 'Princess 4 Litre R', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1964, "annee_fin": 1968},
        {"modele": 'Princess 1100', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1963, "annee_fin": 1974},
        {"modele": 'Torpedo', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1910, "annee_fin": 1923},
    ],
    'Vauxhall': [
    ],
    'Vector': [
        {"modele": 'M12', "variante": 'Supercar', "portes": 2, "places": 2, "annee_debut": 1996, "annee_fin": 1999},
        {"modele": 'W8', "variante": 'Supercar', "portes": 2, "places": 2, "annee_debut": 1989, "annee_fin": 1993},
    ],
    'Velie': [
        {"modele": 'Model 38', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1915, "annee_fin": 1918, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 50', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 58', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1922, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Venturi': [
        {"modele": 'Venturi 260', "portes": 2, "places": 2, "reservoir": 70, "annee_debut": 1984, "annee_fin": 1994},
        {"modele": 'Venturi 400 GT', "portes": 2, "places": 2, "reservoir": 80, "annee_debut": 1992, "annee_fin": 1995},
        {"modele": 'Venturi Atlantique', "portes": 2, "places": 2, "annee_debut": 1991, "annee_fin": 2000},
        {"modele": 'Venturi Atlantique 300', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Venturi Atlantique 300 Biturbo', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Venturi Buckeye Bullet', "portes": 2, "places": 2, "annee_debut": 2010},
        {"modele": 'Venturi Fétish', "variante": 'Électrique', "portes": 2, "places": 2, "reservoir": 0},
        {"modele": 'Venturi VBB-3', "portes": 2, "places": 1, "annee_debut": 2016},
        {"modele": 'Venturi Volage', "variante": 'Électrique', "portes": 2, "places": 2, "reservoir": 0},
    ],
    'Veritas': [
        {"modele": 'Dyna', "variante": 'Coupé / Cabriolet', "portes": 2, "places": 2, "annee_debut": 1950, "annee_fin": 1952},
        {"modele": 'RS', "variante": 'Course', "portes": 0, "places": 2, "annee_debut": 1947, "annee_fin": 1949},
        {"modele": 'RS III', "variante": 'Roadster', "portes": 0, "places": 2, "annee_debut": 2001, "annee_fin": 2003},
        {"modele": 'RS III V10', "variante": 'Roadster', "portes": 0, "places": 2, "annee_debut": 2009, "annee_fin": 2012},
    ],
    'Vespa': [
        {"modele": '400', "variante": 'Microcar', "portes": 2, "places": 2, "annee_debut": 1957, "annee_fin": 1961},
    ],
    'Vidal & Sohn': [
        {"modele": 'Tempo Hanseat', "variante": 'Triporteur', "portes": 2, "places": 2, "annee_debut": 1949, "annee_fin": 1956},
        {"modele": 'Tempo Matador', "variante": 'Utilitaire', "portes": 3, "places": 3, "annee_debut": 1949, "annee_fin": 1967},
    ],
    'Viking': [
        {"modele": 'Model 8', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1929, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'VinFast': [
        {"modele": 'VinFast Fadil', "portes": 5, "places": 5, "annee_debut": 2019, "annee_fin": 2022},
        {"modele": 'VinFast Lux A2.0', "portes": 4, "places": 5, "annee_debut": 2018, "annee_fin": 2022},
        {"modele": 'VinFast Lux SA2.0', "portes": 5, "places": 7, "annee_debut": 2018, "annee_fin": 2022},
        {"modele": 'VinFast VF 5', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'VinFast VF 6', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'VinFast VF 8', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2022},
        {"modele": 'VinFast VF 9', "variante": 'Électrique', "portes": 5, "places": 7, "annee_debut": 2022},
        {"modele": 'VinFast VF e34', "variante": 'Électrique', "portes": 5, "places": 5, "annee_debut": 2021},
    ],
    'Vinot-Deguingand': [
        {"modele": 'Type BL', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1912, "annee_fin": 1916, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Type L', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1920, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Vivinus': [
        {"modele": 'Type 18/22 HP', "variante": 'Tonneau', "portes": 0, "places": 4, "annee_debut": 1905, "annee_fin": 1912, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Voiturette', "variante": 'Voiturette', "portes": 0, "places": 2, "annee_debut": 1899, "annee_fin": 1904, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Voisin': [
        {"modele": 'Biscooter', "variante": 'Microcar', "portes": 0, "places": 2, "annee_debut": 1950, "annee_fin": 1958, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C1', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1919, "annee_fin": 1922, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C5', "variante": 'Torpedo', "portes": 4, "places": 4, "annee_debut": 1923, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C11', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1928, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C14', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1927, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C25 Aérodyne', "variante": 'Coupé', "portes": 2, "places": 4, "annee_debut": 1934, "annee_fin": 1935, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'C28', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1935, "annee_fin": 1937, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Volkswagen': [
    ],
    'Volvo': [
    ],
    'Wanderer': [
        {"modele": 'W1 Puppchen', "variante": 'Voiturette', "portes": 2, "places": 2, "annee_debut": 1913, "annee_fin": 1914, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W10', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1926, "annee_fin": 1932, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W11', "variante": 'Berline', "portes": 4, "places": 6, "annee_debut": 1928, "annee_fin": 1932, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W21', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1933, "annee_fin": 1935, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W22', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1933, "annee_fin": 1935, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W23', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1937, "annee_fin": 1940, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W24', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1937, "annee_fin": 1940, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W25K', "variante": 'Roadster', "portes": 2, "places": 2, "annee_debut": 1936, "annee_fin": 1938, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Wartburg': [
        {"modele": 'Wartburg 1.3', "portes": 4, "places": 5, "annee_debut": 1988, "annee_fin": 1991},
        {"modele": 'Wartburg 311', "portes": 4, "places": 5, "annee_debut": 1956, "annee_fin": 1965},
        {"modele": 'Wartburg 312', "portes": 4, "places": 5, "annee_debut": 1965, "annee_fin": 1967},
        {"modele": 'Wartburg 353', "portes": 4, "places": 5, "annee_debut": 1966, "annee_fin": 1988},
        {"modele": 'Wartburg Kombi', "portes": 4, "places": 5, "annee_debut": 1966, "annee_fin": 1988},
        {"modele": 'Wartburg Tourist', "portes": 2, "places": 2, "annee_debut": 1961, "annee_fin": 1988},
    ],
    'Western Star': [
        {"modele": '49X', "variante": 'Chantier', "portes": 2, "places": 2, "annee_debut": 2020},
        {"modele": '57X', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2022},
        {"modele": '4900', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 1991, "annee_fin": 2020},
        {"modele": '5700XE', "variante": 'Tracteur routier', "portes": 2, "places": 2, "annee_debut": 2014, "annee_fin": 2022},
    ],
    'Whippet': [
        {"modele": 'Model 96', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model 98', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1928, "annee_fin": 1931, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'White': [
        {"modele": 'M3 Scout Car', "variante": 'Blindé', "portes": 0, "places": 8, "annee_debut": 1938, "annee_fin": 1944},
        {"modele": 'Model 40', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1911, "annee_fin": 1918},
        {"modele": 'Steam Car', "variante": 'Vapeur', "portes": 0, "places": 4, "annee_debut": 1900, "annee_fin": 1910},
        {"modele": 'WC', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1949, "annee_fin": 1960},
    ],
    'Wiesmann': [
        {"modele": 'GT MF4', "variante": 'Coupé', "portes": 2, "places": 2, "reservoir": 70, "annee_debut": 2003, "annee_fin": 2013},
        {"modele": 'GT MF4-CS', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'GT MF4-R', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'GT MF5', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'GT MF5', "variante": 'Coupé', "portes": 2, "places": 2, "reservoir": 70, "annee_debut": 2009, "annee_fin": 2013},
        {"modele": 'MF3', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 70, "annee_debut": 1993, "annee_fin": 2011},
        {"modele": 'MF4', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'MF4', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 70},
        {"modele": 'MF5', "variante": 'Coupe', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'MF5', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'MF6', "variante": 'Roadster', "portes": 2, "places": 2, "reservoir": 80},
        {"modele": 'Project Thunderball', "variante": 'Roadster électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2022},
    ],
    'Willème': [
        {"modele": 'LD 610', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1950, "annee_fin": 1960, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'TG 300', "variante": 'Tracteur lourd', "portes": 2, "places": 2, "annee_debut": 1958, "annee_fin": 1970, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'W8', "variante": 'Camion', "portes": 2, "places": 2, "annee_debut": 1965, "annee_fin": 1970, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Wills Sainte Claire': [
        {"modele": 'A-68', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1921, "annee_fin": 1923, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'B-68', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1924, "annee_fin": 1925, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'T-6', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1926, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Willys': [
        {"modele": 'Aero', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1952, "annee_fin": 1955},
        {"modele": 'Americar', "variante": 'Berline / Coupé', "portes": 4, "places": 5, "annee_debut": 1937, "annee_fin": 1942},
        {"modele": 'CJ-2A', "variante": 'Jeep', "portes": 0, "places": 4, "annee_debut": 1945, "annee_fin": 1949},
        {"modele": 'Jeep Station Wagon', "variante": 'Break', "portes": 3, "places": 6, "annee_debut": 1946, "annee_fin": 1965},
        {"modele": 'Jeepster', "variante": 'Phaeton', "portes": 2, "places": 5, "annee_debut": 1948, "annee_fin": 1950},
        {"modele": 'M38', "variante": 'Jeep militaire', "portes": 0, "places": 4, "annee_debut": 1950, "annee_fin": 1952},
        {"modele": 'MB', "variante": 'Jeep militaire', "portes": 0, "places": 4, "annee_debut": 1941, "annee_fin": 1945},
        {"modele": 'Model 77', "variante": 'Berline', "portes": 4, "places": 4, "annee_debut": 1933, "annee_fin": 1936},
        {"modele": 'Whippet', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1926, "annee_fin": 1931},
        {"modele": 'Willys-Knight Model 70', "variante": 'Berline', "portes": 4, "places": 5, "annee_debut": 1925, "annee_fin": 1928},
    ],
    'Winton': [
        {"modele": 'Bullet', "variante": 'Course', "portes": 0, "places": 1, "annee_debut": 1902, "annee_fin": 1904, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Model K', "variante": 'Tonneau', "portes": 0, "places": 5, "annee_debut": 1904, "annee_fin": 1905, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Motor Carriage', "variante": 'Buggy', "portes": 0, "places": 2, "annee_debut": 1897, "annee_fin": 1899, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
        {"modele": 'Six', "variante": 'Torpedo', "portes": 4, "places": 5, "annee_debut": 1908, "annee_fin": 1924, "remarques": 'Désignations et dates indicatives (marque ancienne), à vérifier.'},
    ],
    'Workhorse': [
        {"modele": 'C1000', "variante": 'Utilitaire électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2016, "annee_fin": 2021},
        {"modele": 'W4 CC', "variante": 'Camion électrique', "portes": 2, "places": 3, "reservoir": 0, "annee_debut": 2023},
        {"modele": 'W56', "variante": 'Utilitaire électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2024},
    ],
    'Wuling': [
        {"modele": 'Wuling Baojun 510', "portes": 5, "places": 5, "annee_debut": 2016},
        {"modele": 'Wuling Hongguang', "portes": 5, "places": 7, "annee_debut": 2010},
        {"modele": 'Wuling Hongguang Mini EV', "variante": 'Électrique', "portes": 3, "places": 4, "annee_debut": 2020},
        {"modele": 'Wuling Hongguang S', "portes": 5, "places": 7, "annee_debut": 2013},
        {"modele": 'Wuling Rongguang', "portes": 2, "places": 5, "annee_debut": 2008},
        {"modele": 'Wuling Victory', "portes": 5, "places": 7, "annee_debut": 2020},
    ],
    'XPeng': [
        {"modele": 'XPeng G3', "portes": 5, "places": 5, "annee_debut": 2018, "annee_fin": 2023},
        {"modele": 'XPeng G6', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'XPeng G9', "portes": 5, "places": 5, "annee_debut": 2023},
        {"modele": 'XPeng P5', "portes": 4, "places": 5, "annee_debut": 2021},
        {"modele": 'XPeng P7', "portes": 4, "places": 5, "annee_debut": 2020},
    ],
    'Zap': [
        {"modele": 'Alias', "variante": 'Tricycle électrique', "portes": 2, "places": 2, "reservoir": 0, "annee_debut": 2010, "annee_fin": 2012},
        {"modele": 'Xebra', "variante": 'Tricycle électrique', "portes": 4, "places": 4, "reservoir": 0, "annee_debut": 2006, "annee_fin": 2009},
    ],
    'ZIL': [
        {"modele": 'ZIL-111', "portes": 4, "places": 6, "annee_debut": 1958, "annee_fin": 1967},
        {"modele": 'ZIL-114', "portes": 4, "places": 6, "annee_debut": 1967, "annee_fin": 1978},
        {"modele": 'ZIL-115', "portes": 4, "places": 6, "annee_debut": 1978, "annee_fin": 1989},
        {"modele": 'ZIL-130', "portes": 2, "places": 3, "annee_debut": 1962, "annee_fin": 1994},
        {"modele": 'ZIL-131', "portes": 2, "places": 3, "annee_debut": 1966, "annee_fin": 1990},
        {"modele": 'ZIL-133', "portes": 2, "places": 3, "annee_debut": 1975, "annee_fin": 1991},
        {"modele": 'ZIL-4104', "portes": 4, "places": 6, "annee_debut": 1985, "annee_fin": 1994},
    ],
    'Zimmer': [
        {"modele": 'Golden Spirit', "variante": 'Coupé', "portes": 2, "places": 5, "annee_debut": 1980, "annee_fin": 1988},
        {"modele": 'Quicksilver', "variante": 'Coupé', "portes": 2, "places": 4, "annee_debut": 1984, "annee_fin": 1988},
    ],
    'Zündapp': [
        {"modele": 'Janus', "variante": 'Microcar', "portes": 2, "places": 4, "annee_debut": 1957, "annee_fin": 1958},
    ],
}

# Détail génération › phase › variantes, un fichier par marque (data/detail/)
from voiture.voiture_modele.data.detail import detail as _detail  # noqa: E402

for _marque, _lignes in _detail().items():
    MODELES.setdefault(_marque, []).extend(_lignes)
