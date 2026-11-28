"""Hupmobile (Detroit, 1909-1940) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Model 20, Model R, Century Eight, Aerodynamic (six et huit cylindres) et Skylark (carrosserie de la Cord 810). Puissances brutes
converties en ch (× 1,014). Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "HUP-L4-2.8": f("ATM", E_, 2.8, "NC", 4, 1800, 1000, "SAE30", 3.5, 2000),
    "HUP-L4-3.1": f("ATM", E_, 3.1, "NC", 4, 2400, 1200, "SAE30", 4.0, 2000),
    "HUP-L8-4.4": f("ATM", E_, 4.4, "NC", 8, 3200, 1600, "SAE30", 6.0, 3000),
    "HUP-L6-4.0": f("ATM", E_, 4.0, "NC", 6, 3600, 1600, "SAE30", 5.0, 3000),
    "HUP-L8-5.0": f("ATM", E_, 5.0, "NC", 8, 3400, 1600, "SAE30", 6.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Hupmobile")
L = []
IND = "désignations et données indicatives (marque ancienne), à vérifier"

mg(L, "Model 20", "Model 20", "1", "1909-01", "1913-12", [("2.8 20", "HUP-L4-2.8", 90)], portes=2, places=2, reservoir=40, remarques="Runabout, premier succès de la marque ; " + IND)
mg(L, "Model R", "Model R", "1", "1918-01", "1925-12", [("3.1 35", "HUP-L4-3.1", 150)], portes=4, places=5, reservoir=50, remarques=IND)
mg(L, "Century Eight", "Century", "1", "1928-01", "1931-12", [("4.4 L8 101", "HUP-L8-4.4", 290)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Aerodynamic", "Aerodynamic", "1", "1934-01", "1936-12", [("4.0 L6 91", "HUP-L6-4.0", 250), ("5.0 L8 122", "HUP-L8-5.0", 330)], portes=4, places=5, reservoir=70,
   remarques="Style aérodynamique (Raymond Loewy) ; " + IND)
mg(L, "Skylark", "Skylark", "1", "1939-05", "1941-07", [("4.0 L6 102", "HUP-L6-4.0", 270)], portes=4, places=5, reservoir=70,
   remarques="Carrosserie issue des outillages de la Cord 810, environ 300 exemplaires ; " + IND)

MOT = Motorisations("Hupmobile", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Hupmobile": L}
MOTEURS = MOT.moteurs()
