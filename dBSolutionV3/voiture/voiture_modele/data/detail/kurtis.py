"""Kurtis (Kurtis-Kraft, Los Angeles) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Sport Car (1949-1950, base de la Muntz Jet) et 500S (1953-1955, roadster dérivé des monoplaces d'Indianapolis). Moteurs au choix du client
(Ford, Cadillac, Chrysler) : une motorisation représentative. Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "FORD-FLATHEAD-3.9": f("ATM", "ESS", 3.9, "NC", 8, 3600, 2000, "SAE30", 4.7, 3000, a="V"),
    "CADILLAC-V8-5.4": f("ATM", "ESS", 5.4, "CHAINE", 8, 4150, 2700, "10W30", 4.7, 5000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Ford", lambda fam: "Cadillac" if fam.startswith("CADILLAC") else "Ford")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Sport Car", "Sport Car", "1", "1949-01", "1950-12", [("3.9 V8 101", "FORD-FLATHEAD-3.9", 244)], portes=2, places=2, reservoir=75, remarques="Roadster en polyester, 36 exemplaires ; " + IND)
mg(L, "500S", "500S", "1", "1953-01", "1955-12", [("5.4 V8 213", "CADILLAC-V8-5.4", 446)], portes=0, places=2, reservoir=75, remarques="Roadster de course-client, environ 30 exemplaires ; " + IND)

MOT = Motorisations("Ford", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Kurtis": L}
MOTEURS = MOT.moteurs()
