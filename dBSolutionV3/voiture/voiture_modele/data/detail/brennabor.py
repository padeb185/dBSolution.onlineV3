"""Brennabor : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur de Brandebourg-sur-la-Havel : Typ P (8/24 PS), Typ R (6/25 PS), Juwel (6 et 8 cylindres) et Ideal.
Puissances en ch DIN. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

E_ = "ESS"
FAMILLES = {
    "BRENNABOR-2.1": f("ATM", E_, 2.1, "NC", 4, 2400, 1400, "SAE30", 4.0, 3000),
    "BRENNABOR-1.6": f("ATM", E_, 1.6, "NC", 4, 2800, 1600, "SAE30", 3.5, 3000),
    "BRENNABOR-L6-3.1": f("ATM", E_, 3.1, "NC", 6, 3000, 1600, "SAE30", 5.5, 3000),
    "BRENNABOR-L8-3.4": f("ATM", E_, 3.4, "NC", 8, 3200, 1600, "SAE30", 6.5, 3000),
    "BRENNABOR-L6-2.5": f("ATM", E_, 2.5, "NC", 6, 3200, 1800, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Brennabor", lambda fam: "Brennabor")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Typ P", "P", "1", "1919-01", "1925-12", [("2.1 24", "BRENNABOR-2.1", 90)], portes=4, places=4, reservoir=50, remarques="8/24 PS, torpédo ; " + IND)
mg(L, "Typ R", "R", "1", "1925-01", "1928-12", [("1.6 25", "BRENNABOR-1.6", 75)], portes=4, places=4, reservoir=40, remarques="6/25 PS, berline ; " + IND)
mg(L, "Juwel", "Juwel", "1", "1928-01", "1933-12", [("Juwel 6 3.1 L6 55", "BRENNABOR-L6-3.1", 160), ("Juwel 8 3.4 L8 70", "BRENNABOR-L8-3.4", 180, {"debut": "1929-01"})],
   portes=4, places=5, reservoir=60, remarques="Berline et cabriolet ; " + IND)
mg(L, "Ideal", "Ideal", "1", "1931-01", "1933-12", [("2.5 L6 45", "BRENNABOR-L6-2.5", 130)], portes=4, places=4, reservoir=50, remarques="Berline ; " + IND)

MOT = Motorisations("Brennabor", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Brennabor": L}
MOTEURS = MOT.moteurs()
