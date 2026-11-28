"""Mercer (Trenton, New Jersey, 1909-1925) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Raceabout Type 35 (quatre cylindres à culasse en T), Series 22 (L-head) et Series 6 (six cylindres). Puissances brutes converties en ch (× 1,014).
Désignations, cylindrées et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "MERCER-T4-4.9": f("ATM", "ESS", 4.9, "NC", 4, 1700, 1000, "SAE30", 5.0, 1000),
    "MERCER-L4-4.9": f("ATM", "ESS", 4.9, "NC", 4, 2500, 1200, "SAE30", 5.0, 2000),
    "MERCER-L6-4.9": f("ATM", "ESS", 4.9, "NC", 6, 2800, 1400, "SAE30", 6.0, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Mercer")
L = []
IND = "marché nord-américain ; données indicatives (marque ancienne), à vérifier"
mg(L, "Raceabout Type 35", "35", "1", "1911-01", "1914-12", [("4.9 59", "MERCER-T4-4.9", 250)], portes=0, places=2, reservoir=60, remarques="Roadster sportif emblématique ; " + IND)
mg(L, "Series 22", "22", "1", "1915-01", "1918-12", [("4.9 71", "MERCER-L4-4.9", 270)], portes=4, places=5, reservoir=70, remarques=IND)
mg(L, "Series 6", "6", "1", "1923-01", "1925-12", [("4.9 L6 72", "MERCER-L6-4.9", 260)], portes=4, places=5, reservoir=75, remarques=IND)

MOT = Motorisations("Mercer", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mercer": L}
MOTEURS = MOT.moteurs()
