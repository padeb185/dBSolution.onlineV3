"""Czinger : générations, phases, motorisations (marché nord-américain) et moteurs liés.
21C, hypercar hybride à structure imprimée en 3D (Los Angeles), places en tandem : V8 2.88 biturbo à vilebrequin plat
(11 000 tr/min) et moteurs électriques avant, batterie lithium-titanate 2 kWh ; 80 exemplaires prévus (route et Lightweight Track).
Puissances hp converties en ch (× 1,014). Le couple indiqué est celui du V8 seul.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f

FAMILLES = {"CZINGER-V8-2.9TT-HYB": f("HYB_TE", "ESS", 2.9, "CHAINE", 8, 10500, 8000, "5W50", 9.0, 5000, a="V")}
mg = SaisieMoteurs(FAMILLES, "Czinger", lambda fam: "Czinger")
L = []

mg(L, "21C", "21C", "1", "2023-10", None, [("Hybrid 2.9 V8 TT 1267", "CZINGER-V8-2.9TT-HYB", 746, {"batterie": 2}),
                                          ("Blackbird Hybrid 2.9 V8 TT 1369", "CZINGER-V8-2.9TT-HYB", 746, {"batterie": 2})],
   portes=2, places=2, reservoir=55, remarques="Fabrication depuis 2021, livraisons à partir de fin 2023 ; transmission intégrale, boîte séquentielle Xtrac 7 rapports ; "
                                               "pack +100 hp (Blackbird) ; réservoir indicatif ; marché nord-américain")

MOT = Motorisations("Czinger", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Czinger": L}
MOTEURS = MOT.moteurs()
