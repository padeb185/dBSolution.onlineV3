"""Nash-Healey (Nash-Kelvinator et Donald Healey, 1951-1954) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Roadster (carrosserie Panelcraft puis Pinin Farina) et Le Mans Coupé, six cylindres Nash Ambassador ; 3e au Mans 1952.
Puissances brutes converties en ch (× 1,014). Données indicatives (environ 500 exemplaires).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {
    "NASH-L6-3.8": f("ATM", "ESS", 3.8, "NC", 6, 4000, 1600, "SAE30", 4.7, 3000),
    "NASH-L6-4.1": f("ATM", "ESS", 4.1, "NC", 6, 4000, 2000, "SAE30", 4.7, 3000),
}
mg = SaisieMoteurs(FAMILLES, "Nash")
L = []
IND = "marché nord-américain ; données indicatives"
mg(L, "Roadster", "Roadster", "1", "1951-02", "1954-12", [("3.8 L6 127", "NASH-L6-3.8", 285, {"fin": "1951-12"}), ("4.1 L6 142", "NASH-L6-4.1", 311, {"debut": "1952-01"})],
   portes=2, places=2, reservoir=76, remarques="Première voiture de sport d'après-guerre d'un grand constructeur américain ; " + IND)
mg(L, "Le Mans Coupé", "Roadster", "C", "1953-01", "1954-12", [("4.1 L6 142", "NASH-L6-4.1", 311)], portes=2, places=2, reservoir=76, remarques=IND)

MOT = Motorisations("Nash", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Nash-Healey": L}
MOTEURS = MOT.moteurs()
