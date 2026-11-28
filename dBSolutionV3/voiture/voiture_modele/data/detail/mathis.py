"""Mathis (Émile Mathis, Strasbourg, 1910-1950) : générations, phases, motorisations (marché français) et moteurs liés.
Babylette (cyclecar), SB, Emyquatre (« Emy-4 ») et 333 (trois roues à flat-twin, 1946-1948). Puissances en ch.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MATHIS-L4-0.9": f("ATM", "ESS", 0.9, "NC", 4, 2400, 1500, "SAE30", 2.5, 2000),
    "MATHIS-L4-1.1": f("ATM", "ESS", 1.1, "NC", 4, 3000, 1800, "SAE30", 3.0, 2000),
    "MATHIS-L4-1.2": f("ATM", "ESS", 1.2, "NC", 4, 3400, 2000, "SAE30", 3.0, 3000),
    "MATHIS-B2-0.7": f("ATM", "ESS", 0.7, "NC", 2, 4000, 2500, "SAE30", 2.0, 3000, a="PLAT"),
}
mg = SaisieMoteurs(FAMILLES, "Mathis")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Babylette", "Babylette", "1", "1913-01", "1914-12", [("0.9 10", "MATHIS-L4-0.9", 40)], portes=0, places=2, reservoir=25, remarques="Cyclecar ; " + IND)
mg(L, "SB", "SB", "1", "1921-01", "1923-12", [("1.1 18", "MATHIS-L4-1.1", 55)], portes=4, places=4, reservoir=35, remarques=IND)
mg(L, "Emyquatre", "Emy-4", "1", "1932-01", "1934-12", [("1.2 28", "MATHIS-L4-1.2", 70)], portes=4, places=4, reservoir=40, remarques=IND)
mg(L, "333", "333", "1", "1946-01", "1948-12", [("0.7 Flat-twin 15", "MATHIS-B2-0.7", 38)], portes=2, places=3, reservoir=30,
   remarques="Trois roues, trois places, caisse en aluminium ; une dizaine de préséries ; " + IND)

MOT = Motorisations("Mathis", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mathis": L}
MOTEURS = MOT.moteurs()
