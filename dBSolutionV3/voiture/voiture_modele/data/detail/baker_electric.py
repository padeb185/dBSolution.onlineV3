"""Baker Electric : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Constructeur de voitures électriques de Cleveland (Ohio) : Victoria, Torpedo (voiture de record, 1902) et Model V.
Moteurs électriques à batteries plomb. Puissances et capacités indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique

FAMILLES = {"BAKER-EV": electrique(km=5000)}
mg = SaisieMoteurs(FAMILLES, "Baker Electric", lambda fam: "Baker Electric")
L = []
IND = "électrique à batteries plomb ; désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Torpedo", "Torpedo", "1", "1902-01", "1902-12", [("Record électrique 14", "BAKER-EV", 60, {"batterie": 8})], portes=0, places=2, reservoir=0,
   remarques="Voiture de record carénée, exemplaire unique ; " + IND)
mg(L, "Victoria", "Victoria", "1", "1906-01", "1910-12", [("Électrique 3", "BAKER-EV", 30, {"batterie": 5})], portes=0, places=2, reservoir=0, remarques=IND)
mg(L, "Model V", "Model V", "1", "1910-01", "1915-12", [("Électrique 4", "BAKER-EV", 35, {"batterie": 6})], portes=2, places=4, reservoir=0,
   remarques="Coupé électrique (brougham) ; " + IND)

MOT = Motorisations("Baker Electric", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Baker Electric": L}
MOTEURS = MOT.moteurs()
