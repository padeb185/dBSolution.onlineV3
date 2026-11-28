"""Métallurgique (Marchienne-au-Pont, Belgique, 1898-1928) : générations, phases, motorisations (marché européen) et moteurs liés.
12 HP, 26/60 HP (moteurs conçus par Ernst Lehmann, réputés pour leurs performances) et 15/20 HP d'après-guerre ; reprise par Imperia (1927).
Puissances en ch. Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "METAL-2C-2.0": f("ATM", "ESS", 2.0, "NC", 2, 1200, 800, "SAE30", 2.5, 1000),
    "METAL-L4-6.3": f("ATM", "ESS", 6.3, "NC", 4, 1800, 1100, "SAE30", 7.0, 1000),
    "METAL-L4-2.6": f("ATM", "ESS", 2.6, "NC", 4, 2600, 1400, "SAE30", 4.0, 2000),
}
mg = SaisieMoteurs(FAMILLES, "Métallurgique")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "12 HP", "12 HP", "1", "1903-01", "1906-12", [("2.0 12", "METAL-2C-2.0", 70)], portes=4, places=4, reservoir=40, remarques=IND)
mg(L, "26/60 HP", "26/60", "1", "1907-01", "1914-12", [("6.3 60", "METAL-L4-6.3", 300)], portes=4, places=5, reservoir=80, remarques=IND)
mg(L, "15/20 HP", "15/20", "1", "1920-01", "1927-12", [("2.6 35", "METAL-L4-2.6", 130)], portes=4, places=5, reservoir=55, remarques=IND)

MOT = Motorisations("Métallurgique", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Métallurgique": L}
MOTEURS = MOT.moteurs()
