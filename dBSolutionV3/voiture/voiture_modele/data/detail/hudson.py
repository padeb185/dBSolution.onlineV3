"""Hudson (Detroit, 1909-1957) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 20, Super Six, Greater Eight, Commodore, Hornet (dont la Hornet « Step-down » des victoires NASCAR et la Hornet sur base Nash),
Wasp, Jet et Italia (Carrozzeria Touring). Fusion avec Nash dans AMC (1954) ; marque arrêtée en 1957. Essex et Terraplane à part.
V8 Packard (1955-1956) et AMC (1957) ajoutés. Puissances brutes (SAE gross) converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "HUDSON-L4-3.3": f("ATM", E_, 3.3, "NC", 4, 1800, 1000, "SAE30", 4.0, 2000),
    "HUDSON-L6-4.7": f("ATM", E_, 4.7, "NC", 6, 2400, 1200, "SAE30", 5.0, 3000),
    "HUDSON-L8-3.5": f("ATM", E_, 3.5, "NC", 8, 3600, 1600, "SAE30", 5.0, 3000),
    "HUDSON-L8-4.2": f("ATM", E_, 4.2, "NC", 8, 4200, 1800, "SAE30", 5.5, 3000),
    "HUDSON-L6-3.3": f("ATM", E_, 3.3, "NC", 6, 4000, 1600, "SAE30", 4.7, 3000),
    "HUDSON-L6-3.5": f("ATM", E_, 3.5, "NC", 6, 4000, 1600, "SAE30", 4.7, 3000),
    "HUDSON-L6-3.8": f("ATM", E_, 3.8, "NC", 6, 4000, 1600, "SAE30", 4.7, 3000),
    "HUDSON-L6-4.3": f("ATM", E_, 4.3, "NC", 6, 4000, 1600, "SAE30", 4.7, 3000),
    "HUDSON-L6-5.0": f("ATM", E_, 5.0, "NC", 6, 3800, 1800, "SAE30", 5.2, 3000),
    "PACKARD-V8-5.2": f("ATM", E_, 5.2, "CHAINE", 8, 4200, 2400, "10W30", 5.7, 5000, a="V"),
    "AMC-V8-5.4": f("ATM", E_, 5.4, "CHAINE", 8, 4700, 2600, "10W30", 4.7, 5000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Hudson", lambda fam: "Packard" if fam.startswith("PACKARD") else ("AMC" if fam.startswith("AMC") else "Hudson"))
L = []
IND = "marché nord-américain ; données indicatives"

mg(L, "Model 20", "Model 20", "1", "1909-07", "1910-12", [("3.3 20", "HUDSON-L4-3.3", 100)], portes=2, places=2, reservoir=45, remarques="Première Hudson, roadster ; " + IND)
mg(L, "Super Six", "Super Six", "1", "1916-01", "1926-12", [("4.7 L6 77", "HUDSON-L6-4.7", 240)], portes=4, places=5, reservoir=60,
   remarques="Six cylindres à vilebrequin équilibré, records d'endurance ; " + IND)
mg(L, "Greater Eight", "Greater Eight", "1", "1930-01", "1932-12", [("3.5 L8 81", "HUDSON-L8-3.5", 210), ("4.2 L8 102", "HUDSON-L8-4.2", 250, {"debut": "1932-01"})],
   portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Commodore", "Commodore", "1", "1941-01", "1947-12", [("3.5 L6 103", "HUDSON-L6-3.5", 230), ("4.2 L8 130", "HUDSON-L8-4.2", 271)], portes=4, places=6, reservoir=60,
   remarques="Production interrompue de 1942 à 1945 ; " + IND)
mg(L, "Commodore", "Step-down", "1", "1948-01", "1952-12", [("4.3 L6 123", "HUDSON-L6-4.3", 271), ("4.2 L8 130", "HUDSON-L8-4.2", 271)], portes=4, places=6, reservoir=75,
   remarques="Carrosserie « Step-down » à plancher surbaissé ; " + IND)
mg(L, "Hornet", "Step-down", "1", "1951-01", "1954-12",
   [("5.0 L6 147", "HUDSON-L6-5.0", 348), ("Twin H-Power 5.0 L6 162", "HUDSON-L6-5.0", 348, {"debut": "1952-01"}), ("Twin H-Power 5.0 L6 172", "HUDSON-L6-5.0", 353, {"debut": "1954-01"})],
   portes=4, places=6, reservoir=75, remarques="« Fabulous Hudson Hornet », victoires NASCAR 1951-1954 ; " + IND)
mg(L, "Hornet", "Nash", "1", "1955-01", "1957-12",
   [("5.0 L6 162", "HUDSON-L6-5.0", 348, {"fin": "1956-12"}), ("5.2 V8 211", "PACKARD-V8-5.2", 407, {"fin": "1956-12"}), ("5.4 V8 259", "AMC-V8-5.4", 468, {"debut": "1957-01"})],
   portes=4, places=6, reservoir=76, remarques="Base Nash (AMC) à Kenosha ; V8 Packard puis AMC ; " + IND)
mg(L, "Wasp", "Wasp", "1", "1952-01", "1956-12", [("3.8 L6 129", "HUDSON-L6-3.8", 271), ("Twin H-Power 3.8 L6 142", "HUDSON-L6-3.8", 278, {"debut": "1954-01"})],
   portes=4, places=6, reservoir=75, remarques="Base Nash à partir de 1955 ; " + IND)
mg(L, "Jet", "Jet", "1", "1953-01", "1954-12", [("3.3 L6 105", "HUDSON-L6-3.3", 225), ("Super Jet Twin H 3.3 L6 116", "HUDSON-L6-3.3", 237)], portes=4, places=5, reservoir=60,
   remarques="Compacte, échec commercial ; " + IND)
mg(L, "Italia", "Italia", "1", "1954-01", "1955-12", [("3.3 L6 116", "HUDSON-L6-3.3", 237)], portes=2, places=4, reservoir=60,
   remarques="Coupé carrossé par Touring (Milan) sur base Jet, 26 exemplaires ; " + IND)

MOT = Motorisations("Hudson", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hudson": L}
MOTEURS = MOT.moteurs()
