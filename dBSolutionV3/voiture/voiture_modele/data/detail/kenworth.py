"""Kenworth (PACCAR, Kirkland, Washington) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Tracteurs routiers et camions de chantier : W900, K100 (cabine avancée), T600 (aérodynamique), T680, T880 et C500 (tout-terrain lourd).
Moteurs Cummins repris d'international.py et PACCAR MX de jonckheere.py (mêmes codes) ; Caterpillar et Detroit selon configuration non repris.
Puissances hp converties en ch (× 1,014). Poids lourds aux configurations multiples : une motorisation représentative, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .international import FAMILLES as FAMILLES_INT
from .jonckheere import FAMILLES as FAMILLES_JK

FAMILLES = {
    "CUMMINS-NTC-14.0": FAMILLES_INT["CUMMINS-NTC-14.0"], "CUMMINS-ISX-15.0": FAMILLES_INT["CUMMINS-ISX-15.0"],
    "PACCAR-MX-12.9": FAMILLES_JK["PACCAR-MX-12.9"],
}
mg = SaisieMoteurs(FAMILLES, "Cummins", lambda fam: "DAF" if fam.startswith("PACCAR") else "Cummins")
L = []
IND = "poids lourd, marché nord-américain ; motorisations multiples, données indicatives"
mg(L, "W900", "W900", "1", "1961-01", None, [("Cummins 14.0 Turbo 355", "CUMMINS-NTC-14.0", 1450, {"fin": "1997-12"}), ("Cummins 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508, {"debut": "1998-01"})],
   portes=2, places=2, reservoir=570, remarques="Tracteur à capot long emblématique (W900A, W900B, W900L) ; " + IND)
mg(L, "K100", "K100", "1", "1961-01", "2004-12", [("Cummins 14.0 Turbo 355", "CUMMINS-NTC-14.0", 1450)], portes=2, places=2, reservoir=570, remarques="Tracteur à cabine avancée ; " + IND)
mg(L, "T600", "T600", "1", "1985-01", "2011-12", [("Cummins 15.0 Turbo 456", "CUMMINS-ISX-15.0", 2100)], portes=2, places=2, reservoir=570, remarques="Premier tracteur aérodynamique américain ; " + IND)
mg(L, "T680", "T680", "1", "2012-01", None, [("PACCAR MX-13 12.9 Turbo 410", "PACCAR-MX-12.9", 1900), ("Cummins 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508)],
   portes=2, places=2, reservoir=570, remarques="Long-courrier aérodynamique ; " + IND)
mg(L, "T880", "T880", "1", "2013-01", None, [("PACCAR MX-13 12.9 Turbo 410", "PACCAR-MX-12.9", 1900), ("Cummins 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508)],
   portes=2, places=2, reservoir=380, remarques="Camion de chantier et porteur lourd ; " + IND)
mg(L, "C500", "C500", "1", "1987-01", None, [("Cummins 15.0 Turbo 507", "CUMMINS-ISX-15.0", 2508)], portes=2, places=2, reservoir=570,
   remarques="Tout-terrain lourd (pétrole, exploitation forestière) ; " + IND)

MOT = Motorisations("Cummins", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Kenworth": L}
MOTEURS = MOT.moteurs()
