"""Continental : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Division Continental de Ford : Mark II (coupé de luxe, 1956-1957) et Mark III (1958, réintégrée ensuite chez Lincoln).
V8 Lincoln Y-block 6.0 et Ford MEL 7.0 repris de lincoln.py (mêmes familles, couples et motoristes).
Puissances brutes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .lincoln import FAMILLES as FAMILLES_LINCOLN, motoriste as motoriste_lincoln

FAMILLES = {k: FAMILLES_LINCOLN[k] for k in ("LINCOLN-Y-6.0", "FORD-MEL-7.0")}
mg = SaisieMoteurs(FAMILLES, "Lincoln", motoriste_lincoln)
L = []
NA = "marché nord-américain ; données indicatives"

mg(L, "Mark II", "Mark II", "1", "1955-10", "1957-05", [("6.0 V8 289", "LINCOLN-Y-6.0", 549, {"fin": "1956-12"}), ("6.0 V8 304", "LINCOLN-Y-6.0", 563, {"debut": "1957-01"})],
   portes=2, places=5, reservoir=87, remarques="Coupé de grand luxe assemblé à la main, environ 3 000 exemplaires ; " + NA)
mg(L, "Mark III", "Mark III", "1", "1957-10", "1958-12", [("7.0 V8 380", "FORD-MEL-7.0", 664)], portes=4, places=6, reservoir=87,
   remarques="Berline, coupé, cabriolet et hardtop à lunette arrière rétractable ; " + NA)

MOT = Motorisations("Continental", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Continental": L}
MOTEURS = MOT.moteurs()
