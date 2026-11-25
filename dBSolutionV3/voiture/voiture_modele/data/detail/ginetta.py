"""Ginetta (Royaume-Uni) : générations, phases, motorisations et moteurs liés.
Routières : G4, G15, G21, G32, G33, G40R, G60, Akula. Voitures de course clients (non homologuées route) : G50, G55, G56.
Petites séries artisanales et kits : dates et puissances indicatives. Moteurs Ford repris de ford.py (motoriste « Ford ») ;
Rootes, Rover et moteurs propres Ginetta ajoutés ici. Kits (G26, G27…) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

FORD_AJOUTS = {
    "KENT-1.5": f("ATM", E_, 1.5, C, 4, 5000, 3000, "20W50", 3.25, 5000),
    "ESSEX-3.0V6": f("ATM", E_, 3.0, "NC", 6, 4750, 3000, "20W50", 4.5, 10000, a="V"),
    "CVH-1.9": f("ATM", E_, 1.9, B, 4, 5500, 4000, "15W40", 3.75, 10000),
    "CYCLONE-3.5": f("ATM", E_, 3.5, C, 6, 6500, 4500, "5W20", 5.7, 15000, a="V"),
    "CYCLONE-3.7": f("ATM", E_, 3.7, C, 6, 6500, 4500, "5W20", 5.7, 15000, a="V"),
}
FORD = {**{k: FAMILLES_FORD[k] for k in ("KENT-1.0", "CVH-1.6", "ZETEC-1.8")}, **FORD_AJOUTS}
ROOTES = {
    "IMP-0.9": f("ATM", E_, 0.9, C, 4, 6100, 4300, "20W50", 3.4, 5000),
    "ROOTES-1.7": f("ATM", E_, 1.7, C, 4, 5200, 3300, "20W50", 4.0, 5000),
}
ROVER = {"ROVER-V8-3.9": f("ATM", E_, 3.9, C, 8, 5250, 3200, "10W40", 5.0, 10000, a="V")}
PROPRES = {
    "GINETTA-V8-6.2": f("ATM", E_, 6.2, C, 8, 6800, 5000, "10W60", 8.0, 5000, a="V"),
    "GINETTA-V8-6.4": f("ATM", E_, 6.4, C, 8, 7200, 5100, "10W60", 8.0, 10000, a="V"),
}
FAMILLES = {**FORD, **ROOTES, **ROVER, **PROPRES}


def motoriste(fam):
    if fam in FORD:
        return "Ford"
    if fam in ROOTES:
        return "Rootes"
    return "Rover" if fam in ROVER else "Ginetta"


COURSE = "Voiture de course client, non homologuée pour la route"
mg = SaisieMoteurs(FAMILLES, "Ginetta", motoriste)
L = []

mg(L, "G4", "G4", "1", "1961-01", "1969-12",
   [("Ford 105E 1.0 40", "KENT-1.0", 64), ("Ford 1.5 Cortina GT 85", "KENT-1.5", 132, {"debut": "1963-01"})], portes=2, places=2, reservoir=36,
   remarques="Routière de compétition en fibre de verre (séries 1 à 4) ; données indicatives")
mg(L, "G15", "G15", "1", "1967-10", "1974-12", [("Imp 0.9 55", "IMP-0.9", 68)], portes=2, places=2, reservoir=27,
   remarques="Moteur arrière Hillman Imp Sport 875 cm³ ; données indicatives")
mg(L, "G21", "G21", "1", "1970-10", "1978-12",
   [("1.7 79", "ROOTES-1.7", 129), ("1.7 S 93", "ROOTES-1.7", 140), ("3.0 V6 128", "ESSEX-3.0V6", 235, {"fin": "1973-12"})], portes=2, places=4,
   reservoir=55, remarques="Coupé 2+2 ; moteur Sunbeam Rapier ou V6 Ford Essex ; données indicatives")
mg(L, "G32", "G32", "1", "1989-01", "1992-12",
   [("1.6 110", "CVH-1.6", 138), ("1.9 115", "CVH-1.9", 155, {"debut": "1990-06"})], portes=2, places=2, reservoir=45,
   remarques="Moteur central Ford Fiesta XR2 ; coupé et cabriolet ; données indicatives")
mg(L, "G33", "G33", "1", "1990-01", "1993-12", [("3.9 V8 198", "ROVER-V8-3.9", 298)], portes=2, places=2, reservoir=50,
   remarques="Roadster V8 Rover ; données indicatives")
mg(L, "G40", "G40R", "1", "2010-06", "2018-12", [("1.8 Zetec 137", "ZETEC-1.8", 172)], portes=2, places=2, reservoir=55,
   remarques="G40R routière dérivée de la G40 Junior/Club ; données indicatives")
mg(L, "G60", "G60", "1", "2012-01", "2015-11", [("3.7 V6 314", "CYCLONE-3.7", 393)], portes=2, places=2, reservoir=60,
   remarques="Moteur central V6 Ford, dérivée de la Farbio GTS/F400 ; production arrêtée en novembre 2015")
mg(L, "Akula", "Akula", "1", "2024-09", None, [("6.4 V8 608", "GINETTA-V8-6.4", 670)], portes=2, places=2, reservoir=100,
   remarques="20 exemplaires ; V8 atmosphérique Ginetta, boîte manuelle")

# ---------------------------------------------------------------- course
mg(L, "G50", "G50", "1", "2008-01", "2012-12", [("3.5 V6 300", "CYCLONE-3.5", 350)], portes=2, places=1, reservoir=100,
   remarques=COURSE + " (Cup, GT4)")
mg(L, "G55", "G55", "1", "2011-02", "2020-12", [("3.7 V6 GT4 360", "CYCLONE-3.7", 400)], portes=2, places=1, reservoir=100,
   remarques=COURSE + " (Supercup, GT4) ; version GT3 V8 4,35 l non reprise")
mg(L, "G56", "G56", "1", "2021-01", None,
   [("GTA 3.7 V6 274", "CYCLONE-3.7", 370), ("GT4 6.2 V8 507", "GINETTA-V8-6.2", 610)], portes=2, places=1, reservoir=100,
   remarques=COURSE + " ; GT4 Evo (2024)")

MOT = Motorisations("Ginetta", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Ginetta": L}
MOTEURS = MOT.moteurs()
