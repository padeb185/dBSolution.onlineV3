"""Ligier : générations, phases, motorisations et moteurs liés.
Sportive JS2 (V6 Maserati) ; quadricycles légers sans permis (45 km/h) : Optimax, BE Up/BE Two, X-Too, Pulse 4, Ixo, JS50,
JS50L, Myli, JS60 ; voitures de course clients JS2 R et JS P4 (non homologuées route).
Moteurs propres au motoriste « Ligier » (diesels de quadricycles, électrique), V6 Maserati au motoriste « Maserati »,
V6 Ford 3.7 repris de ginetta.py (motoriste « Ford »). Puissances des quadricycles en ch arrondis ; données indicatives.
Prototype JS1 et modèles JS3, JS51, JS55, JS2 RS non repris faute de données fiables.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .ginetta import FAMILLES as FAMILLES_GINETTA

E_, D = "ESS", "DSL"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "LOMBARDINI-0.5": f("ATM", D, 0.5, B, 2, 3200, 2200, "10W40", 1.6, 5000),
    "LIGIER-DCI-0.5": f("ATM", D, 0.5, B, 2, 3200, 2200, "10W40", 1.6, 5000),
    "LIGIER-REVO-0.5": f("ATM", D, 0.5, B, 1, 3000, 2200, "10W30", 1.6, 5000),
    "LIGIER-EV": electrique(),
}
MASERATI = {
    "MASERATI-C114-2.7": f("ATM", E_, 2.7, C, 6, 5500, 4000, "20W50", 7.0, 5000, a="V"),
    "MASERATI-C114-3.0": f("ATM", E_, 3.0, C, 6, 5500, 4000, "20W50", 7.0, 5000, a="V"),
}
FORD = {"CYCLONE-3.7": FAMILLES_GINETTA["CYCLONE-3.7"]}
FAMILLES = {**PROPRES, **MASERATI, **FORD}


def motoriste(fam):
    return "Maserati" if fam in MASERATI else ("Ford" if fam in FORD else "Ligier")


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


SP = "Quadricycle léger sans permis (45 km/h)"
COURSE = "Voiture de course client, non homologuée pour la route"
mg = SaisieMoteurs(FAMILLES, "Ligier", motoriste)
L = []

mg(L, "JS2", "JS2", "1", "1971-10", "1975-12",
   [("2.7 V6 170", "MASERATI-C114-2.7", 250, {"fin": "1974-06"}), ("3.0 V6 195", "MASERATI-C114-3.0", 255, {"debut": "1974-07"})], portes=2, places=2, reservoir=60,
   remarques="Coupé à moteur central V6 Maserati (Citroën SM) ; environ 250 exemplaires ; données indicatives")

# ---------------------------------------------------------------- quadricycles
mg(L, "Optimax", "Optimax", "1", "2001-01", "2008-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=16,
   remarques=SP + " ; données indicatives")
mg(L, "BE", "BE", "1", "2001-01", "2008-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=16,
   remarques=SP + " ; BE Up (sans portes) et BE Two ; données indicatives")
mg(L, "X-too RS", "X-Too", "1", "2006-01", "2013-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=2, reservoir=16,
   remarques=SP + " ; X-Too, X-Too R, RS et Max ; données indicatives")
mg(L, "Pulse 4", "Pulse", "1", "2010-01", "2013-12", [("Diesel 0.5 7", "LOMBARDINI-0.5", 23)], portes=2, places=4, reservoir=16,
   remarques="Quadricycle lourd 4 places ; données indicatives")
mg(L, "Ixo", "Ixo", "1", "2013-06", "2019-12", [("DCI 0.5 8", "LIGIER-DCI-0.5", 26), ("Électrique 8", "LIGIER-EV", 10, el(6, debut="2015-01"))], portes=2, places=2,
   reservoir=16, remarques=SP + " ; données indicatives")
mg(L, "JS50", "JS50", "1", "2013-09", "2024-10", [("DCI 0.5 8", "LIGIER-DCI-0.5", 26), ("Électrique 8", "LIGIER-EV", 10, el(6, debut="2016-01"))], portes=2,
   places=2, reservoir=16, remarques=SP + " ; restylages 2017 et 2020 ; données indicatives")
mg(L, "JS50", "JS50 (2024)", "1", "2024-11", None,
   [("Électrique 8", "LIGIER-EV", 10, el(8)), ("Électrique Haute Performance 8", "LIGIER-EV", 10, el(12)),
    ("Diesel REVO D+ 0.5 8", "LIGIER-REVO-0.5", 27, {"debut": "2025-03"}), ("Électrique B11 8", "LIGIER-EV", 10, el(11, debut="2026-01"))],
   portes=2, places=2, reservoir=17, remarques=SP + " ; nouvelle génération ; moteur électrique Valeo 5,6 kW")
mg(L, "JS50L", "JS50", "1", "2014-06", "2024-10", [("DCI 0.5 8", "LIGIER-DCI-0.5", 26)], portes=2, places=2, reservoir=16,
   remarques=SP + " ; version allongée ; données indicatives")
mg(L, "Myli", "Myli", "1", "2023-03", None,
   [("Électrique Standard 8", "LIGIER-EV", 10, el(4)), ("Électrique Étendue 8", "LIGIER-EV", 10, el(8)), ("Électrique Haute Performance 8", "LIGIER-EV", 10, el(12)),
    ("Diesel 0.5 8", "LIGIER-REVO-0.5", 27, {"debut": "2023-11"})], portes=2, places=2, reservoir=17,
   remarques=SP + " ; moteur Valeo 5,6 kW et 10,4 Nm (électrique), monocylindre diesel 6 kW et 26 Nm")
mg(L, "JS60", "JS60", "1", "2026-03", None, [("Électrique 8", "LIGIER-EV", 10, el(11)), ("Diesel REVO D+ 0.5 8", "LIGIER-REVO-0.5", 27)], portes=2, places=2,
   reservoir=17, remarques="Versions L6e (45 km/h) et L7e (75 km/h, permis B1) ; date indicative")

# ---------------------------------------------------------------- course
mg(L, "JS2 R", "JS2 R", "1", "2015-01", None, [("3.7 V6 340", "CYCLONE-3.7", 410)], portes=2, places=1, reservoir=80,
   remarques=COURSE + " (coupé, monotype Ligier JS Cup) ; données indicatives")
mg(L, "JS P4", "JS P4", "1", "2018-01", None, [("3.7 V6 340", "CYCLONE-3.7", 410)], portes=0, places=1, reservoir=80,
   remarques=COURSE + " (prototype LMP4) ; données indicatives")

MOT = Motorisations("Ligier", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ligier": L}
MOTEURS = MOT.moteurs()
