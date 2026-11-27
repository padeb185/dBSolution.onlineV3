"""Dürkopp : générations, phases, motorisations (marché européen) et moteurs liés.
Dürkopp & Co. (Bielefeld) : P 8 (1910-1914) et P 12 (1919-1923). Puissances en ch DIN.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DURKOPP-2.1": f("ATM", "ESS", 2.1, "NC", 4, 1800, 1000, "SAE30", 4.0, 2000),
    "DURKOPP-3.1": f("ATM", "ESS", 3.1, "NC", 4, 2000, 1200, "SAE30", 5.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Dürkopp", lambda fam: "Dürkopp")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "P 8", "P 8", "1", "1910-01", "1914-12", [("2.1 20", "DURKOPP-2.1", 90)], portes=4, places=4, reservoir=50, remarques="Torpédo 8/20 PS ; " + IND)
mg(L, "P 12", "P 12", "1", "1919-01", "1923-12", [("3.1 30", "DURKOPP-3.1", 130)], portes=4, places=4, reservoir=55, remarques="Torpédo 12/30 PS ; " + IND)

MOT = Motorisations("Dürkopp", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Dürkopp": L}
MOTEURS = MOT.moteurs()
