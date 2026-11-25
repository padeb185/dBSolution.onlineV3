"""Marcos (Royaume-Uni) : générations, phases, motorisations et moteurs liés.
GT (Marcos 1800/1600/3-Litre puis Mantula), Mantara, LM600, GTS (TSO). Petites séries artisanales : données indicatives.
Moteurs repris des modules existants avec leurs codes : Volvo (volvo.py), Ford (ford.py, ginetta.py), Rover (land_rover.py,
ginetta.py), Chevrolet (chevrolet.py). « Talon » de l'ancienne liste non reprise (modèle non identifié avec certitude).
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .chevrolet import FAMILLES as FAMILLES_CHEVROLET
from .ginetta import FAMILLES as FAMILLES_GINETTA
from .land_rover import FAMILLES as FAMILLES_LR
from .volvo import FAMILLES as FAMILLES_VOLVO

E_ = "ESS"

VOLVO = {k: FAMILLES_VOLVO[k] for k in ("B18", "B30")}
FORD = {**{k: FAMILLES_GINETTA[k] for k in ("KENT-1.5", "ESSEX-3.0V6")},
        "KENT-1.6": f("ATM", E_, 1.6, "CHAINE", 4, 5500, 3500, "20W50", 3.25, 5000)}
ROVER = {**{k: FAMILLES_LR[k] for k in ("ROVER-V8-3.5", "ROVER-V8-4.0", "ROVER-V8-4.6", "ROVER-KV6-2.5")}, "ROVER-V8-3.9": FAMILLES_GINETTA["ROVER-V8-3.9"]}
CHEVROLET = {k: FAMILLES_CHEVROLET[k] for k in ("LT1-5.7", "LS1-5.7")}
FAMILLES = {**VOLVO, **FORD, **ROVER, **CHEVROLET}


def motoriste(fam):
    for groupe, nom in ((VOLVO, "Volvo"), (FORD, "Ford"), (ROVER, "Rover"), (CHEVROLET, "Chevrolet")):
        if fam in groupe:
            return nom
    return "Marcos"


mg = SaisieMoteurs(FAMILLES, "Marcos", motoriste)
L = []

mg(L, "GT", "1800", "1", "1964-10", "1972-12",
   [("1800 Volvo 1.8 115", "B18", 154, {"fin": "1966-12"}), ("1500 Ford 1.5 85", "KENT-1.5", 132, {"debut": "1966-06", "fin": "1968-06"}),
    ("1600 Ford 1.6 88", "KENT-1.6", 130, {"debut": "1968-06"}), ("3-Litre Ford 3.0 V6 140", "ESSEX-3.0V6", 236, {"debut": "1969-06", "fin": "1971-12"}),
    ("3-Litre Volvo 3.0 130", "B30", 208, {"debut": "1970-06", "fin": "1971-12"})], portes=2, places=2, reservoir=45,
   remarques="Coupé en fibre de verre dessiné par Dennis Adams ; châssis bois jusqu'en 1969 ; données indicatives")
mg(L, "GT", "Mantula", "1", "1983-01", "1993-12", [("Mantula 3.5 V8 192", "ROVER-V8-3.5", 298), ("Mantula 3.9 V8 193", "ROVER-V8-3.9", 300, {"debut": "1989-01"})],
   portes=2, places=2, reservoir=60, remarques="Reprise du GT avec V8 Rover ; coupé et Spyder ; données indicatives")
mg(L, "Mantara", "Mantara", "1", "1993-01", "2000-12",
   [("4.0 V8 190", "ROVER-V8-4.0", 320), ("4.6 V8 260", "ROVER-V8-4.6", 400, {"debut": "1997-01"})], portes=2, places=2, reservoir=60,
   remarques="Coupé et Spyder ; données indicatives")
mg(L, "LM600", "LM600", "1", "1997-01", "2000-12", [("Chevrolet 5.7 V8 335", "LT1-5.7", 461)], portes=2, places=2, reservoir=60,
   remarques="Version route de la voiture de course LM600 ; données indicatives")
mg(L, "GTS", "TSO", "1", "2004-06", "2007-10",
   [("GTS 2.5 V6 175", "ROVER-KV6-2.5", 240, {"fin": "2005-12"}), ("TSO GT2 5.7 V8 350", "LS1-5.7", 475)], portes=2, places=2, reservoir=60,
   remarques="Marcos TSO et GTS ; faillite de Marcos en 2007 ; données indicatives")

MOT = Motorisations("Marcos", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Marcos": L}
MOTEURS = MOT.moteurs()
