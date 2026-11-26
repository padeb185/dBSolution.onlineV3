"""Maybach : générations, phases, motorisations (marché européen) et moteurs liés.
Maybach historique (DS7 et DS8 Zeppelin), Maybach 57 et 62 (2002-2012, dont S, Zeppelin, Landaulet) et Mercedes-Maybach
(Classe S X222 et Z223, Pullman, GLS, EQS SUV, SL). Les anciennes marques « Mercedes-Maybach » et « Mercedes-Benz Maybach »
ont été supprimées du référentiel.
Moteurs Mercedes repris de mercedes.py (motoristes « Mercedes-Benz » et « Mercedes-AMG », mêmes codes) ; V12 historiques au
motoriste « Maybach » ; V12 M285 des 57/62 au motoriste « Mercedes-Benz ». Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, famille as f
from .mercedes import FAMILLES as FAMILLES_MB

E_ = "ESS"
C = "CHAINE"

MAYBACH = {
    "MAYBACH-V12-7.0": f("ATM", E_, 7.0, C, 12, 2800, 1500, "20W50", 12.0, 3000, a="V"),
    "MAYBACH-V12-8.0": f("ATM", E_, 8.0, C, 12, 3200, 1600, "20W50", 12.0, 3000, a="V"),
}
M285 = {
    "M285-5.5": f("TURBO", E_, 5.5, C, 12, 5250, 2300, "0W40", 10.0, 20000, a="V"),
    "M285-6.0": f("TURBO", E_, 6.0, C, 12, 4800, 2000, "0W40", 10.0, 20000, a="V"),
}
MB = {k: FAMILLES_MB[k] for k in ("M278-4.7", "M176-4.0", "M176-MHEV", "M177E-4.0", "M279-6.0", "M256-PHEV", "EQ-EVA2")}
AMG = {k: FAMILLES_MB[k] for k in ("M279-6.0-AMG", "M177-4.0")}
FAMILLES = {**MAYBACH, **M285, **MB, **AMG}


def motoriste(fam):
    if fam in MAYBACH:
        return "Maybach"
    return "Mercedes-AMG" if fam in AMG else "Mercedes-Benz"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Maybach", motoriste)
L = []

mg(L, "Maybach DS7 Zeppelin", "DS7", "1", "1929-01", "1933-12", [("7.0 V12 150", "MAYBACH-V12-7.0", 400)], portes=4, places=5, reservoir=135,
   remarques="Limousine de luxe ; données indicatives")
mg(L, "Maybach DS8 Zeppelin", "DS8", "1", "1930-01", "1939-12", [("8.0 V12 200", "MAYBACH-V12-8.0", 480)], portes=4, places=5, reservoir=135,
   remarques="Données indicatives")
mg(L, "Maybach 57", "W240", "1", "2002-09", "2012-12",
   [("57 5.5 V12 Biturbo 550", "M285-5.5", 900), ("57 S 6.0 V12 Biturbo 612", "M285-6.0", 1000, {"debut": "2005-09"}),
    ("57 Zeppelin 6.0 V12 Biturbo 640", "M285-6.0", 1000, {"debut": "2009-03"})], portes=4, places=5, reservoir=110, remarques="Empattement 3,39 m")
mg(L, "Maybach 62", "V240", "1", "2002-09", "2012-12",
   [("62 5.5 V12 Biturbo 550", "M285-5.5", 900), ("62 S 6.0 V12 Biturbo 612", "M285-6.0", 1000, {"debut": "2006-06"}),
    ("62 Zeppelin 6.0 V12 Biturbo 640", "M285-6.0", 1000, {"debut": "2009-03"})], portes=4, places=5, reservoir=110,
   remarques="Empattement 3,83 m ; Landaulet (2009)")

# ---------------------------------------------------------------- Mercedes-Maybach
mg(L, "Mercedes-Maybach Classe S", "X222", "1", "2015-01", "2020-12",
   [("S 500 455", "M278-4.7", 700, {"fin": "2017-06"}), ("S 560 469", "M176-4.0", 700, {"debut": "2017-07"}), ("S 600 530", "M279-6.0", 830, {"fin": "2017-06"}),
    ("S 650 630", "M279-6.0-AMG", 1000, {"debut": "2017-07"})], portes=4, places=4, reservoir=80, remarques="Empattement allongé ; restylage 2017")
mg(L, "Mercedes-Maybach Pullman", "V222", "1", "2015-06", "2020-12",
   [("S 600 Pullman 530", "M279-6.0", 830, {"fin": "2018-06"}), ("S 650 Pullman 630", "M279-6.0-AMG", 1000, {"debut": "2018-07"})], portes=4, places=6, reservoir=80,
   remarques="Limousine 6,5 m")
mg(L, "Mercedes-Maybach Classe S", "Z223", "1", "2021-02", None,
   [("S 580 503", "M176-MHEV", 700), ("S 680 612", "M279-6.0", 900), ("S 580 e 510", "M256-PHEV", 750, {"debut": "2023-06", "batterie": 28})], portes=4, places=4,
   reservoir=76, remarques="Séries Edition 100 (2021) et Emerald Isle (2025) ; restylage 2026 non détaillé")
mg(L, "Mercedes-Maybach GLS", "X167", "1", "2020-12", None, [("GLS 600 558", "M177E-4.0", 730)], portes=5, places=4, reservoir=90, remarques="Restylage 2023")
mg(L, "Mercedes-Maybach EQS SUV", "X296", "1", "2023-06", None, [("EQS 680 SUV 658", "EQ-EVA2", 950, el(116))], portes=5, places=4, reservoir=0)
mg(L, "Mercedes-Maybach SL", "R232", "1", "2025-01", None, [("SL 680 Monogram Series 585", "M177-4.0", 800)], portes=2, places=2, reservoir=70,
   remarques="Roadster dérivé du Mercedes-AMG SL")

MOT = Motorisations("Maybach", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)

DETAIL = {"Maybach": L}
MOTEURS = MOT.moteurs()
