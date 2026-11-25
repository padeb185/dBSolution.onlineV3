"""Lotus et Lotus Exige : générations, phases, motorisations (marché européen) et moteurs liés.
Lotus : Elite (Type 14 et Type 75), Elan (Type 26 et M100), Europa, Esprit, Elise (S1, S2, S3), Evora, 3-Eleven, Emira, Evija,
Eletre (dont Eletre X), Emeya. Lotus Exige : Exige S1, S2, S3 (V6).
Moteurs Toyota repris de toyota.py (motoriste « Toyota »), AMG M139 de mercedes.py (« Mercedes-AMG »), Rover K de land_rover.py
(« Rover ») ; moteurs Lotus, Coventry Climax, Renault et Isuzu ajoutés. Données anciennes indicatives.
Saisie (SaisieMoteurs) : (nom, famille, couple_nm[, surcharges]) ; la puissance est le dernier nombre du nom."""
from ._outil import Motorisations, SaisieMoteurs, electrique, famille as f
from .land_rover import FAMILLES as FAMILLES_LR
from .mercedes import FAMILLES as FAMILLES_MB
from .toyota import FAMILLES as FAMILLES_TOYOTA

E_ = "ESS"
C, B = "CHAINE", "COURROIE"

PROPRES = {
    "LOTUS-TC-1.6": f("ATM", E_, 1.6, C, 4, 6500, 4500, "20W50", 4.5, 5000),
    "LOTUS-907-2.0": f("ATM", E_, 2.0, B, 4, 6200, 4900, "10W40", 5.5, 10000),
    "LOTUS-912-2.2": f("ATM", E_, 2.2, B, 4, 6500, 5000, "10W40", 5.5, 10000),
    "LOTUS-910-2.2T": f("TURBO", E_, 2.2, B, 4, 6000, 4000, "10W40", 6.0, 10000),
    "LOTUS-920-2.0T": f("TURBO", E_, 2.0, B, 4, 6250, 3750, "10W40", 6.0, 10000),
    "LOTUS-918-3.5TT": f("TURBO", E_, 3.5, B, 8, 6500, 4250, "10W60", 7.0, 10000, a="V"),
    "2ZZ-GE-SC": f("TURBO", E_, 1.8, C, 4, 8000, 5500, "5W30", 4.2, 15000),
    "2GR-FE": f("ATM", E_, 3.5, C, 6, 6400, 4700, "0W20", 6.0, 15000, a="V"),
    "2GR-FE-SC": f("TURBO", E_, 3.5, C, 6, 7000, 4500, "0W20", 6.0, 15000, a="V"),
    "LOTUS-XHYBRID-2.0T": f("HYB_E", E_, 2.0, C, 4, 5500, 2000, "0W20", 5.0, 15000),
    "LOTUS-EV": electrique(),
}
AUTRES = {
    "CLIMAX-FWE-1.2": ("Coventry Climax", f("ATM", E_, 1.2, C, 4, 6100, 4750, "20W50", 4.5, 5000)),
    "RENAULT-16-1.5": ("Renault", f("ATM", E_, 1.5, C, 4, 6000, 4000, "20W50", 4.0, 5000)),
    "ISUZU-4XE1-1.6": ("Isuzu", f("ATM", E_, 1.6, B, 4, 7200, 4200, "10W40", 4.0, 10000)),
    "ISUZU-4XE1-1.6T": ("Isuzu", f("TURBO", E_, 1.6, B, 4, 6600, 4200, "10W40", 4.0, 10000)),
}
TOYOTA = {k: FAMILLES_TOYOTA[k] for k in ("1ZZ-FE", "2ZZ-GE", "1ZR-FAE", "2ZR-FE", "2ZR-FE-SC")}
AMG = {"M139-2.0": FAMILLES_MB["M139-2.0"]}
ROVER = {"ROVER-K-1.8": FAMILLES_LR["ROVER-K-1.8"]}
FAMILLES = {**PROPRES, **{k: v for k, (_, v) in AUTRES.items()}, **TOYOTA, **AMG, **ROVER}


def motoriste(fam):
    if fam in AUTRES:
        return AUTRES[fam][0]
    if fam in TOYOTA or fam in ("2GR-FE", "2GR-FE-SC"):
        return "Toyota"
    if fam in AMG:
        return "Mercedes-AMG"
    return "Rover" if fam in ROVER else "Lotus"


def el(kwh, **kw):
    return {"reservoir": 0, "batterie": kwh, **kw}


mg = SaisieMoteurs(FAMILLES, "Lotus", motoriste)
L = []

# ---------------------------------------------------------------- classiques
mg(L, "Elite", "Type 14", "1", "1957-10", "1963-12", [("Climax 1.2 76", "CLIMAX-FWE-1.2", 102), ("SE Climax 1.2 84", "CLIMAX-FWE-1.2", 105, {"debut": "1960-06"})],
   portes=2, places=2, reservoir=36, remarques="Coque autoporteuse en fibre de verre ; données indicatives")
mg(L, "Elan", "Type 26", "1", "1962-10", "1973-08",
   [("Twin Cam 1.6 106", "LOTUS-TC-1.6", 147), ("S4 SE Twin Cam 1.6 117", "LOTUS-TC-1.6", 147, {"debut": "1968-03"}),
    ("Sprint Twin Cam 1.6 128", "LOTUS-TC-1.6", 154, {"debut": "1971-02"})], portes=2, places=2, reservoir=45,
   remarques="Roadster et coupé, Elan +2 (1967) ; données indicatives")
mg(L, "Europa", "Type 46", "1", "1966-12", "1975-08",
   [("Renault 1.5 79", "RENAULT-16-1.5", 105, {"fin": "1971-06"}), ("Twin Cam 1.6 106", "LOTUS-TC-1.6", 147, {"debut": "1971-07", "fin": "1972-09"}),
    ("Special Twin Cam 1.6 128", "LOTUS-TC-1.6", 154, {"debut": "1972-10"})], portes=2, places=2, reservoir=32, remarques="Moteur central ; données indicatives")
mg(L, "Elite", "Type 75", "1", "1974-05", "1982-12", [("2.0 160", "LOTUS-907-2.0", 190, {"fin": "1980-06"}), ("2.2 160", "LOTUS-912-2.2", 217, {"debut": "1980-07"})],
   portes=3, places=4, reservoir=68, remarques="Shooting brake 2+2 ; Eclat (coupé) et Excel dérivés ; données indicatives")
mg(L, "Esprit", "S1-S3", "1", "1976-06", "1987-09",
   [("2.0 160", "LOTUS-907-2.0", 190, {"fin": "1980-06"}), ("2.2 162", "LOTUS-912-2.2", 217, {"debut": "1980-07"}), ("Turbo 2.2 213", "LOTUS-910-2.2T", 271, {"debut": "1980-02"})],
   portes=2, places=2, reservoir=73, remarques="Esprit dessinée par Giugiaro ; données indicatives")
mg(L, "Esprit", "X180", "1", "1987-10", "2004-02",
   [("Turbo 2.2 218", "LOTUS-910-2.2T", 298, {"fin": "1989-12"}), ("Turbo SE 2.2 268", "LOTUS-910-2.2T", 359, {"debut": "1989-06", "fin": "1995-12"}),
    ("GT3 2.0 Turbo 243", "LOTUS-920-2.0T", 295, {"debut": "1996-06", "fin": "1999-12"}), ("V8 3.5 Biturbo 354", "LOTUS-918-3.5TT", 400, {"debut": "1996-03"})],
   portes=2, places=2, reservoir=73, remarques="Restylée par Peter Stevens ; Sport 300 et S4 ; données indicatives")
mg(L, "Elan", "M100", "1", "1989-10", "1995-12", [("1.6 130", "ISUZU-4XE1-1.6", 142), ("SE Turbo 1.6 167", "ISUZU-4XE1-1.6T", 200)], portes=2, places=2, reservoir=46,
   remarques="Traction avant, moteur Isuzu ; Kia Elan (1996-1999) non reprise")

# ---------------------------------------------------------------- Elise / Evora
mg(L, "Elise", "S1", "1", "1996-08", "2001-09",
   [("1.8 120", "ROVER-K-1.8", 165), ("111S 1.8 145", "ROVER-K-1.8", 174, {"debut": "1999-06"})], portes=2, places=2, reservoir=36,
   remarques="Châssis aluminium collé ; Sport 135, 160 et 190 non détaillées")
mg(L, "Elise", "S2", "1", "2001-10", "2011-03",
   [("1.8 122", "ROVER-K-1.8", 160, {"fin": "2006-06"}), ("111S 1.8 156", "ROVER-K-1.8", 174, {"fin": "2006-06"}), ("S 1.8 136", "1ZZ-FE", 172, {"debut": "2006-07"}),
    ("111R 1.8 192", "2ZZ-GE", 180, {"debut": "2004-03"}), ("SC 1.8 Compresseur 220", "2ZZ-GE-SC", 212, {"debut": "2008-03"})], portes=2, places=2, reservoir=40,
   remarques="Moteurs Rover puis Toyota ; restylage 2010 (1.6 132 non détaillé)")
mg(L, "Elise", "S3", "1", "2011-03", "2021-12",
   [("1.6 136", "1ZR-FAE", 160, {"fin": "2016-12"}), ("S 1.8 Compresseur 220", "2ZR-FE-SC", 250), ("Sport 1.8 136", "2ZR-FE", 173, {"debut": "2017-01"}),
    ("Cup 250 1.8 Compresseur 245", "2ZR-FE-SC", 250, {"debut": "2016-06"})], portes=2, places=2, reservoir=40,
   remarques="Elise Sport 220 et Cup 250 ; production arrêtée fin 2021")
mg(L, "Evora", "Evora", "1", "2009-07", "2015-06", [("3.5 V6 280", "2GR-FE", 350), ("S 3.5 V6 Compresseur 350", "2GR-FE-SC", 400, {"debut": "2010-10"})],
   portes=2, places=4, reservoir=60, remarques="2+2 ; V6 Toyota")
mg(L, "Evora", "Evora", "2", "2015-07", "2021-12",
   [("400 3.5 V6 Compresseur 406", "2GR-FE-SC", 410, {"fin": "2018-12"}), ("GT410 3.5 V6 Compresseur 416", "2GR-FE-SC", 420, {"debut": "2019-06"}),
    ("GT430 3.5 V6 Compresseur 436", "2GR-FE-SC", 440, {"debut": "2017-06", "fin": "2018-12"})], portes=2, places=4, reservoir=60,
   remarques="Evora 400, Sport 410, GT410, GT430")
mg(L, "3-Eleven", "3-Eleven", "1", "2016-06", "2018-12", [("Road 3.5 V6 Compresseur 416", "2GR-FE-SC", 420), ("Race 3.5 V6 Compresseur 466", "2GR-FE-SC", 450)],
   portes=0, places=2, reservoir=60, remarques="311 exemplaires ; version Race non homologuée pour la route")
mg(L, "Emira", "Type 131", "1", "2022-01", None,
   [("V6 3.5 Compresseur 405", "2GR-FE-SC", 420), ("Turbo 2.0 360", "M139-2.0", 430, {"debut": "2023-06"}), ("Turbo SE 2.0 406", "M139-2.0", 480, {"debut": "2023-09"}),
    ("420 Sport 2.0 420", "M139-2.0", 480, {"debut": "2026-07"})], portes=2, places=2, reservoir=68,
   remarques="Dernière Lotus thermique ; quatre-cylindres AMG M139 ; couples des versions turbo indicatifs")

# ---------------------------------------------------------------- électriques et hybrides
mg(L, "Evija", "Type 130", "1", "2024-06", None, [("Électrique 2039", "LOTUS-EV", 1700, el(70))], portes=2, places=2, reservoir=0,
   remarques="Hypercar électrique limitée à 130 exemplaires ; date et couple indicatifs")
mg(L, "Eletre", "Type 132", "1", "2023-03", None,
   [("Eletre 612", "LOTUS-EV", 710, el(112)), ("Eletre R 918", "LOTUS-EV", 985, el(112)), ("Eletre 600 603", "LOTUS-EV", 710, el(112, debut="2024-09")),
    ("Eletre X 2.0 X-Hybrid 952", "LOTUS-XHYBRID-2.0T", 1000, {"debut": "2026-11", "batterie": 70})], portes=5, places=5, reservoir=0,
   remarques="SUV électrique 800 V produit à Wuhan ; Eletre X hybride rechargeable (livraisons fin 2026) ; couples et dates indicatifs")
mg(L, "Emeya", "Type 133", "1", "2024-04", None, [("Emeya 612", "LOTUS-EV", 710, el(102)), ("Emeya R 918", "LOTUS-EV", 985, el(102))], portes=5, places=4, reservoir=0,
   remarques="GT électrique ; données indicatives")

# ---------------------------------------------------------------- Lotus Exige
LX = []
mg(LX, "Exige", "S1", "1", "2000-06", "2001-12", [("1.8 VHPD 177", "ROVER-K-1.8", 172)], portes=2, places=2, reservoir=36, remarques="Coupé dérivé de l'Elise S1")
mg(LX, "Exige", "S2", "1", "2004-03", "2011-12",
   [("1.8 192", "2ZZ-GE", 180), ("S 1.8 Compresseur 221", "2ZZ-GE-SC", 215, {"debut": "2006-06"}), ("S 240 1.8 Compresseur 243", "2ZZ-GE-SC", 230, {"debut": "2008-06"}),
    ("Cup 260 1.8 Compresseur 260", "2ZZ-GE-SC", 236, {"debut": "2008-06"})], portes=2, places=2, reservoir=40, remarques="Moteurs Toyota")
mg(LX, "Exige", "S3", "1", "2012-03", "2016-02", [("S 3.5 V6 Compresseur 350", "2GR-FE-SC", 400)], portes=2, places=2, reservoir=40, remarques="Coupé et Roadster (2013)")
mg(LX, "Exige", "S3", "2", "2016-03", "2021-12",
   [("Sport 350 3.5 V6 Compresseur 350", "2GR-FE-SC", 400), ("Sport 380 3.5 V6 Compresseur 380", "2GR-FE-SC", 410),
    ("Cup 380 3.5 V6 Compresseur 380", "2GR-FE-SC", 410), ("Sport 410 3.5 V6 Compresseur 416", "2GR-FE-SC", 420, {"debut": "2018-06"}),
    ("Cup 430 3.5 V6 Compresseur 436", "2GR-FE-SC", 440, {"debut": "2017-10"})], portes=2, places=2, reservoir=40,
   remarques="Production arrêtée fin 2021 avec l'Elise et l'Evora")

MOT = Motorisations("Lotus", FAMILLES, mg.table, mg.eres, prefixes=())
MOT.lier(L)
MOT.lier(LX)

DETAIL = {"Lotus": L, "Lotus Exige": LX}
MOTEURS = MOT.moteurs()
