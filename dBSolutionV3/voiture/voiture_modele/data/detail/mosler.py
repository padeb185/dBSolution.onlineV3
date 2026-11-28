"""Mosler (Mosler Automotive, Riviera Beach, Floride) : générations, phases, motorisations (marché nord-américain) et moteurs liés.
Raptor (ex-Consulier, V8 LT1) et MT900 (supercar en carbone, V8 LS1 puis LS7 pour la MT900S). Moteurs Chevrolet repris de chevrolet.py.
Puissances en ch. Petites séries, données indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {
    "LT1-5.7": FAMILLES_CHEVROLET["LT1-5.7"], "LS1-5.7": FAMILLES_CHEVROLET["LS1-5.7"], "LS7-7.0": FAMILLES_CHEVROLET["LS7-7.0"],
}
mg = SaisieMoteurs(FAMILLES, "Chevrolet")
L = []
IND = "petite série ; données indicatives"
mg(L, "Raptor", "Raptor", "1", "1993-01", "1995-12", [("5.7 V8 LT1 304", "LT1-5.7", 461)], portes=2, places=2, reservoir=60, remarques="Coupé ex-Consulier GTP ; " + IND)
mg(L, "MT900", "MT900", "1", "2001-01", "2011-12", [("5.7 V8 350", "LS1-5.7", 475), ("MT900S 7.0 V8 608", "LS7-7.0", 760, {"debut": "2005-01", "remarques": "MT900S, LS7 préparé ; couple indicatif"})],
   portes=2, places=2, reservoir=75, remarques="Supercar à moteur central en carbone, versions GT3 / GT1 en course ; " + IND)

MOT = Motorisations("Chevrolet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mosler": L}
MOTEURS = MOT.moteurs()
