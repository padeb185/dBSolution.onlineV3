"""Mazzanti Automobili (Pontedera, Italie) : générations, phases, motorisations (marché européen) et moteurs liés.
Evantra (V8 Chevrolet LS7 7.0, 2013-2023), Evantra 771, Millecavalli et Millecavalli R (V8 biturbo dérivé du LS7), 781 et Pura (V8 6.2
à compresseur) ; production limitée à cinq voitures par an. Moteurs Chevrolet repris de chevrolet.py (familles). Puissances en ch.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET

FAMILLES = {
    "LS7-7.0": FAMILLES_CHEVROLET["LS7-7.0"], "LT4-6.2SC": FAMILLES_CHEVROLET["LT4-6.2SC"],
    "MAZZANTI-V8-7.2TT": f("TURBO", "ESS", 7.2, "CHAINE", 8, 6500, 5000, "10W60", 10.0, 10000, a="V"),
}
mg = SaisieMoteurs(FAMILLES, "Chevrolet", lambda fam: "Mazzanti" if fam.startswith("MAZZANTI") else "Chevrolet")
L = []
IND = "petite série (cinq par an)"
mg(L, "Evantra", "Evantra", "1", "2013-04", "2016-12", [("7.0 V8 751", "LS7-7.0", 860)], portes=2, places=2, reservoir=80, remarques="V8 atmosphérique LS7 ; " + IND)
mg(L, "Evantra 771", "Evantra", "2", "2017-01", "2020-12", [("7.0 V8 771", "LS7-7.0", 860)], portes=2, places=2, reservoir=80, remarques=IND + " ; couple indicatif")
mg(L, "Evantra Millecavalli", "Millecavalli", "1", "2016-10", "2019-12", [("7.2 V8 Biturbo 1014", "MAZZANTI-V8-7.2TT", 1200)], portes=2, places=2, reservoir=90, remarques="25 exemplaires ; " + IND)
mg(L, "Evantra Millecavalli R", "Millecavalli", "R", "2019-01", "2023-12", [("7.4 V8 Biturbo 1121", "MAZZANTI-V8-7.2TT", 1210)], portes=2, places=2, reservoir=90,
   remarques="V8 porté à 7,4 l (famille 7.2) ; " + IND)
mg(L, "Evantra 781", "Evantra", "3", "2020-01", "2023-12", [("6.2 V8 Compresseur 781", "LT4-6.2SC", 910)], portes=2, places=2, reservoir=80, remarques=IND + " ; couple indicatif")
mg(L, "Evantra Pura", "Pura", "1", "2021-10", "2023-12", [("6.2 V8 Compresseur 772", "LT4-6.2SC", 910)], portes=2, places=2, reservoir=80, remarques="Version allégée à boîte manuelle 7 rapports ; " + IND)

MOT = Motorisations("Chevrolet", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Mazzanti": L}
MOTEURS = MOT.moteurs()
