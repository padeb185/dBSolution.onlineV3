"""Dixi : générations, phases, motorisations (marché européen) et moteurs liés.
Fahrzeugfabrik Eisenach : S6 (1910-1914), G1 (1920-1925) et 3/15 PS DA-1 (Austin Seven sous licence, 1927-1929),
reprise par BMW en 1928 (BMW 3/15). Puissances en ch DIN. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "DIXI-1.6": f("ATM", E_, 1.6, "NC", 4, 2000, 1200, "SAE30", 3.5, 2000),
    "DIXI-1.6B": f("ATM", E_, 1.6, "NC", 4, 2400, 1400, "SAE30", 3.5, 3000),
    "DIXI-0.75": f("ATM", E_, 0.75, "NC", 4, 3000, 2000, "SAE30", 2.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Dixi", lambda fam: "Dixi")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "S6", "S6", "1", "1910-01", "1914-12", [("1.6 16", "DIXI-1.6", 70)], portes=4, places=4, reservoir=40, remarques="Torpédo ; " + IND)
mg(L, "G1", "G1", "1", "1920-01", "1925-12", [("1.6 20", "DIXI-1.6B", 75)], portes=4, places=4, reservoir=40, remarques="Torpédo ; " + IND)
mg(L, "3/15 PS DA-1", "DA-1", "1", "1927-12", "1929-12", [("0.75 15", "DIXI-0.75", 35)], portes=2, places=4, reservoir=25,
   remarques="Austin Seven sous licence, poursuivie comme BMW 3/15 DA-1 ; " + IND)

MOT = Motorisations("Dixi", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Dixi": L}
MOTEURS = MOT.moteurs()
