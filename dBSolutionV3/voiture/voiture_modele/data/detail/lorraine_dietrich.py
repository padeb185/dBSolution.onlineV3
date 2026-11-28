"""Lorraine-Dietrich (Lunéville, puis Argenteuil, 1896-1935) : générations, phases, motorisations (marché français) et moteurs liés.
Type B3-6 (15 CV, victoires aux 24 Heures du Mans 1925 et 1926), Type 15 Sport et Type 20/30. Puissances en ch.
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "LD-L6-3.4": f("ATM", "ESS", 3.4, "NC", 6, 3000, 1800, "SAE30", 6.0, 3000),
    "LD-L6-4.1": f("ATM", "ESS", 4.1, "NC", 6, 3000, 1800, "SAE30", 7.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Lorraine-Dietrich")
L = []
IND = "données indicatives (marque ancienne), à vérifier"
mg(L, "Type B3-6", "B3-6", "1", "1922-01", "1932-12", [("3.4 L6 60", "LD-L6-3.4", 180)], portes=4, places=4, reservoir=70, remarques="Six cylindres 15 CV ; " + IND)
mg(L, "Type 15 Sport", "B3-6 Sport", "1", "1925-01", "1931-12", [("3.4 L6 75", "LD-L6-3.4", 190)], portes=4, places=4, reservoir=90, remarques="Version sport, Le Mans 1925 et 1926 ; " + IND)
mg(L, "Type 20/30", "20/30", "1", "1931-01", "1934-12", [("4.1 L6 90", "LD-L6-4.1", 240)], portes=4, places=5, reservoir=80, remarques=IND)

MOT = Motorisations("Lorraine-Dietrich", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Lorraine-Dietrich": L}
MOTEURS = MOT.moteurs()
