"""Edran : générations, phases, motorisations (marché européen) et moteurs liés.
Petit constructeur : Hippo (tout-terrain, 1979-1983) et Ranger (roadster, 1984-1989). Mécanique et puissances non documentées,
saisies de manière indicative. Désignations et dates indicatives (marque ancienne), à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"EDRAN-1.6": f("ATM", "ESS", 1.6, "COURROIE", 4, 5000, 3000, "15W40", 3.5, 10000)}
mg = SaisieMoteurs(FAMILLES, "Edran", lambda fam: "Edran")
L = []
IND = "mécanique non documentée, saisie indicative ; désignations et dates indicatives, à vérifier"

mg(L, "Hippo", "Hippo", "1", "1979-01", "1983-12", [("1.6 75", "EDRAN-1.6", 120)], portes=3, places=4, reservoir=50, remarques="Tout-terrain ; " + IND)
mg(L, "Ranger", "Ranger", "1", "1984-01", "1989-12", [("1.6 75", "EDRAN-1.6", 120)], portes=0, places=2, reservoir=45, remarques="Roadster ; " + IND)

MOT = Motorisations("Edran", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Edran": L}
MOTEURS = MOT.moteurs()
