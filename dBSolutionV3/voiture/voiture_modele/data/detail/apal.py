"""Apal : générations, phases, motorisations (marché européen) et moteurs liés.
Constructeur belge (Blégny, Liège) de voitures en polyester sur base Volkswagen Coccinelle : Speedster, Coupé GT, Buggy,
Corsaire et Speedster 356 (réplique Porsche 356).
Flat-4 Volkswagen repris de volkswagen_classiques.py (mêmes familles et couples). Puissances en ch DIN. Données indicatives, à vérifier.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .volkswagen_classiques import FAMILLES as FAMILLES_VW

FAMILLES = {k: FAMILLES_VW[k] for k in ("BOXER-1.2", "BOXER-1.3", "BOXER-1.5", "BOXER-1.6")}
mg = SaisieMoteurs(FAMILLES, "Volkswagen", lambda fam: "Volkswagen")
L = []
IND = "base Volkswagen Coccinelle ; données indicatives, à vérifier"

mg(L, "Speedster", "Speedster", "1", "1961-01", "1964-12", [("1.2 34", "BOXER-1.2", 82)], portes=0, places=2, reservoir=40, remarques="Roadster ; " + IND)
mg(L, "Coupé GT", "Coupé GT", "1", "1964-01", "1972-12", [("1.3 40", "BOXER-1.3", 89, {"debut": "1965-08"}), ("1.5 44", "BOXER-1.5", 102, {"debut": "1966-08"}),
                                                     ("1.2 34", "BOXER-1.2", 82, {"fin": "1966-07"})], portes=2, places=2, reservoir=40, remarques="Coupé ; " + IND)
mg(L, "Buggy", "Buggy", "1", "1968-01", "1992-12", [("1.3 44", "BOXER-1.3", 86), ("1.6 50", "BOXER-1.6", 106, {"debut": "1970-08"})], portes=0, places=4, reservoir=40,
   remarques="Buggy (Apal Buggy) ; " + IND)
mg(L, "Corsaire", "Corsaire", "1", "1975-01", "1985-12", [("1.6 50", "BOXER-1.6", 106)], portes=2, places=2, reservoir=40, remarques="Cabriolet ; " + IND)
mg(L, "Speedster 356", "Speedster 356", "1", "1981-01", "1998-12", [("1.6 50", "BOXER-1.6", 106)], portes=0, places=2, reservoir=40,
   remarques="Réplique Porsche 356 Speedster ; " + IND)

MOT = Motorisations("Apal", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Apal": L}
MOTEURS = MOT.moteurs()
