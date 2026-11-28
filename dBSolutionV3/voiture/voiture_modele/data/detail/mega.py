"""Mega (Aixam-Mega, Aix-les-Bains) : générations, phases, motorisations (marché français) et moteurs liés.
Track (supercar à V12 Mercedes, 1992-1993), Monte Carlo (1996-1997), Club (buggy) et e-Worker (utilitaire électrique). Moteurs Mercedes
et Kubota repris de mercedes.py et aixam.py (mêmes codes). Puissances en ch. Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .mercedes import FAMILLES as FAMILLES_MB
from .aixam import FAMILLES as FAMILLES_AIXAM

FAMILLES = {
    "M120-6.0": FAMILLES_MB["M120-6.0"], "KUBOTA-Z482": FAMILLES_AIXAM["KUBOTA-Z482"],
    "MEGA-EV": electrique(),
}
mg = SaisieMoteurs(FAMILLES, "Mercedes-Benz", lambda fam: "Kubota" if fam.startswith("KUBOTA") else ("Mega" if fam == "MEGA-EV" else "Mercedes-Benz"))
L = []
IND = "petite série ; données indicatives"
mg(L, "Track", "Track", "1", "1992-01", "1993-12", [("6.0 V12 394", "M120-6.0", 570)], portes=2, places=2, reservoir=100, remarques="Supercar à transmission intégrale ; " + IND)
mg(L, "Monte Carlo", "Monte Carlo", "1", "1996-01", "1997-12", [("6.0 V12 394", "M120-6.0", 570)], portes=2, places=2, reservoir=100, remarques="Coupé et cabriolet ; " + IND)
mg(L, "Club", "Club", "1", "1996-01", "1999-12", [("Diesel 0.5 7", "KUBOTA-Z482", 23)], portes=0, places=2, reservoir=16, remarques="Buggy de loisirs (voiture sans permis) ; " + IND)
mg(L, "e-Worker", "e-Worker", "1", "2009-01", "2014-12", [("Électrique 20", "MEGA-EV", 80, {"batterie": 11})], portes=2, places=2, reservoir=0, remarques="Petit utilitaire électrique ; " + IND)

MOT = Motorisations("Mercedes-Benz", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mega": L}
MOTEURS = MOT.moteurs()
