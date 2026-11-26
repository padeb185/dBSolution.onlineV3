"""Amilcar : générations, phases, motorisations (marché européen) et moteurs liés.
CC, CGS, CGSS, C6, M, Pégase et Compound (1921-1939). Quatre et six cylindres Amilcar ajoutés.
Puissances en ch, désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "AMILCAR-0.9": f("ATM", E_, 0.9, "NC", 4, 3000, 2000, "SAE30", 2.5, 3000),
    "AMILCAR-1.1": f("ATM", E_, 1.1, "NC", 4, 3600, 2400, "SAE30", 3.0, 3000),
    "AMILCAR-1.1-L6C": f("TURBO", E_, 1.1, "NC", 6, 6000, 4500, "SAE30", 4.0, 2000),
    "AMILCAR-1.2": f("ATM", E_, 1.2, "NC", 4, 3600, 2200, "SAE30", 3.0, 3000),
    "AMILCAR-2.0": f("ATM", E_, 2.0, "NC", 4, 4000, 2500, "SAE30", 4.5, 3000),
    "AMILCAR-2.5": f("ATM", E_, 2.5, "NC", 4, 4000, 2500, "SAE30", 4.5, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Amilcar", lambda fam: "Amilcar")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "CC", "CC", "1", "1921-01", "1922-12", [("0.9 18", "AMILCAR-0.9", 45)], portes=0, places=2, reservoir=25, remarques="Cyclecar ; " + IND)
mg(L, "CGS", "CGS", "1", "1924-01", "1927-12", [("1.1 30", "AMILCAR-1.1", 65)], portes=0, places=2, reservoir=35, remarques="Grand Sport, roadster ; " + IND)
mg(L, "CGSS", "CGSS", "1", "1926-01", "1929-12", [("1.1 35", "AMILCAR-1.1", 68)], portes=0, places=2, reservoir=35, remarques="Grand Sport surbaissée ; " + IND)
mg(L, "C6", "C6", "1", "1926-01", "1929-12", [("1.1 L6 compresseur 83", "AMILCAR-1.1-L6C", 110)], portes=0, places=2, reservoir=45,
   remarques="Six cylindres double arbre à compresseur, voiture de course ; " + IND)
mg(L, "M", "M", "1", "1928-01", "1935-12", [("1.2 28", "AMILCAR-1.2", 66)], portes=4, places=4, reservoir=40, remarques="Berlines M, M2, M3 et M4 ; " + IND)
mg(L, "Pégase", "Pégase", "1", "1934-01", "1937-12", [("2.0 55", "AMILCAR-2.0", 120), ("2.5 70", "AMILCAR-2.5", 150, {"debut": "1935-01"})],
   portes=2, places=4, reservoir=55, remarques="Coupé et cabriolet ; " + IND)
mg(L, "Compound", "Compound", "1", "1938-01", "1939-12", [("1.2 34", "AMILCAR-1.2", 70)], portes=4, places=4, reservoir=40,
   remarques="Traction avant, châssis en alliage léger (période Hotchkiss) ; " + IND)

MOT = Motorisations("Amilcar", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Amilcar": L}
MOTEURS = MOT.moteurs()
