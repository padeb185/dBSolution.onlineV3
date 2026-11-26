"""Anteros : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Coupé (XTM, carrosserie spécifique sur base Chevrolet Corvette C6, 2005-2011).
V8 LS2 6.0 et LS3 6.2 repris de chevrolet.py (mêmes familles et couples). Puissances SAE nettes converties en ch (× 1,014). Données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {k: FAMILLES_CHEVROLET[k] for k in ("LS2-6.0", "LS3-6.2")}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Chevrolet")
L = []

mg(L, "Coupé", "XTM", "1", "2005-01", "2011-12", [("6.0 V8 405", "LS2-6.0", 542, {"fin": "2007-12"}), ("6.2 V8 437", "LS3-6.2", 575, {"debut": "2008-01"})],
   portes=2, places=2, reservoir=68, remarques="Coupé et roadster carrossés sur Corvette C6 (N2A Motors) ; marché nord-américain ; données indicatives")

MOT = Motorisations("Anteros", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
DETAIL = {"Anteros": L}
MOTEURS = MOT.moteurs()
