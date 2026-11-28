"""LaSalle (General Motors / Cadillac, 1927-1940) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Series 303 (première voiture dessinée par Harley Earl), 340, Series 50 (huit cylindres Oldsmobile 1934-1936, puis V8 Cadillac) et
Series 52 (1938-1940). Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LASALLE-V8-5.0": f("ATM", "ESS", 5.0, "NC", 8, 3000, 1400, "SAE30", 7.0, 3000, a="V"),
    "LASALLE-V8-5.6": f("ATM", "ESS", 5.6, "NC", 8, 3000, 1400, "SAE30", 7.0, 3000, a="V"),
    "OLDS-L8-4.0": f("ATM", "ESS", 4.0, "NC", 8, 3700, 1600, "SAE30", 5.5, 3000),
    "LASALLE-V8-5.3": f("ATM", "ESS", 5.3, "NC", 8, 3400, 1600, "SAE30", 6.5, 3000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Cadillac", lambda fam: "Oldsmobile" if fam.startswith("OLDS") else "Cadillac")
L = []
IND = "marché nord-américain ; données indicatives"
mg(L, "Series 303", "303", "1", "1927-03", "1928-12", [("5.0 V8 76", "LASALLE-V8-5.0", 230)], portes=4, places=5, reservoir=75, remarques="Marque compagne de Cadillac ; " + IND)
mg(L, "Series 340", "340", "1", "1929-01", "1930-12", [("5.6 V8 91", "LASALLE-V8-5.6", 260)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "Series 50", "50", "1", "1934-01", "1937-12", [("4.0 L8 96", "OLDS-L8-4.0", 260, {"fin": "1936-12"}), ("5.3 V8 127", "LASALLE-V8-5.3", 339, {"debut": "1937-01"})],
   portes=4, places=5, reservoir=75, remarques="Huit cylindres Oldsmobile, puis V8 Cadillac en 1937 ; " + IND)
mg(L, "Series 52", "52", "1", "1938-01", "1940-12", [("5.3 V8 127", "LASALLE-V8-5.3", 339, {"fin": "1939-12"}), ("5.3 V8 132", "LASALLE-V8-5.3", 339, {"debut": "1940-01"})],
   portes=4, places=5, reservoir=75, remarques="Berline, coupé et cabriolet ; dernière LaSalle en 1940 ; " + IND)

MOT = Motorisations("Cadillac", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"LaSalle": L}
MOTEURS = MOT.moteurs()
