"""CG (Chappe et Gessalin) : générations, phases, motorisations (marché européen) et moteurs liés.
Petites sportives françaises en polyester sur base Simca : 1000 Spider, 1200 S (coupé / spider) et 1300.
Moteurs Simca « Poissy » repris de simca.py (mêmes familles, couples et motoristes). Puissances en ch. Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .simca import FAMILLES as FAMILLES_SIMCA, motoriste as motoriste_simca

FAMILLES = {k: FAMILLES_SIMCA[k] for k in ("POISSY-0.9", "POISSY-1.2", "POISSY-1.3")}
mg = SaisieMoteurs(FAMILLES, "Simca", motoriste_simca)
L = []
IND = "carrosserie polyester sur base Simca 1000 ; données indicatives"

mg(L, "1000", "Spider", "1", "1966-01", "1968-12", [("0.9 52", "POISSY-0.9", 72)], portes=2, places=2, reservoir=36, remarques="Spider ; " + IND)
mg(L, "1200 S", "1200 S", "1", "1968-01", "1972-12", [("1.2 80", "POISSY-1.2", 103, {"fin": "1968-12"}), ("1.2 85", "POISSY-1.2", 105, {"debut": "1969-01"})],
   portes=2, places=2, reservoir=36, remarques="Coupé et spider ; " + IND)
mg(L, "1300", "1300", "1", "1971-01", "1974-12", [("1.3 82", "POISSY-1.3", 106), ("1.3 103", "POISSY-1.3", 118, {"debut": "1973-01"})],
   portes=2, places=2, reservoir=36, remarques="Coupé, mécanique Simca Rallye ; " + IND)

MOT = Motorisations("CG", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"CG": L}
MOTEURS = MOT.moteurs()
