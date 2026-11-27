"""D'Ieteren : générations, phases, motorisations (marché européen) et moteurs liés.
Carrossier bruxellois (devenu importateur Volkswagen en Belgique) : Coach Springfield (carrosserie sur châssis Rolls-Royce
Springfield / Phantom, 1920-1939) et Coccinelle Cabriolet (carrosserie D'Ieteren sur Volkswagen Type 1, 1950-1960).
Moteurs repris de rolls_royce.py et volkswagen_classiques.py (mêmes familles et couples). Désignations et dates indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .rolls_royce import FAMILLES as FAMILLES_RR
from .volkswagen_classiques import FAMILLES as FAMILLES_VW

RR = {"RR-L6-7.7": FAMILLES_RR["RR-L6-7.7"]}
VW = {"BOXER-1.1": FAMILLES_VW["BOXER-1.1"], "BOXER-1.2": FAMILLES_VW["BOXER-1.2"]}
FAMILLES = {**RR, **VW}
mg = SaisieMoteurs(FAMILLES, "D'Ieteren", lambda fam: "Rolls-Royce" if fam in RR else "Volkswagen")
L = []
IND = "désignations et dates indicatives (marque ancienne), à vérifier"

mg(L, "Coach Springfield", "Springfield", "1", "1920-01", "1939-12", [("7.7 L6 101", "RR-L6-7.7", 400)], portes=2, places=4, reservoir=91,
   remarques="Carrosserie D'Ieteren sur châssis Rolls-Royce (Phantom I) ; " + IND)
mg(L, "Coccinelle Cabriolet", "Type 1", "1", "1950-01", "1960-12", [("1.1 25", "BOXER-1.1", 67, {"fin": "1953-12"}), ("1.2 30", "BOXER-1.2", 76, {"debut": "1954-01"})],
   portes=2, places=4, reservoir=40, remarques="Cabriolet carrossé par D'Ieteren sur Volkswagen Coccinelle ; " + IND)

MOT = Motorisations("D'Ieteren", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"D'Ieteren": L}
MOTEURS = MOT.moteurs()
