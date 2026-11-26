"""Noble : générations, phases, motorisations (marché européen) et moteurs liés.
M10, M12 (GTO, GTO-3, GTO-3R), M400, M600 (dont Speedster et Carbon Sport) et M500.
V6 Ford Duratec 2.5/3.0 (atmosphérique et biturbo) et V8 Volvo B8444 biturbo ajoutés ; V6 EcoBoost 3.5 repris de ford.py
(même code). Production artisanale, données indicatives. Prototypes M14 et M15 non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .ford import FAMILLES as FAMILLES_FORD

E_ = "ESS"
C = "CHAINE"

FORD = {
    "DURATEC-2.5V6": f("ATM", E_, 2.5, C, 6, 6250, 4250, "5W30", 5.7, 10000, a="V"),
    "DURATEC-2.5V6-BT": f("TURBO", E_, 2.5, C, 6, 6200, 3500, "5W40", 5.7, 10000, a="V"),
    "DURATEC-3.0V6-BT": f("TURBO", E_, 3.0, C, 6, 6500, 4000, "5W40", 5.7, 10000, a="V"),
    "ECOBOOST-V6-3.5": FAMILLES_FORD["ECOBOOST-V6-3.5"],
}
VOLVO = {"B8444-BT": f("TURBO", E_, 4.4, C, 8, 6800, 3800, "5W40", 7.4, 10000, a="V")}
FAMILLES = {**FORD, **VOLVO}


def motoriste(fam):
    return "Volvo" if fam in VOLVO else "Ford"


mg = SaisieMoteurs(FAMILLES, "Noble", motoriste)
L = []
IND = "données indicatives"

mg(L, "M10", "M10", "1", "1999-10", "2001-12", [("2.5 V6 170", "DURATEC-2.5V6", 231)], portes=2, places=2, reservoir=60,
   remarques="Cabriolet à moteur central ; " + IND)
mg(L, "M12", "GTO", "1", "2000-10", "2002-06", [("GTO 2.5 V6 Biturbo 310", "DURATEC-2.5V6-BT", 435)], portes=2, places=2, reservoir=70, remarques=IND)
mg(L, "M12", "GTO-3", "1", "2002-07", "2003-12", [("GTO-3 3.0 V6 Biturbo 357", "DURATEC-3.0V6-BT", 475)], portes=2, places=2, reservoir=70, remarques=IND)
mg(L, "M12", "GTO-3R", "1", "2003-06", "2007-12", [("GTO-3R 3.0 V6 Biturbo 357", "DURATEC-3.0V6-BT", 475)], portes=2, places=2, reservoir=70,
   remarques="Coupé et cabriolet (M12 GTO-3R Convertible) ; " + IND)
mg(L, "M400", "M12", "1", "2004-09", "2007-12", [("3.0 V6 Biturbo 431", "DURATEC-3.0V6-BT", 529)], portes=2, places=2, reservoir=70,
   remarques="Version allégée et radicale du M12 ; " + IND)
mg(L, "M600", "M600", "1", "2010-06", "2018-12",
   [("4.4 V8 Biturbo 659", "B8444-BT", 819), ("Speedster 4.4 V8 Biturbo 659", "B8444-BT", 819, {"debut": "2016-06"})], portes=2, places=2, reservoir=80,
   remarques="Puissance réglable 450/550/650 ch ; coupé, Carbon Sport et Speedster (cabriolet) ; " + IND)
mg(L, "M500", "M500", "1", "2023-01", None, [("3.5 V6 Biturbo 550", "ECOBOOST-V6-3.5", 650)], portes=2, places=2, reservoir=70,
   remarques="V6 Ford EcoBoost ; production confidentielle (une cinquantaine par an visée) ; " + IND)

MOT = Motorisations("Noble", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Noble": L}
MOTEURS = MOT.moteurs()
