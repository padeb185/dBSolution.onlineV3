"""Donnet : générations, phases, motorisations (marché européen) et moteurs liés.
Donnet-Zédel puis Donnet (Nanterre, 1924-1934, repris par Simca) : Donnet-Zédel Type G, Type 7 et Donnet 5 CV. Puissances en ch.
Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "DONNET-1.1": f("ATM", "ESS", 1.1, "NC", 4, 3000, 1800, "SAE30", 2.5, 3000),
    "DONNET-0.8": f("ATM", "ESS", 0.8, "NC", 4, 3200, 2000, "SAE30", 2.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Donnet", lambda fam: "Donnet")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Donnet-Zédel Type G", "G", "1", "1924-01", "1926-12", [("1.1 20", "DONNET-1.1", 55)], portes=4, places=4, reservoir=35, remarques="Torpédo 7 CV ; " + IND)
mg(L, "Type 7", "7", "1", "1926-01", "1930-12", [("1.1 22", "DONNET-1.1", 58)], portes=4, places=4, reservoir=35, remarques="Berline 7 CV ; " + IND)
mg(L, "Donnet 5 CV", "5 CV", "1", "1932-01", "1934-12", [("0.8 15", "DONNET-0.8", 40)], portes=2, places=4, reservoir=30,
   remarques="Petite berline, usine reprise par Simca en 1934 ; " + IND)

MOT = Motorisations("Donnet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Donnet": L}
MOTEURS = MOT.moteurs()
