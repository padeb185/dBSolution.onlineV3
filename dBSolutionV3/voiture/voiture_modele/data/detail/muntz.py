"""Muntz (Muntz Car Company, Glendale puis Evanston, 1950-1954) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Muntz Jet (dérivé de la Kurtis Sport Car) : V8 Cadillac, puis V8 Lincoln (code repris de lincoln.py). Puissances brutes converties en ch (× 1,014).
Données indicatives (environ 400 exemplaires).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .lincoln import FAMILLES as FAMILLES_LINCOLN

FAMILLES = {
    "CADILLAC-V8-5.4": f("ATM", "ESS", 5.4, "CHAINE", 8, 3800, 1800, "10W30", 4.7, 5000, a="V"),
    "LINCOLN-V8-5.5": FAMILLES_LINCOLN["LINCOLN-V8-5.5"],
}
mg = SaisieMoteurs(FAMILLES, "Cadillac", lambda fam: "Lincoln" if fam.startswith("LINCOLN") else "Cadillac")
L = []
mg(L, "Jet", "Jet", "1", "1950-01", "1954-12", [("5.4 V8 162", "CADILLAC-V8-5.4", 420, {"fin": "1951-12"}), ("5.5 V8 154", "LINCOLN-V8-5.5", 359, {"debut": "1951-06"})],
   portes=2, places=4, reservoir=75, remarques="Cabriolet à hard-top, 4 places ; marché nord-américain ; données indicatives")

MOT = Motorisations("Cadillac", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Muntz": L}
MOTEURS = MOT.moteurs()
