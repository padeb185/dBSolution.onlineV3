"""Pagani : générations, phases, motorisations (marché européen) et moteurs liés.
Zonda (C12, S, Roadster, F, Roadster F, Cinque, Tricolore), Huayra (Coupé, BC, Roadster, Roadster BC, Imola, Codalunga),
Huayra R et Utopia (Coupé et Roadster).
V12 Mercedes M120 6.0 repris de mercedes.py (même code) ; V12 AMG M120 7.0 / 7.3, V12 biturbo AMG M158 et V12 atmosphérique
Pagani / HWA (Huayra R) ajoutés. Séries très limitées, données indicatives. One-off et Zonda R (piste) non repris.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .mercedes import FAMILLES as FAMILLES_MERCEDES

E_ = "ESS"
C = "CHAINE"

MB = {"M120-6.0": FAMILLES_MERCEDES["M120-6.0"]}
AMG = {
    "M120-7.0-AMG": f("ATM", E_, 7.0, C, 12, 5500, 4100, "10W60", 11.0, 10000, a="V"),
    "M120-7.3-AMG": f("ATM", E_, 7.3, C, 12, 6200, 4000, "10W60", 11.0, 10000, a="V"),
    "M158-6.0TT": f("TURBO", E_, 6.0, C, 12, 6000, 2400, "5W40", 11.0, 10000, a="V"),
}
HWA = {"HWA-V12-6.0": f("ATM", E_, 6.0, C, 12, 8250, 5500, "10W60", 11.0, 5000, a="V")}
FAMILLES = {**MB, **AMG, **HWA}


def motoriste(fam):
    if fam in MB:
        return "Mercedes-Benz"
    if fam in AMG:
        return "Mercedes-AMG"
    return "HWA"


mg = SaisieMoteurs(FAMILLES, "Pagani", motoriste)
L = []
IND = "données indicatives"

mg(L, "Zonda", "C12", "1", "1999-03", "2002-12",
   [("C12 6.0 V12 394", "M120-6.0", 570), ("C12 S 7.0 V12 550", "M120-7.0-AMG", 750, {"debut": "2000-03"}), ("C12 S 7.3 V12 555", "M120-7.3-AMG", 750, {"debut": "2002-01"})],
   portes=2, places=2, reservoir=100, remarques="Coupé ; quelques exemplaires par version ; " + IND)
mg(L, "Zonda", "S", "1", "2002-03", "2005-02", [("S 7.3 V12 555", "M120-7.3-AMG", 750), ("Roadster 7.3 V12 555", "M120-7.3-AMG", 750, {"debut": "2003-03"})],
   portes=2, places=2, reservoir=100, remarques="Zonda S 7.3 et Roadster ; " + IND)
mg(L, "Zonda", "F", "1", "2005-03", "2011-12",
   [("F 7.3 V12 602", "M120-7.3-AMG", 760), ("F Clubsport 7.3 V12 650", "M120-7.3-AMG", 780), ("Roadster F 7.3 V12 650", "M120-7.3-AMG", 780, {"debut": "2006-01"}),
    ("Cinque 7.3 V12 678", "M120-7.3-AMG", 780, {"debut": "2009-01", "fin": "2010-12"}), ("Tricolore 7.3 V12 678", "M120-7.3-AMG", 780, {"debut": "2010-01", "fin": "2010-12"})],
   portes=2, places=2, reservoir=100, remarques="Zonda F, Roadster F, Cinque (5 coupés et 5 roadsters) et Tricolore ; " + IND)
mg(L, "Huayra", "Huayra", "1", "2012-01", "2018-12",
   [("6.0 V12 Biturbo 730", "M158-6.0TT", 1000), ("BC 6.0 V12 Biturbo 789", "M158-6.0TT", 1100, {"debut": "2016-03"})], portes=2, places=2, reservoir=85,
   remarques="Coupé à portes papillon ; Huayra BC (20 exemplaires) ; " + IND)
mg(L, "Huayra", "Huayra Roadster", "1", "2017-03", "2022-12",
   [("Roadster 6.0 V12 Biturbo 764", "M158-6.0TT", 1000), ("Roadster BC 6.0 V12 Biturbo 802", "M158-6.0TT", 1050, {"debut": "2019-08"}),
    ("Imola 6.0 V12 Biturbo 838", "M158-6.0TT", 1100, {"debut": "2020-02", "fin": "2020-12"}), ("Codalunga 6.0 V12 Biturbo 840", "M158-6.0TT", 1100, {"debut": "2022-06"})],
   portes=2, places=2, reservoir=85, remarques="Dont Imola (5 ex.) et Codalunga (5 ex.) ; " + IND)
mg(L, "Huayra R", "Huayra R", "1", "2021-03", None, [("6.0 V12 850", "HWA-V12-6.0", 750)], portes=2, places=1, reservoir=110,
   remarques="Voiture de piste, V12 atmosphérique ; 30 exemplaires ; " + IND)
mg(L, "Utopia", "Utopia", "1", "2023-01", None,
   [("6.0 V12 Biturbo 864", "M158-6.0TT", 1100), ("Roadster 6.0 V12 Biturbo 864", "M158-6.0TT", 1100, {"debut": "2024-09"})], portes=2, places=2, reservoir=80,
   remarques="Coupé (99 ex.) et Roadster (130 ex.) ; boîte manuelle ou automatisée ; " + IND)

MOT = Motorisations("Pagani", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Pagani": L}
MOTEURS = MOT.moteurs()
