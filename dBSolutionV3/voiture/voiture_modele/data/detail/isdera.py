"""Isdera (Eberhard Schulz, Leonberg) : générations, phases, motorisations (marché européen) et moteurs liés.
Spyder 033 (roadster), Imperator 108i (coupé à portes papillon) et Commendatore 112i (exemplaire unique), toutes à moteur Mercedes-Benz
(codes et couples repris de mercedes.py quand ils existent). Puissances en ch. Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .mercedes import FAMILLES as FAMILLES_MB

FAMILLES = {k: FAMILLES_MB[k] for k in ("M102-2.3", "M102-2.3-16", "M117-5.0", "M117-5.6", "M119-5.0", "M120-6.0")}
mg = SaisieMoteurs(FAMILLES, "Mercedes-Benz")
L = []
IND = "petite série ; données indicatives"

mg(L, "Spyder 033", "Spyder", "1", "1983-01", "1990-12", [("033i 2.3 136", "M102-2.3", 201, {"fin": "1987-12"}), ("033-16 2.3 16V 185", "M102-2.3-16", 235, {"debut": "1988-01"})],
   portes=0, places=2, reservoir=60, remarques="Roadster à moteur central, environ 17 exemplaires ; " + IND)
mg(L, "Imperator 108i", "Imperator", "1", "1984-01", "1993-12",
   [("5.0 V8 231", "M117-5.0", 405, {"fin": "1987-12"}), ("5.6 V8 299", "M117-5.6", 455, {"debut": "1988-01", "fin": "1990-12"}), ("5.0 V8 32V 326", "M119-5.0", 450, {"debut": "1991-01"})],
   portes=2, places=2, reservoir=85, remarques="Coupé à portes papillon (concept Mercedes CW 311), environ 30 exemplaires ; " + IND)
mg(L, "Commendatore 112i", "Commendatore", "1", "1993-01", "1999-12", [("6.0 V12 408", "M120-6.0", 580)], portes=2, places=2, reservoir=90,
   remarques="Supercar à moteur central, un seul exemplaire achevé ; " + IND)

MOT = Motorisations("Mercedes-Benz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Isdera": L}
MOTEURS = MOT.moteurs()
